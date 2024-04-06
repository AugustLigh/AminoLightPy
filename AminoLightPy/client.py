from uuid import uuid4
from base64 import b64encode
from typing import BinaryIO, Union

from .constants import *
from .lib.util import exceptions, objects, helpers
from .socket import Callbacks, SocketHandler, SocketRequests


#@dorthegra/IDörthe#8835 thanks for support!

class Client(Callbacks, SocketHandler, SocketRequests):
    def __init__(self, proxies: dict = None, socketDebugging = False, socket_enabled = True):
        self.api = api
        self.authenticated = False
        self.session = AminoSession()

        self.socket_enabled = socket_enabled
        if socket_enabled:
            handler = SocketHandler.__init__(self, self, socketDebugging)
            SocketRequests.__init__(self, handler)
            Callbacks.__init__(self)

        self.session.proxies = proxies

        self.sid = None
        self.profile: objects.UserProfile = objects.UserProfile(None).UserProfile
        self.profile.session = self.session


    def parse_headers(self, data: str = None) -> dict:
        base_headers: dict = self.session.headers
        if data:
            base_headers["NDC-MSG-SIG"] = helpers.signature(data)

        return base_headers


    def login_sid(self, SID: str):
        """
        Login into an account with an SID

        **Parameters**
            - **SID** : SID of the account
        """
        userId = helpers.sid_to_uid(SID)
        self.authenticated = True
        self.sid = SID

        self.profile: objects.UserProfile = objects.UserProfile({"uid": userId}).UserProfile
        # self.profile: objects.UserProfile = self.get_user_info(userId)
    
        self.session.headers.update({
            "NDCAUTH": f"sid={self.sid}",
            "AUID": self.profile.userId
            })

        self.profile.session = self.session

        if self.socket_enabled:
            self.run_amino_socket()

    def login(self, email: str, password: str):
        """
        Login into an account.

        **Parameters**
            - **email** : Email of the account.
            - **password** : Password of the account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        data = {
            "email": email,
            "secret": f"0 {password}",
            "clientType": 100,
            "deviceID": device_id
        }

        response = self.session.post(f"{api}/g/s/auth/login", json=data)
        self.authenticated = True
        json = response.json()
        self.sid = json["sid"]
        self.profile: objects.UserProfile = objects.UserProfile(json["userProfile"]).UserProfile

        self.session.headers.update({
            "NDCAUTH": f"sid={self.sid}",
            "AUID": self.profile.userId
        })

        self.profile.session = self.session

        if self.socket_enabled:
            self.run_amino_socket()

        return json

    def login_phone(self, phoneNumber: str, password: str):
        """
        Login into an account.

        **Parameters**
            - **phoneNumber** : Phone number of the account.
            - **password** : Password of the account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "phoneNumber": phoneNumber,
            "v": 2,
            "secret": f"0 {password}",
            "deviceID": device_id,
            "clientType": 100,
            "action": "normal",
        }

        response = self.session.post(f"{api}/g/s/auth/login", json=data)
        self.authenticated = True
        json = response.json()
        self.sid = json["sid"]

        self.profile: objects.UserProfile = objects.UserProfile(json["userProfile"]).UserProfile

        self.session.headers.update({
            "NDCAUTH": f"sid={self.sid}",
            "AUID": self.profile.userId
        })

        self.profile.session = self.session

        if self.socket_enabled:
            self.run_amino_socket()

        return json

    def login_secret(self, secret: str):
        """
        Login into an account.

        **Parameters**
            - **secret** : Secret of the account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "v": 2,
            "secret": secret,
            "deviceID": device_id,
            "clientType": 100,
            "action": "normal",
        }

        response = self.session.post(f"{api}/g/s/auth/login", json=data)
        self.authenticated = True
        json = response.json()
        self.sid = json["sid"]

        self.profile: objects.UserProfile = objects.UserProfile(json["userProfile"]).UserProfile

        self.session.headers.update({
            "NDCAUTH": f"sid={self.sid}",
            "AUID": self.profile.userId
        })

        self.profile.session = self.session

        if self.socket_enabled:
            self.run_amino_socket()

        return json

    def register(self, nickname: str, email: str, password: str, verificationCode: str, deviceId: str = None):
        """
        Register an account.

        **Parameters**
            - **nickname** : Nickname of the account.
            - **email** : Email of the account.
            - **password** : Password of the account.
            - **verificationCode** : Verification code.
            - **deviceId** : The device id being registered to.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        if deviceId == None: deviceId = device_id

        data = {
            "secret": f"0 {password}",
            "deviceID": deviceId,
            "email": email,
            "clientType": 100,
            "nickname": nickname,
            "latitude": 0,
            "longitude": 0,
            "address": None,
            "clientCallbackURL": "narviiapp://relogin",
            "validationContext": {
                "data": {
                    "code": verificationCode
                },
                "type": 1,
                "identity": email
            },
            "type": 1,
            "identity": email,
        }     

        response = self.session.post(f"{api}/g/s/auth/register", json=data)
        return response.json()

    def restore(self, email: str, password: str):
        """
        Restore a deleted account.

        **Parameters**
            - **email** : Email of the account.
            - **password** : Password of the account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "secret": f"0 {password}",
            "deviceID": device_id,
            "email": email
        }

        response = self.session.post(f"{api}/g/s/account/delete-request/cancel", json=data)
        return response.status_code

    def logout(self):
        """
        Logout from an account.

        **Parameters**
            - No parameters required.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "deviceID": device_id,
            "clientType": 100
        }

        response = self.session.post(f"{api}/g/s/auth/logout", json=data)
        self.authenticated = False
        self.sid = None
        self.profile: None
        self.session.headers.update({
            "NDCAUTH": None,
            "AUID": None
        })

        self.profile.session = None

        if self.socket_enabled:
            self.close()

        return response.status_code

    def configure(self, age: int, gender: str):
        """
        Configure the settings of an account.

        **Parameters**
            - **age** : Age of the account. Minimum is 13.
            - **gender** : Gender of the account.
                - ``Male``, ``Female`` or ``Non-Binary``

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if gender.lower() == "male": gender = 1
        elif gender.lower() == "female": gender = 2
        elif gender.lower() == "non-binary": gender = 255
        else: raise exceptions.SpecifyType

        if age <= 12: raise exceptions.AgeTooLow

        data = {
            "age": age,
            "gender": gender,
        }

        response = self.session.post(f"{api}/g/s/persona/profile/basic", json=data)
        return response.status_code

    def verify(self, email: str, code: str):
        """
        Verify an account.

        **Parameters**
            - **email** : Email of the account.
            - **code** : Verification code.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "validationContext": {
                "type": 1,
                "identity": email,
                "data": {"code": code}},
            "deviceID": device_id,
        }

        response = self.session.post(f"{api}/g/s/auth/check-security-validation", json=data)
        return response.status_code

    def request_verify_code(self, email: str, resetPassword: bool = False):
        """
        Request an verification code to the targeted email.

        **Parameters**
            - **email** : Email of the account.
            - **resetPassword** : If the code should be for Password Reset.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "identity": email,
            "type": 1,
            "deviceID": device_id
        }

        if resetPassword is True:
            data["level"] = 2
            data["purpose"] = "reset-password"

        response = self.session.post(f"{api}/g/s/auth/request-security-validation", json=data)
        return response.status_code

    def activate_account(self, email: str, code: str):
        """
        Activate an account.

        **Parameters**
            - **email** : Email of the account.
            - **code** : Verification code.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        data = {
            "type": 1,
            "identity": email,
            "data": {"code": code},
            "deviceID": device_id
        }

        response = self.session.post(f"{api}/g/s/auth/activate-email", json=data)
        return response.status_code

    # Provided by "𝑰 𝑵 𝑻 𝑬 𝑹 𝑳 𝑼 𝑫 𝑬#4082"
    def delete_account(self, password: str):
        """
        Delete an account.

        **Parameters**
            - **password** : Password of the account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        data = {
            "deviceID": device_id,
            "secret": f"0 {password}"
        }

        response = self.session.post(f"{api}/g/s/account/delete-request", json=data)
        return response.status_code

    def change_password(self, email: str, password: str, code: str):
        """
        Change password of an account.

        **Parameters**
            - **email** : Email of the account.
            - **password** : Password of the account.
            - **code** : Verification code.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        data = {
            "updateSecret": f"0 {password}",
            "emailValidationContext": {
                "data": {
                    "code": code
                },
                "type": 1,
                "identity": email,
                "level": 2,
                "deviceID": device_id
            },
            "phoneNumberValidationContext": None,
            "deviceID": device_id
        }

        response = self.session.post(f"{api}/g/s/auth/reset-password", json=data)
        return response.status_code


    def get_account_info(self):
        response = self.session.get(f"{api}/g/s/account")
        return objects.UserProfile(response.json()["account"]).UserProfile

    def handle_socket_message(self, data):
        return self.resolve(data)

    def get_eventlog(self):
        response = self.session.get(f"{api}/g/s/eventlog/profile?language=en")
        return response.json()

    def sub_clients(self, start: int = 0, size: int = 25):
        """
        List of Communities the account is in.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Community List <amino.lib.util.objects.CommunityList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if not self.authenticated: raise exceptions.NotLoggedIn
        response = self.session.get(f"{api}/g/s/community/joined?v=1&start={start}&size={size}")
        return objects.CommunityList(response.json()["communityList"]).CommunityList

    def sub_clients_profile(self, start: int = 0, size: int = 25):
        if not self.authenticated: raise exceptions.NotLoggedIn
        response = self.session.get(f"{api}/g/s/community/joined?v=1&start={start}&size={size}")
        return response.json()["userInfoInCommunities"]

    def get_user_info(self, userId: str):
        """
        Information of an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : :meth:`User Object <amino.lib.util.objects.UserProfile>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/user-profile/{userId}")
        return objects.UserProfile(response.json()["userProfile"]).UserProfile

    def get_chat_threads(self, start: int = 0, size: int = 25):
        """
        List of Chats the account is in.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Chat List <amino.lib.util.objects.ThreadList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/chat/thread?type=joined-me&start={start}&size={size}")
        return objects.ThreadList(response.json()["threadList"]).ThreadList

    def get_chat_thread(self, chatId: str):
        """
        Get the Chat Object from an Chat ID.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : :meth:`Chat Object <amino.lib.util.objects.Thread>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/chat/thread/{chatId}")
        return objects.Thread(response.json()["thread"]).Thread

    def get_chat_users(self, chatId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/g/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2")
        return objects.UserProfileList(response.json()["memberList"]).UserProfileList

    def join_chat(self, chatId: str):
        """
        Join an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/member/{self.profile.userId}")
        return response.status_code

    def leave_chat(self, chatId: str):
        """
        Leave an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.delete(f"{api}/g/s/chat/thread/{chatId}/member/{self.profile.userId}")
        return response.status_code

    def start_chat(self, userId: Union[str, list], message: str, title: str = None, content: str = None, isGlobal: bool = False, publishToGlobal: bool = False):
        """
        Start an Chat with an User or List of Users.

        **Parameters**
            - **userId** : ID of the User or List of User IDs.
            - **message** : Starting Message.
            - **title** : Title of Group Chat.
            - **content** : Content of Group Chat.
            - **isGlobal** : If Group Chat is Global.
            - **publishToGlobal** : If Group Chat should show in Global.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if isinstance(userId, str): userIds = [userId]
        elif isinstance(userId, list): userIds = userId
        elif isinstance(userId, tuple): userIds = userId
        else: raise exceptions.WrongType

        data = {
            "title": title,
            "inviteeUids": userIds,
            "initialMessageContent": message,
            "content": content,
        }

        if isGlobal is True:
            data["type"] = 2
            data["eventSource"] = "GlobalComposeMenu"
        else: data["type"] = 0

        if publishToGlobal is True: data["publishToGlobal"] = 1
        else: data["publishToGlobal"] = 0


        response = self.session.post(f"{api}/g/s/chat/thread", json=data)
        return objects.Thread(response.json()["thread"]).Thread

    def invite_to_chat(self, userId: Union[str, list], chatId: str):
        """
        Invite a User or List of Users to a Chat.

        **Parameters**
            - **userId** : ID of the User or List of User IDs.
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if isinstance(userId, str): userIds = [userId]
        elif isinstance(userId, list): userIds = userId
        elif isinstance(userId, tuple): userIds = userId
        else: raise exceptions.WrongType

        data = {
            "uids": userIds
        }

        response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/member/invite", json=data)
        return response.status_code

    def kick(self, userId: str, chatId: str, allowRejoin: bool = True):
        if allowRejoin: allowRejoin = 1
        if not allowRejoin: allowRejoin = 0

        response = self.session.delete(f"{api}/g/s/chat/thread/{chatId}/member/{userId}?allowRejoin={allowRejoin}")
        return response.status_code

    def get_chat_messages(self, chatId: str, size: int = 25, pageToken: str = None):
        """
        List of Messages from an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.
            - *size* : Size of the list.
            - *size* : Size of the list.
            - *pageToken* : Next Page Token.

        **Returns**
            - **Success** : :meth:`Message List <amino.lib.util.objects.MessageList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if not pageToken: url = f"{api}/g/s/chat/thread/{chatId}/message?v=2&pagingType=t&pageToken={pageToken}&size={size}"
        else: url = f"{api}/g/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}"

        response = self.session.get(url)
        return objects.GetMessages(response.json()).GetMessages

    def get_message_info(self, chatId: str, messageId: str):
        """
        Information of an Message from an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.
            - **messageId** : ID of the Message.

        **Returns**
            - **Success** : :meth:`Message Object <amino.lib.util.objects.Message>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/chat/thread/{chatId}/message/{messageId}")
        return objects.Message(response.json()["message"]).Message

    def get_community_info(self, comId: int):
        """
        Information of an Community.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **Success** : :meth:`Community Object <amino.lib.util.objects.Community>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s-x{comId}/community/info?withInfluencerList=1&withTopicList=true&influencerListOrderStrategy=fansCount")
        return objects.Community(response.json()["community"]).Community

    def search_community(self, aminoId: str):
        """
        Search a Community byt its Amino ID.

        **Parameters**
            - **aminoId** : Amino ID of the Community.

        **Returns**
            - **Success** : :meth:`Community List <amino.lib.util.objects.CommunityList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/search/amino-id-and-link?q={aminoId}")
        result = response.json()["resultList"]
        if len(result) == 0: raise exceptions.CommunityNotFound(aminoId)
        else: return objects.CommunityList([com["refObject"] for com in result]).CommunityList

    def get_user_following(self, userId: str, start: int = 0, size: int = 25):
        """
        List of Users that the User is Following.

        **Parameters**
            - **userId** : ID of the User.
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`User List <amino.lib.util.objects.UserProfileList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/user-profile/{userId}/joined?start={start}&size={size}")
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList

    def get_user_followers(self, userId: str, start: int = 0, size: int = 25):
        """
        List of Users that are Following the User.

        **Parameters**
            - **userId** : ID of the User.
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`User List <amino.lib.util.objects.UserProfileList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/user-profile/{userId}/member?start={start}&size={size}")
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList

    def get_blocked_users(self, start: int = 0, size: int = 25):
        """
        List of Users that the User Blocked.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Users List <amino.lib.util.objects.UserProfileList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/block?start={start}&size={size}")
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList

    def get_blog_info(self, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None):
        if blogId or quizId:
            if quizId is not None: blogId = quizId
            response = self.session.get(f"{api}/g/s/blog/{blogId}")
            return objects.GetBlogInfo(response.json()).GetBlogInfo

        elif wikiId:
            response = self.session.get(f"{api}/g/s/item/{wikiId}")
            return objects.GetBlogInfo(response.json()).GetWikiInfo

        elif fileId:
            response = self.session.get(f"{api}/g/s/shared-folder/files/{fileId}")
            return objects.SharedFolderFile(response.json()["file"]).SharedFolderFile

        else: raise exceptions.SpecifyType()

    def get_blog_comments(self, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, sorting: str = "newest", start: int = 0, size: int = 25):
        if sorting == "newest": sorting = "newest"
        elif sorting == "oldest": sorting = "oldest"
        elif sorting == "top": sorting = "vote"
        else: raise exceptions.WrongType(sorting)

        if blogId or quizId:
            if not quizId: 
                blogId = quizId
            url = f"{api}/g/s/blog/{blogId}/comment?sort={sorting}&start={start}&size={size}"
        elif wikiId: url = f"{api}/g/s/item/{wikiId}/comment?sort={sorting}&start={start}&size={size}"
        elif fileId: url = f"{api}/g/s/shared-folder/files/{fileId}/comment?sort={sorting}&start={start}&size={size}",
        else: raise exceptions.SpecifyType

        response = self.session.get(url)
        return objects.CommentList(response.json()["commentList"]).CommentList

    def get_blocker_users(self, start: int = 0, size: int = 25):
        """
        List of Users that are Blocking the User.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`List of User IDs <None>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/block/full-list?start={start}&size={size}")
        return response.json()["blockerUidList"]

    def get_wall_comments(self, userId: str, sorting: str, start: int = 0, size: int = 25):
        """
        List of Wall Comments of an User.

        **Parameters**
            - **userId** : ID of the User.
            - **sorting** : Order of the Comments.
                - ``newest``, ``oldest``, ``top``
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Comments List <amino.lib.util.objects.CommentList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if sorting.lower() == "newest": sorting = "newest"
        elif sorting.lower() == "oldest": sorting = "oldest"
        elif sorting.lower() == "top": sorting = "vote"
        else: raise exceptions.WrongType(sorting)

        response = self.session.get(f"{api}/g/s/user-profile/{userId}/g-comment?sort={sorting}&start={start}&size={size}")
        return objects.CommentList(response.json()["commentList"]).CommentList

    def flag(self, reason: str, flagType: int, userId: str = None, blogId: str = None, wikiId: str = None, asGuest: bool = False):
        """
        Flag a User, Blog or Wiki.

        **Parameters**
            - **reason** : Reason of the Flag.
            - **flagType** : Type of the Flag.
            - **userId** : ID of the User.
            - **blogId** : ID of the Blog.
            - **wikiId** : ID of the Wiki.
            - *asGuest* : Execute as a Guest.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if reason is None: raise exceptions.ReasonNeeded
        if flagType is None: raise exceptions.FlagTypeNeeded

        data = {
            "flagType": flagType,
            "message": reason
        }

        if userId:
            data["objectId"] = userId
            data["objectType"] = 0

        elif blogId:
            data["objectId"] = blogId
            data["objectType"] = 1

        elif wikiId:
            data["objectId"] = wikiId
            data["objectType"] = 2

        else: raise exceptions.SpecifyType

        if asGuest: flg = "g-flag"
        else: flg = "flag"

        response = self.session.post(f"{api}/g/s/{flg}", json=data)
        return response.status_code

    def check_values(self, *args):
        return any(arg is None for arg in args)

    def send_message(self, chatId: str, message: str = None, messageType: int = 0, file: BinaryIO = None, fileType: str = None, replyTo: str = None, mentionUserIds: list = None, stickerId: str = None, embedId: str = None, embedType: int = None, embedLink: str = None, embedTitle: str = None, embedContent: str = None, embedImage: BinaryIO = None):
        """
        Send a Message to a Chat.

        **Parameters**
            - **message** : Message to be sent
            - **chatId** : ID of the Chat.
            - **file** : File to be sent.
            - **fileType** : Type of the file.
                - ``audio``, ``image``, ``gif``
            - **messageType** : Type of the Message.
            - **mentionUserIds** : List of User IDS to mention. '@' needed in the Message.
            - **replyTo** : Message ID to reply to.
            - **stickerId** : Sticker ID to be sent.
            - **embedTitle** : Title of the Embed.
            - **embedContent** : Content of the Embed.
            - **embedLink** : Link of the Embed.
            - **embedImage** : Image of the Embed.
            - **embedId** : ID of the Embed.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        data = {
            "type": messageType,
            "content": message
        }
        
        if self.check_values(embedId, embedType, embedLink, embedTitle, embedContent, embedImage):
            attachedObject = dict()

            if embedId:
                attachedObject["objectId"] = embedId

            if embedType:
                attachedObject["objectType"] = embedType

            if embedLink:
                attachedObject["link"] = embedLink

            if embedTitle:
                attachedObject["title"] = embedTitle

            if embedContent:
                attachedObject["content"] = embedContent

            if embedImage:
                attachedObject["mediaList"] = [[100, upload_media(self, embedImage, "image"), None]]

            data["attachedObject"] = attachedObject
        
        if mentionUserIds:
            mentions = [{"uid": mention_uid} for mention_uid in mentionUserIds]
            data["extensions"] = {"mentionedArray": mentions}

        if replyTo: data["replyMessageId"] = replyTo

        if stickerId:
            data["content"] = None
            data["stickerId"] = stickerId
            data["type"] = 3

        if file:
            data["content"] = None
            if fileType == "audio":
                data["type"] = 2
                data["mediaType"] = 110

            elif fileType == "image":
                data["mediaType"] = 100
                data["mediaUploadValueContentType"] = "image/jpg"
                data["mediaUhqEnabled"] = True

            elif fileType == "gif":
                data["mediaType"] = 100
                data["mediaUploadValueContentType"] = "image/gif"
                data["mediaUhqEnabled"] = True

            else: raise exceptions.SpecifyType(fileType)

            data["mediaUploadValue"] = b64encode(file.read()).decode()

        response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/message", json=data)
        return response.status_code

    def delete_message(self, chatId: str, messageId: str, asStaff: bool = False, reason: str = None):
        """
        Delete a Message from a Chat.

        **Parameters**
            - **messageId** : ID of the Message.
            - **chatId** : ID of the Chat.
            - **asStaff** : If execute as a Staff member (Leader or Curator).
            - **reason** : Reason of the action to show on the Moderation History.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "adminOpName": 102,
        }

        if asStaff and reason:
            data["adminOpNote"] = {"content": reason}
        
        if not asStaff: response = self.session.delete(f"{api}/g/s/chat/thread/{chatId}/message/{messageId}")
        else: response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/message/{messageId}/admin", json=data)
        return response.status_code

    def mark_as_read(self, chatId: str, messageId: str):
        """
        Mark a Message from a Chat as Read.

        **Parameters**
            - **messageId** : ID of the Message.
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "messageId": messageId,
        }
        
        response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/mark-as-read", json=data)
        return response.status_code

    def edit_chat(self, chatId: str, doNotDisturb: bool = None, pinChat: bool = None, title: str = None, icon: str = None, backgroundImage: str = None, content: str = None, announcement: str = None, coHosts: list = None, keywords: list = None, pinAnnouncement: bool = None, publishToGlobal: bool = None, canTip: bool = None, viewOnly: bool = None, canInvite: bool = None, fansOnly: bool = None):
        """
        Send a Message to a Chat.

        **Parameters**
            - **chatId** : ID of the Chat.
            - **title** : Title of the Chat.
            - **content** : Content of the Chat.
            - **icon** : Icon of the Chat.
            - **backgroundImage** : Url of the Background Image of the Chat.
            - **announcement** : Announcement of the Chat.
            - **pinAnnouncement** : If the Chat Announcement should Pinned or not.
            - **coHosts** : List of User IDS to be Co-Host.
            - **keywords** : List of Keywords of the Chat.
            - **viewOnly** : If the Chat should be on View Only or not.
            - **canTip** : If the Chat should be Tippable or not.
            - **canInvite** : If the Chat should be Invitable or not.
            - **fansOnly** : If the Chat should be Fans Only or not.
            - **publishToGlobal** : If the Chat should show on Public Chats or not.
            - **doNotDisturb** : If the Chat should Do Not Disturb or not.
            - **pinChat** : If the Chat should Pinned or not.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = dict()

        if title: data["title"] = title
        if content: data["content"] = content
        if icon: data["icon"] = icon
        if keywords: data["keywords"] = keywords
        if announcement: data["extensions"] = {"announcement": announcement}
        if pinAnnouncement: data["extensions"] = {"pinAnnouncement": pinAnnouncement}
        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}

        if publishToGlobal: data["publishToGlobal"] = 0
        if not publishToGlobal: data["publishToGlobal"] = 1

        res = []

        if doNotDisturb != None:
            if doNotDisturb:
                data = {"alertOption": 2}
                
                response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/member/{self.profile.userId}/alert", json=data)
                res.append(response.status_code)

            if not doNotDisturb:
                data = {"alertOption": 1}
                
                response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/member/{self.profile.userId}/alert", json=data)
                res.append(response.status_code)

        if pinChat != None:
            if pinChat:
                response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/pin", json=data)
                res.append(response.status_code)

            if not pinChat:
                response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/unpin", json=data)
                res.append(response.status_code)

        if backgroundImage != None:
            data = {"media": [100, backgroundImage, None]}
            
            response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/member/{self.profile.userId}/background", json=data)
            res.append(response.status_code)

        if coHosts != None:
            data = {"uidList": coHosts}
            
            response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/co-host", data=data)
            res.append(response.status_code)
        
        if viewOnly != None:
            if viewOnly:
                
                response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/view-only/enable")
                res.append(response.status_code)

            if not viewOnly:
                
                response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/view-only/disable")
                res.append(response.status_code)

        if canInvite != None:
            if canInvite:
                
                response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/members-can-invite/enable", json=data)
                res.append(response.status_code)

            if not canInvite:
                
                response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/members-can-invite/disable", json=data)
                res.append(response.status_code)

        if canTip != None:
            if canTip:
                
                response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/tipping-perm-status/enable", json=data)
                res.append(response.status_code)

            if not canTip:
                
                response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/tipping-perm-status/disable", json=data)
                res.append(response.status_code)
        
        response = self.session.post(f"{api}/g/s/chat/thread/{chatId}", json=data)
        res.append(response.status_code)

        return res

    def send_coins(self, coins: int, blogId: str = None, chatId: str = None, objectId: str = None, transactionId: str = None):
        url = None
        if transactionId is None: transactionId = str(uuid4())

        data = {
            "coins": coins,
            "tippingContext": {"transactionId": transactionId},
        }

        if blogId != None: url = f"{api}/g/s/blog/{blogId}/tipping"
        if chatId != None: url = f"{api}/g/s/chat/thread/{chatId}/tipping"
        if objectId != None:
            data["objectId"] = objectId
            data["objectType"] = 2
            url = f"{api}/g/s/tipping"

        if url is None: raise exceptions.SpecifyType

        response = self.session.post(url, json=data)
        return response.status_code

    def follow(self, userId: Union[str, list]):
        """
        Follow an User or Multiple Users.

        **Parameters**
            - **userId** : ID of the User or List of IDs of the Users.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if isinstance(userId, str):
            response = self.session.post(f"{api}/g/s/user-profile/{userId}/member")

        elif isinstance(userId, list):
            data = {"targetUidList": userId}
            
            response = self.session.post(f"{api}/g/s/user-profile/{self.profile.userId}/joined", json=data)

        else: raise exceptions.WrongType

        return response.status_code

    def unfollow(self, userId: str):
        """
        Unfollow an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.delete(f"{api}/g/s/user-profile/{userId}/member/{self.profile.userId}")
        return response.status_code

    def block(self, userId: str):
        """
        Block an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.post(f"{api}/g/s/block/{userId}")
        return response.status_code

    def unblock(self, userId: str):
        """
        Unblock an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.delete(f"{api}/g/s/block/{userId}")
        return response.status_code

    def join_community(self, comId: int, invitationId: str = None):
        """
        Join a Community.

        **Parameters**
            - **comId** : ID of the Community.
            - **invitationId** : ID of the Invitation Code.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = dict()
        if invitationId: data["invitationId"] = invitationId

        response = self.session.post(f"{api}/x{comId}/s/community/join", json=data)
        return response.status_code

    def request_join_community(self, comId: int, message: str = None):
        """
        Request to join a Community.

        **Parameters**
            - **comId** : ID of the Community.
            - **message** : Message to be sent.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {"message": message}

        response = self.session.post(f"{api}/x{comId}/s/community/membership-request", jaon=data)
        return response.status_code

    def leave_community(self, comId: int):
        """
        Leave a Community.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.post(f"{api}/x{comId}/s/community/leave")
        return response.status_code

    def flag_community(self, comId: int, reason: str, flagType: int, isGuest: bool = False):
        """
        Flag a Community.

        **Parameters**
            - **comId** : ID of the Community.
            - **reason** : Reason of the Flag.
            - **flagType** : Type of Flag.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if reason is None: raise exceptions.ReasonNeeded
        if flagType is None: raise exceptions.FlagTypeNeeded

        data = {
            "objectId": comId,
            "objectType": 16,
            "flagType": flagType,
            "message": reason,
        }

        if isGuest: flg = "g-flag"
        else: flg = "flag"
        
        response = self.session.post(f"{api}/x{comId}/s/{flg}", json=data)
        return response.status_code

    def edit_profile(self, nickname: str = None, content: str = None, icon: BinaryIO = None, backgroundColor: str = None, backgroundImage: str = None, defaultBubbleId: str = None):
        """
        Edit account's Profile.

        **Parameters**
            - **nickname** : Nickname of the Profile.
            - **content** : Biography of the Profile.
            - **icon** : Icon of the Profile.
            - **backgroundImage** : Url of the Background Picture of the Profile.
            - **backgroundColor** : Hexadecimal Background Color of the Profile.
            - **defaultBubbleId** : Chat bubble ID.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "address": None,
            "latitude": 0,
            "longitude": 0,
            "mediaList": None,
            "eventSource": "UserProfileView",
        }

        if nickname: data["nickname"] = nickname
        if icon: data["icon"] = upload_media(self, icon, "image")
        if content: data["content"] = content
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if backgroundImage: data["extensions"] = {"style": {"backgroundMediaList": [[100, backgroundImage, None, None, None]]}}
        if defaultBubbleId: data["extensions"] = {"defaultBubbleId": defaultBubbleId}

        response = self.session.post(f"{api}/g/s/user-profile/{self.profile.userId}", json=data)
        return response.status_code

    def set_amino_id(self, aminoId: str):
        """
        Edit account's Amino ID.

        **Parameters**
            - **aminoId** : Amino ID of the Account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {"aminoId": aminoId}

        response = self.session.post(f"{api}/g/s/account/change-amino-id", json=data)
        return response.status_code

    def get_linked_communities(self, userId: str):
        """
        Get a List of Linked Communities of an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : :meth:`Community List <amino.lib.util.objects.CommunityList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/user-profile/{userId}/linked-community")
        return objects.CommunityList(response.json()["linkedCommunityList"]).CommunityList

    def get_unlinked_communities(self, userId: str):
        """
        Get a List of Unlinked Communities of an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : :meth:`Community List <amino.lib.util.objects.CommunityList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/user-profile/{userId}/linked-community")
        return objects.CommunityList(response.json()["unlinkedCommunityList"]).CommunityList

    def reorder_linked_communities(self, comIds: list):
        """
        Reorder List of Linked Communities.

        **Parameters**
            - **comIds** : IDS of the Communities.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {"ndcIds": comIds}

        response = self.session.post(f"{api}/g/s/user-profile/{self.profile.userId}/linked-community/reorder", json=data)
        return response.status_code

    def add_linked_community(self, comId: int):
        """
        Add a Linked Community on your profile.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.post(f"{api}/g/s/user-profile/{self.profile.userId}/linked-community/{comId}")
        return response.status_code

    def remove_linked_community(self, comId: int):
        """
        Remove a Linked Community on your profile.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.delete(f"{api}/g/s/user-profile/{self.profile.userId}/linked-community/{comId}")
        return response.status_code

    def comment(self, message: str, userId: str = None, blogId: str = None, wikiId: str = None, replyTo: str = None):
        """
        Comment on a User's Wall, Blog or Wiki.

        **Parameters**
            - **message** : Message to be sent.
            - **userId** : ID of the User. (for Walls)
            - **blogId** : ID of the Blog. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)
            - **replyTo** : ID of the Comment to Reply to.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if message is None: raise exceptions.MessageNeeded

        data = {
            "content": message,
            "stickerId": None,
            "type": 0,
        }

        if replyTo: data["respondTo"] = replyTo

        if userId:
            data["eventSource"] = "UserProfileView"
            
            url = f"{api}/g/s/user-profile/{userId}/g-comment"

        elif blogId:
            data["eventSource"] = "PostDetailView"
            
            url = f"{api}/g/s/blog/{blogId}/g-comment"

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            
            url = f"{api}/g/s/item/{wikiId}/g-comment"

        else: raise exceptions.SpecifyType

        response = self.session.post(url, json=data)
        return response.status_code

    def delete_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None):
        """
        Delete a Comment on a User's Wall, Blog or Wiki.

        **Parameters**
            - **commentId** : ID of the Comment.
            - **userId** : ID of the User. (for Walls)
            - **blogId** : ID of the Blog. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if userId: url = f"{api}/g/s/user-profile/{userId}/g-comment/{commentId}"
        elif blogId: url = f"{api}/g/s/blog/{blogId}/g-comment/{commentId}"
        elif wikiId: url = f"{api}/g/s/item/{wikiId}/g-comment/{commentId}"
        else: raise exceptions.SpecifyType

        response = self.session.delete(url)
        return response.status_code

    def like_blog(self, blogId: Union[str, list] = None, wikiId: str = None):
        """
        Like a Blog, Multiple Blogs or a Wiki.

        **Parameters**
            - **blogId** : ID of the Blog or List of IDs of the Blogs. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "value": 4,
        }

        if blogId:
            if isinstance(blogId, str):
                data["eventSource"] = "UserProfileView"
                
                url = f"{api}/g/s/blog/{blogId}/g-vote?cv=1.2"

            elif isinstance(blogId, list):
                data["targetIdList"] = blogId
                
                url = f"{api}/g/s/feed/g-vote"

            else: raise exceptions.WrongType(type(blogId))


        elif wikiId:
            data["eventSource"] = "PostDetailView"
            
            url = f"{api}/g/s/item/{wikiId}/g-vote?cv=1.2"

        else: raise exceptions.SpecifyType

        response = self.session.post(url, json=data)
        return response.status_code

    def unlike_blog(self, blogId: str = None, wikiId: str = None):
        """
        Remove a like from a Blog or Wiki.

        **Parameters**
            - **blogId** : ID of the Blog. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if blogId: url = f"{api}/g/s/blog/{blogId}/g-vote?eventSource=UserProfileView"
        elif wikiId: url = f"{api}/g/s/item/{wikiId}/g-vote?eventSource=PostDetailView"
        else: raise exceptions.SpecifyType
        
        response = self.session.delete(url)
        return response.status_code

    def like_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None):
        """
        Like a Comment on a User's Wall, Blog or Wiki.

        **Parameters**
            - **commentId** : ID of the Comment.
            - **userId** : ID of the User. (for Walls)
            - **blogId** : ID of the Blog. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "value": 4,
        }

        if userId:
            data["eventSource"] = "UserProfileView"
            
            url = f"{api}/g/s/user-profile/{userId}/comment/{commentId}/g-vote?cv=1.2&value=1"

        elif blogId:
            data["eventSource"] = "PostDetailView"
            
            url = f"{api}/g/s/blog/{blogId}/comment/{commentId}/g-vote?cv=1.2&value=1"

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            
            url = f"{api}/g/s/item/{wikiId}/comment/{commentId}/g-vote?cv=1.2&value=1"

        else: raise exceptions.SpecifyType

        response = self.session.post(url, json=data)
        return response.status_code

    def unlike_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None):
        """
        Remove a like from a Comment on a User's Wall, Blog or Wiki.

        **Parameters**
            - **commentId** : ID of the Comment.
            - **userId** : ID of the User. (for Walls)
            - **blogId** : ID of the Blog. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if userId: url = f"{api}/g/s/user-profile/{userId}/comment/{commentId}/g-vote?eventSource=UserProfileView"
        elif blogId: url = f"{api}/g/s/blog/{blogId}/comment/{commentId}/g-vote?eventSource=PostDetailView"
        elif wikiId: url = f"{api}/g/s/item/{wikiId}/comment/{commentId}/g-vote?eventSource=PostDetailView"
        else: raise exceptions.SpecifyType

        response = self.session.delete(url)
        return response.status_code

    def get_membership_info(self):
        """
        Get Information about your Amino+ Membership.

        **Parameters**
            - No parameters required.

        **Returns**
            - **Success** : :meth:`Membership Object <amino.lib.util.objects.Membership>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/membership?force=true")
        return objects.Membership(response.json()).Membership

    def get_ta_announcements(self, language: str = "en", start: int = 0, size: int = 25):
        """
        Get the list of Team Amino's Announcement Blogs.

        **Parameters**
            - **language** : Language of the Blogs.
                - ``en``, ``es``, ``pt``, ``ar``, ``ru``, ``fr``, ``de``
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Blogs List <amino.lib.util.objects.BlogList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        if language not in self.get_supported_languages(): raise exceptions.UnsupportedLanguage(language)
        response = self.session.get(f"{api}/g/s/announcement?language={language}&start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_wallet_info(self):
        """
        Get Information about the account's Wallet.

        **Parameters**
            - No parameters required.

        **Returns**
            - **Success** : :meth:`Wallet Object <amino.lib.util.objects.WalletInfo>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/wallet")
        return objects.WalletInfo(response.json()["wallet"]).WalletInfo

    def get_wallet_history(self, start: int = 0, size: int = 25):
        """
        Get the Wallet's History Information.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Wallet Object <amino.lib.util.objects.WalletInfo>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/wallet/coin/history?start={start}&size={size}")
        return objects.WalletHistory(response.json()["coinHistoryList"]).WalletHistory

    def get_from_deviceid(self, deviceId: str):
        """
        Get the User ID from an Device ID.

        **Parameters**
            - **deviceID** : ID of the Device.

        **Returns**
            - **Success** : :meth:`User ID <amino.lib.util.objects.UserProfile.userId>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/auid?deviceId={deviceId}")
        return response.json()["auid"]

    def get_from_code(self, code: str):
        """
        Get the Object Information from the Amino URL Code.

        **Parameters**
            - **code** : Code from the Amino URL.
                - ``http://aminoapps.com/p/EXAMPLE``, the ``code`` is 'EXAMPLE'.

        **Returns**
            - **Success** : :meth:`From Code Object <amino.lib.util.objects.FromCode>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/link-resolution?q={code}")
        return objects.FromCode(response.json()["linkInfoV2"]).FromCode

    def get_from_id(self, objectId: str, objectType: int, comId: int = None):
        """
        Get the Object Information from the Object ID and Type.

        **Parameters**
            - **objectID** : ID of the Object. User ID, Blog ID, etc.
            - **objectType** : Type of the Object.
            - *comId* : ID of the Community. Use if the Object is in a Community.

        **Returns**
            - **Success** : :meth:`From Code Object <amino.lib.util.objects.FromCode>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        data = {
            "objectId": objectId,
            "targetCode": 1,
            "objectType": objectType,
        }
        
        if comId: url = f"{api}/g/s-x{comId}/link-resolution"
        else: url = f"{api}/g/s/link-resolution"

        response = self.session.post(url, json=data)
        return objects.FromCode(response.json()["linkInfoV2"]).FromCode

    def get_supported_languages(self):
        """
        Get the List of Supported Languages by Amino.

        **Parameters**
            - No parameters required.

        **Returns**
            - **Success** : :meth:`List of Supported Languages <List>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/community-collection/supported-languages?start=0&size=100")
        return response.json()["supportedLanguages"]

    def claim_new_user_coupon(self):
        """
        Claim the New User Coupon available when a new account is created.

        **Parameters**
            - No parameters required.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.post(f"{api}/g/s/coupon/new-user-coupon/claim")
        return response.status_code

    def get_subscriptions(self, start: int = 0, size: int = 25):
        """
        Get Information about the account's Subscriptions.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`List <List>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/store/subscription?objectType=122&start={start}&size={size}")
        return response.json()["storeSubscriptionItemList"]

    def get_all_users(self, start: int = 0, size: int = 25):
        """
        Get list of users of Amino.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`User Profile Count List Object <amino.lib.util.objects.UserProfileCountList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/g/s/user-profile?type=recent&start={start}&size={size}")
        return objects.UserProfileCountList(response.json()).UserProfileCountList

    def accept_host(self, chatId: str, requestId: str):
        response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/transfer-organizer/{requestId}/accept")
        return response.status_code

    def accept_organizer(self, chatId: str, requestId: str):
        self.accept_host(chatId, requestId)

    # Contributed by 'https://github.com/LynxN1'
    def link_identify(self, code: str):
        response = self.session.get(f"{api}/g/s/community/link-identify?q=http%3A%2F%2Faminoapps.com%2Finvite%2F{code}")
        return response.json()

    def invite_to_vc(self, chatId: str, userId: str):
        """
        Invite a User to a Voice Chat

        **Parameters**
            - **chatId** - ID of the Chat
            - **userId** - ID of the User

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        data = {
            "uid": userId
        }

        response = self.session.post(f"{api}/g/s/chat/thread/{chatId}/vvchat-presenter/invite", json=data)
        return response.status_code

    def wallet_config(self, level: int):
        """
        Changes ads config

        **Parameters**
            - **level** - Level of the ads.
                - ``1``, ``2``

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        data = {
            "adsLevel": level,
        }

        response = self.session.post(f"{api}/g/s/wallet/ads/config", json=data)
        return response.status_code

    def purchase(self, objectId: str, isAutoRenew: bool = False):
        data = {
            "objectId": objectId,
            "objectType": 114,
            "v": 1,
            "paymentContext":
            {
                "discountStatus": 0,
                "isAutoRenew": isAutoRenew
            },
        }

        response = self.session.post(f"{api}/g/s/store/purchase", json=data)
        return response.status_code

    def get_public_communities(self, language: str = "en", size: int = 25):
        """
        Get public communites

        **Parameters**
            - **language** - Set up language

        **Returns**
            - **Success** : :meth:`Community List <amino.lib.util.objects.CommunityList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        response = self.session.get(f"{api}/g/s/topic/0/feed/community?language={language}&type=web-explore&categoryKey=recommendation&size={size}&pagingType=t")
        return objects.CommunityList(response.json()["communityList"]).CommunityList
