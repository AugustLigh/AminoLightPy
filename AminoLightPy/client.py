# pylint: disable=invalid-name
# pylint: disable=too-many-lines
from json import dumps
from time import time
from .managers import Typing, Recording, CacheManager

from .constants import api, AminoSession
from .abstract_client import AbstractClient
from .amino_socket import Callbacks, SocketHandler, SocketRequests
from .lib import exceptions, objects, helpers, self_deviceId

#@dorthegra/IDörthe#8835 thanks for support!

class Client(Callbacks, SocketHandler, SocketRequests, AbstractClient):
    "Module for work with global"
    def __init__(self, proxies: dict = None, socketDebugging = False, socket_enabled = True):
        self.api = api
        self.authenticated = False
        self.session = AminoSession()
        self.session.verify = False
        self.device_id = self.session.headers["NDCDEVICEID"]

        self.socket_enabled = socket_enabled
        AbstractClient.__init__(self, self.session)
        if socket_enabled:
            SocketHandler.__init__(self, self, socketDebugging)
            SocketRequests.__init__(self, self)
            Callbacks.__init__(self)

        self.session.proxies = proxies

        self.cache_manager = CacheManager()

        self.sid = None
        self.profile = objects.UserProfile(None).UserProfile
        self.profile.session = self.session


    def parse_headers(self, data: str = None) -> dict:
        """
        **Returns**
            - Headers. For support old custom requests
        """
        base_headers: dict = self.session.headers
        if data:
            if not isinstance(data, str):
                data = dumps(data)
            base_headers["NDC-MSG-SIG"] = helpers.signature(data)

        return base_headers


    def login_sid(self, SID: str):
        """
        Login into an account with an SID

        **Parameters**
            - **SID** : SID of the account
        """
        userId = helpers.sid_to_uid(SID)
        self.sid = SID

        self.profile = objects.UserProfile({"uid": userId}).UserProfile

        self.session.headers.update({
            "NDCAUTH": f"sid={SID}",
            "AUID": userId
            })

        self.profile.session = self.session

        if self.socket_enabled and not self.authenticated:
            self.run_amino_socket()

        self.authenticated = True

    def login(self, login: str, password: str, self_device: bool = True):
        if not self.cache_manager.sid_exists(login):
            if login[0] == "+":
                login_data = self.login_phone(login, password, self_device)
            else:
                login_data = self.login_email(login, password, self_device)

            self.cache_manager.save_sid(login, login_data["sid"])

            return login_data

        else:
            sid_file = self.cache_manager.get_sid(login)

            if time() - sid_file["time"] > 86400:
                self.cache_manager.remove_sid(login)
                return self.login(login, password, self_device)
            
            self.session.headers["NDCDEVICEID"] = self_deviceId(login)
            self.login_sid(sid_file["sid"])

            return sid_file["sid"]


    def login_email(self, email: str, password: str, self_device: bool = True):
        """
        Login into an account.

        **Parameters**
            - **email** : Email of the account.
            - **password** : Password of the account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if self_device:
            self.session.headers["NDCDEVICEID"] = self_deviceId(email)
            

        data = {
            "email": email,
            "secret": f"0 {password}",
            "clientType": 100,
            "deviceID": self.session.headers["NDCDEVICEID"],
            "v": 2,
        }

        response = self.session.post("/g/s/auth/login", json=data)
        json = response.json()
        self.sid = json["sid"]
        self.profile = objects.UserProfile(json["userProfile"]).UserProfile

        self.session.headers.update({
            "NDCAUTH": f"sid={self.sid}",
            "AUID": self.profile.userId
        })

        self.profile.session = self.session

        if self.socket_enabled and not self.authenticated:
            self.run_amino_socket()

        self.authenticated = True

        return json

    def login_phone(self, phoneNumber: str, password: str, self_device: bool = True):
        """
        Login into an account.

        **Parameters**
            - **phoneNumber** : Phone number of the account.
            - **password** : Password of the account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if self_device:
            self.session.headers["NDCDEVICEID"] = self_deviceId(phoneNumber)

        data = {
            "phoneNumber": phoneNumber,
            "v": 2,
            "secret": f"0 {password}",
            "deviceID": self.session.headers["NDCDEVICEID"],
            "clientType": 100,
            "action": "normal",
        }

        response = self.session.post("/g/s/auth/login", json=data)
        self.authenticated = True
        json = response.json()
        self.sid = json["sid"]

        self.profile = objects.UserProfile(json["userProfile"]).UserProfile

        self.session.headers.update({
            "NDCAUTH": f"sid={self.sid}",
            "AUID": self.profile.userId
        })

        self.profile.session = self.session

        if self.socket_enabled and not self.authenticated:
            self.run_amino_socket()

        self.authenticated = True

        return json

    def login_secret(self, secret: str, self_device: bool = True):
        """
        Login into an account.

        **Parameters**
            - **secret** : Secret of the account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if self_device:
            self.session.headers["NDCDEVICEID"] = self_deviceId(secret)

        data = {
            "v": 2,
            "secret": secret,
            "deviceID": self.session.headers["NDCDEVICEID"],
            "clientType": 100,
            "action": "normal",
        }

        response = self.session.post("/g/s/auth/login", json=data)
        json = response.json()
        self.sid = json["sid"]

        self.profile = objects.UserProfile(json["userProfile"]).UserProfile

        self.session.headers.update({
            "NDCAUTH": f"sid={self.sid}",
            "AUID": self.profile.userId
        })

        self.profile.session = self.session

        if self.socket_enabled and not self.authenticated:
            self.run_amino_socket()

        self.authenticated = True

        return json

    def register(self, nickname: str, email: str, password: str, verificationCode: str):
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

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """

        data = {
            "secret": f"0 {password}",
            "deviceID": self.device_id,
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
            "identity": email}     

        response = self.session.post("/g/s/auth/register", json=data)
        return response.json()

    def restore(self, email: str, password: str):
        """
        Restore a deleted account.

        **Parameters**
            - **email** : Email of the account.
            - **password** : Password of the account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "secret": f"0 {password}",
            "deviceID": self.device_id,
            "email": email
        }

        response = self.session.post("/g/s/account/delete-request/cancel", json=data)
        return response.status_code

    def logout(self):
        """
        Logout from an account.

        **Parameters**
            - No parameters required.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "deviceID": self.device_id,
            "clientType": 100
        }

        response = self.session.post("/g/s/auth/logout", json=data)
        self.authenticated = False
        self.sid = None
        self.profile = None
        self.session.headers.update({
            "NDCAUTH": None,
            "AUID": None
        })

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

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        gender_mapping = {"male": 1, "female": 2, "non-binary": 255}

        gender = gender.lower()
        if gender not in gender_mapping:
            raise exceptions.SpecifyType

        age = max(13, age)

        data = {
            "age": age,
            "gender": gender_mapping[gender],
        }

        response = self.session.post("/g/s/persona/profile/basic", json=data)
        return response.status_code

    def verify(self, email: str, code: str):
        """
        Verify an account.

        **Parameters**
            - **email** : Email of the account.
            - **code** : Verification code.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "validationContext": {
                "type": 1,
                "identity": email,
                "data": {"code": code}},
            "deviceID": self.device_id,
        }

        response = self.session.post("/g/s/auth/check-security-validation", json=data)
        return response.status_code

    def request_verify_code(self, email: str, resetPassword: bool = False):
        """
        Request an verification code to the targeted email.

        **Parameters**
            - **email** : Email of the account.
            - **resetPassword** : If the code should be for Password Reset.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "identity": email,
            "type": 1,
            "deviceID": self.device_id
        }

        if resetPassword is True:
            data["level"] = 2
            data["purpose"] = "reset-password"

        response = self.session.post("/g/s/auth/request-security-validation", json=data)
        return response.status_code

    def activate_account(self, email: str, code: str):
        """
        Activate an account.

        **Parameters**
            - **email** : Email of the account.
            - **code** : Verification code.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """

        data = {
            "type": 1,
            "identity": email,
            "data": {"code": code},
            "deviceID": self.device_id
        }

        response = self.session.post("/g/s/auth/activate-email", json=data)
        return response.status_code

    # Provided by "𝑰 𝑵 𝑻 𝑬 𝑹 𝑳 𝑼 𝑫 𝑬#4082"
    def delete_account(self, password: str):
        """
        Delete an account.

        **Parameters**
            - **password** : Password of the account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """

        data = {
            "deviceID": self.device_id,
            "secret": f"0 {password}"
        }

        response = self.session.post("/g/s/account/delete-request", json=data)
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

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
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
                "deviceID": self.device_id
            },
            "phoneNumberValidationContext": None,
            "deviceID": self.device_id
        }

        response = self.session.post("/g/s/auth/reset-password", json=data)
        return response.status_code


    def get_account_info(self):
        """
        Information of an this account.

        **Returns**
            - **Success** : :meth:`User Object <AminoLightPy.lib.util.objects.UserProfile>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get("/g/s/account")
        return objects.UserProfile(response.json()["account"]).UserProfile

    def handle_socket_message(self, data):
        "Adapter between receiving messages and processing them"
        return self.resolve(data)

    def get_eventlog(self):
        """
        Information of an events.

        **Returns**
            - **Success** : :meth:`dict`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        params = {"language": "en"}
        response = self.session.get("/g/s/eventlog/profile", params=params)
        return response.json()

    def sub_clients(self, start: int = 0, size: int = 25):
        """
        List of Communities the account is in.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Community List <AminoLightPy.lib.util.objects.CommunityList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if not self.authenticated:
            raise exceptions.NotLoggedIn
        response = self.session.get(f"/g/s/community/joined?v=1&start={start}&size={size}")
        return objects.CommunityList(response.json()["communityList"]).CommunityList

    def sub_clients_profile(self, start: int = 0, size: int = 25):
        """
        List of profiles in communities.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`list<dict>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if not self.authenticated:
            raise exceptions.NotLoggedIn
        response = self.session.get(f"/g/s/community/joined?v=1&start={start}&size={size}")
        return response.json()["userInfoInCommunities"]

    def get_community_info(self, comId: int):
        """
        Information of an Community.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **Success** : :meth:`Community Object <AminoLightPy.lib.util.objects.Community>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"/g/s-x{comId}/community/info?withInfluencerList=1&withTopicList=true&influencerListOrderStrategy=fansCount")
        return objects.Community(response.json()["community"]).Community

    def search_community(self, aminoId: str):
        """
        Search a Community byt its Amino ID.

        **Parameters**
            - **aminoId** : Amino ID of the Community.

        **Returns**
            - **Success** : :meth:`Community List <AminoLightPy.lib.util.objects.CommunityList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"/g/s/search/amino-id-and-link?q={aminoId}")
        result = response.json()["resultList"]
        if not result:
            raise exceptions.CommunityNotFound(aminoId)
        return objects.CommunityList([com["refObject"] for com in result]).CommunityList

    def join_community(self, comId: int, invitationId: str = None):
        """
        Join a Community.

        **Parameters**
            - **comId** : ID of the Community.
            - **invitationId** : ID of the Invitation Code.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {}
        if invitationId:
            data["invitationId"] = invitationId

        response = self.session.post(f"/x{comId}/s/community/join", json=data)
        return response.status_code

    def request_join_community(self, comId: int, message: str = None):
        """
        Request to join a Community.

        **Parameters**
            - **comId** : ID of the Community.
            - **message** : Message to be sent.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {"message": message}

        response = self.session.post(f"/x{comId}/s/community/membership-request", jaon=data)
        return response.status_code

    def leave_community(self, comId: int):
        """
        Leave a Community.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.post(f"/x{comId}/s/community/leave")
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

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if not reason:
            raise exceptions.ReasonNeeded
        if not flagType:
            raise exceptions.FlagTypeNeeded

        data = {
            "objectId": comId,
            "objectType": 16,
            "flagType": flagType,
            "message": reason,
        }

        if isGuest:
            flg = "g-flag"
        else:
            flg = "flag"
        response = self.session.post(f"/x{comId}/s/{flg}", json=data)
        return response.status_code

    def set_amino_id(self, aminoId: str):
        """
        Edit account's Amino ID.

        **Parameters**
            - **aminoId** : Amino ID of the Account.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {"aminoId": aminoId}

        response = self.session.post("/g/s/account/change-amino-id", json=data)
        return response.status_code

    def get_linked_communities(self, userId: str):
        """
        Get a List of Linked Communities of an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : :meth:`Community List <AminoLightPy.lib.util.objects.CommunityList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"/g/s/user-profile/{userId}/linked-community")
        return objects.CommunityList(response.json()["linkedCommunityList"]).CommunityList

    def get_unlinked_communities(self, userId: str):
        """
        Get a List of Unlinked Communities of an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : :meth:`Community List <AminoLightPy.lib.util.objects.CommunityList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"/g/s/user-profile/{userId}/linked-community")
        return objects.CommunityList(response.json()["unlinkedCommunityList"]).CommunityList

    def reorder_linked_communities(self, comIds: list):
        """
        Reorder List of Linked Communities.

        **Parameters**
            - **comIds** : IDS of the Communities.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {"ndcIds": comIds}
        userId = self.session.headers["AUID"]
        return self.session.post(
            url=f"/g/s/user-profile/{userId}/linked-community/reorder",
            json=data
        ).status_code

    def add_linked_community(self, comId: int):
        """
        Add a Linked Community on your profile.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        userId = self.session.headers["AUID"]
        return self.session.post(
            url=f"/g/s/user-profile/{userId}/linked-community/{comId}"
        ).status_code


    def remove_linked_community(self, comId: int):
        """
        Remove a Linked Community on your profile.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        userId = self.session.headers["AUID"]
        return self.session.delete(
            url=f"/g/s/user-profile/{userId}/linked-community/{comId}"
        ).status_code


    def get_membership_info(self):
        """
        Get Information about your Amino+ Membership.

        **Parameters**
            - No parameters required.

        **Returns**
            - **Success** : :meth:`Membership Object <AminoLightPy.lib.util.objects.Membership>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get("/g/s/membership?force=true")
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
            - **Success** : :meth:`Blogs List <AminoLightPy.lib.util.objects.BlogList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if language not in self.get_supported_languages():
            raise exceptions.UnsupportedLanguage(language)
        params = {
            "language": language,
            "start": start,
            "size": size
        }
        response = self.session.get("/g/s/announcement", params=params)
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_wallet_info(self):
        """
        Get Information about the account's Wallet.

        **Parameters**
            - No parameters required.

        **Returns**
            - **Success** : :meth:`Wallet Object <AminoLightPy.lib.util.objects.WalletInfo>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get("/g/s/wallet")
        return objects.WalletInfo(response.json()["wallet"]).WalletInfo

    def get_wallet_history(self, start: int = 0, size: int = 25):
        """
        Get the Wallet's History Information.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Wallet Object <AminoLightPy.lib.util.objects.WalletInfo>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"/g/s/wallet/coin/history?start={start}&size={size}")
        return objects.WalletHistory(response.json()["coinHistoryList"]).WalletHistory

    def get_from_deviceid(self, deviceId: str):
        """
        Get the User ID from an Device ID.

        **Parameters**
            - **deviceID** : ID of the Device.

        **Returns**
            - **Success** : :meth:`User ID <AminoLightPy.lib.util.objects.UserProfile.userId>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"/g/s/auid?deviceId={deviceId}")
        return response.json()["auid"]

    def get_from_code(self, code: str):
        """
        Get the Object Information from the Amino URL Code.

        **Parameters**
            - **code** : Code from the Amino URL.
                - ``http://aminoapps.com/p/EXAMPLE``, the ``code`` is 'EXAMPLE'.

        **Returns**
            - **Success** : :meth:`From Code Object <AminoLightPy.lib.util.objects.FromCode>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"/g/s/link-resolution?q={code}")
        return objects.FromCode(response.json()["linkInfoV2"]).FromCode

    def get_from_id(self, objectId: str, objectType: int, comId: int = None):
        """
        Get the Object Information from the Object ID and Type.

        **Parameters**
            - **objectID** : ID of the Object. User ID, Blog ID, etc.
            - **objectType** : Type of the Object.
            - *comId* : ID of the Community. Use if the Object is in a Community.

        **Returns**
            - **Success** : :meth:`From Code Object <AminoLightPy.lib.util.objects.FromCode>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "objectId": objectId,
            "targetCode": 1,
            "objectType": objectType,
        }
        if comId:
            url = f"/g/s-x{comId}/link-resolution"
        else:
            url = "/g/s/link-resolution"

        response = self.session.post(url, json=data)
        return objects.FromCode(response.json()["linkInfoV2"]).FromCode

    def get_supported_languages(self):
        """
        Get the List of Supported Languages by Amino.

        **Parameters**
            - No parameters required.

        **Returns**
            - **Success** : :meth:`List of Supported Languages <List>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get("/g/s/community-collection/supported-languages")
        return response.json()["supportedLanguages"]
    
    def create_sticker_pack(self, name: str, description: str, image_list: list):
        data = {
            "description": description,
            "collectionType":3,
            "stickerList":image_list,
            "name":name,
            "iconSourceStickerIndex":0
        }

        return self.session.post("/g/s/sticker-collection", json=data)

    def claim_new_user_coupon(self):
        """
        Claim the New User Coupon available when a new account is created.

        **Parameters**
            - No parameters required.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        return self.session.post("/g/s/coupon/new-user-coupon/claim").status_code

    def get_subscriptions(self, start: int = 0, size: int = 25, objectType: int = 122):
        """
        Get Information about the account's Subscriptions.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`List <List>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"/g/s/store/subscription?objectType={objectType}&start={start}&size={size}")
        return response.json()["storeSubscriptionItemList"]


    # Contributed by 'https://github.com/LynxN1'
    def link_identify(self, code: str):
        """
        Identifies a community link.

        **Parameters**
            - **code** (str): The code of the community link.

        **Returns**
            - **Success** : A JSON object with the community link information.
            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"/g/s/community/link-identify?q=http%3A%2F%2Faminoapps.com%2Finvite%2F{code}")
        return response.json()

    def wallet_config(self, level: int):
        """
        Changes ads config

        **Parameters**
            - **level** - Level of the ads.
                - ``1``, ``2``

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """

        data = {
            "adsLevel": level,
        }

        response = self.session.post("/g/s/wallet/ads/config", json=data)
        return response.status_code

    def get_public_communities(self, language: str = "en", size: int = 25):
        """
        Get public communites

        **Parameters**
            - **language** - Set up language

        **Returns**
            - **Success** : :meth:`Community List <AminoLightPy.lib.util.objects.CommunityList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        params = {
            "language": language,
            "type": "web-explore",
            "categoryKey": "recommendation",
            "size": size,
            "pagingType": "t"
        }

        response = self.session.get("/g/s/topic/0/feed/community", params=params)
        return objects.CommunityList(response.json()["communityList"]).CommunityList

    def get_blockers(self) -> list[str]:
        """
        Get ids of user ho block you.

        **Returns**
            - **Success** : :meth:`List <str>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get("/g/s/block/full-list")
        return response.json()["blockerUidList"]

    def set_privacy_status(self, isAnonymous: bool = False, getNotifications: bool = False):
        """
        Allow or disable global notification.

        **Returns**
            - **Success** : :meth:`List <str>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "privacyMode": 2 if isAnonymous else 1
        }
        if not getNotifications:
            data["notificationStatus"] = 2
        else:
            data["privacyMode"] = 1

        response = self.session.post("/g/s/account/visit-settings", json=data)
        return response.json()

    def typing(self, chatId: str, comId: int = None) -> Typing:
        """
        Start typing message in context manager.

        **Returns**
            - **Success** : :meth:`class <Typing>`
        """
        return Typing(self, chatId=chatId, comId=comId)

    def recording(self, chatId: str, comId: int = None) -> Recording:
        """
        Start recording in context manager.

        **Returns**
            - **Success** : :meth:`class <Recording>`
        """
        return Recording(self, chatId=chatId, comId=comId)
