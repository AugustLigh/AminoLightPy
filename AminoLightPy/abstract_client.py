from .lib import objects
from .lib import exceptions

from uuid import uuid4

from base64 import b64encode
from typing import BinaryIO
from requests import Session
from .constants import upload_media

class AbstractClient():
    def __init__(self, session: Session, path: str = "/g"):
        """
        {self.path} or /g
        """
        self.path = path
        self.session = session

    def get_user_info(self, userId: str):
        """
        Information of an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : :meth:`User Object <AminoLightPy.lib.util.objects.UserProfile>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"{self.path}/s/user-profile/{userId}")
        return objects.UserProfile(response.json()["userProfile"]).UserProfile
    
    def get_chat_threads(self, start: int = 0, size: int = 25):
        """
        List of Chats the account is in.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Chat List <AminoLightPy.lib.util.objects.ThreadList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"{self.path}/s/chat/thread?type=joined-me&start={start}&size={size}")
        return objects.ThreadList(response.json()["threadList"]).ThreadList
    
    def get_chat_thread(self, chatId: str):
        """
        Get the Chat Object from an Chat ID.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : :meth:`Chat Object <AminoLightPy.lib.util.objects.Thread>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"{self.path}/s/chat/thread/{chatId}")
        return objects.Thread(response.json()["thread"]).Thread
    
    def get_chat_users(self, chatId: str, start: int = 0, size: int = 25):
        """
        List of users in a chat.

        **Parameters**
            - **chatId** (str): ID of the chat.
            - *start* (int, optional): The index from which to start the list. Defaults to 0.
            - *size* (int, optional): The size of the list. Defaults to 25.

        **Returns**
            - **Success** : :meth:`User List <AminoLightPy.lib.util.objects.UserProfileList>`
            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        params = {
            "start": start,
            "size": size,
            "type": "default",
            "cv": "1.2"
        }

        response = self.session.get(f"{self.path}/s/chat/thread/{chatId}/member", params=params)
        return objects.UserProfileList(response.json()["memberList"]).UserProfileList
    
    def join_chat(self, chatId: str):
        """
        Join an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.post(f"{self.path}/s/chat/thread/{chatId}/member/{self.session.headers['AUID']}")
        return response.status_code
    
    def leave_chat(self, chatId: str):
        """
        Leave an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.delete(f"{self.path}/s/chat/thread/{chatId}/member/{self.session.headers['AUID']}")
        return response.status_code
    
    def start_chat(self, userId: str | list, message: str = None,
            title: str = None, content: str = None,
            isGlobal: bool = False, publishToGlobal: bool = False):
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

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if isinstance(userId, (str, list, tuple)):
            userIds = list(userId)
        else:
            raise exceptions.WrongType

        data = {
            "title": title,
            "inviteeUids": userIds,
            "initialMessageContent": message,
            "content": content,
            "type": 2 if isGlobal else 0,
            "publishToGlobal": int(publishToGlobal)
        }

        if isGlobal: data["eventSource"] = "GlobalComposeMenu"
        
        response = self.session.post(f"{self.path}/s/chat/thread", json=data)
        return objects.Thread(response.json()["thread"]).Thread
    
    def invite_to_chat(self, userId: str | list, chatId: str):
        """
        Invite a User or List of Users to a Chat.

        **Parameters**
            - **userId** : ID of the User or List of User IDs.
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if not isinstance(userId, (str, list)):
            raise exceptions.WrongType

        userIds = list(userId) if isinstance(userId, str) else userId

        data = {"uids": userIds}

        response = self.session.post(f"{self.path}/s/chat/thread/{chatId}/member/invite", json=data)
        return response.status_code
    
    def kick(self, userId: str, chatId: str, allowRejoin: bool = True):
        """
        Kicks a user from a chat.

        **Parameters**
            - **userId** (str): ID of the user to be kicked.
            - **chatId** (str): ID of the chat from which the user is to be kicked.
            - *allowRejoin* (bool, optional): Whether the user is allowed to rejoin the chat. Defaults to True.

        **Returns**
            - **Success** : 200 (int)
            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """

        params = {"allowRejoin": int(allowRejoin)}

        return self.session.delete(
            url=f"{self.path}/s/chat/thread/{chatId}/member/{userId}",
            params=params
        ).status_code
    
    def get_chat_messages(self, chatId: str, size: int = 25, pageToken: str = None):
        """
        List of Messages from an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.
            - *size* : Size of the list.
            - *pageToken* : Next Page Token.

        **Returns**
            - **Success** : :meth:`Message List <AminoLightPy.lib.util.objects.MessageList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """

        if pageToken: url = f"{self.path}/s/chat/thread/{chatId}/message?v=2&pagingType=t&pageToken={pageToken}&size={size}"
        else: url = f"{self.path}/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}"

        return objects.GetMessages(self.session.get(url).json()).GetMessages
    
    def get_message_info(self, chatId: str, messageId: str):
        """
        Information of an Message from an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.
            - **message** : ID of the Message.

        **Returns**
            - **Success** : :meth:`Message Object <AminoLightPy.lib.util.objects.Message>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"{self.path}/s/chat/thread/{chatId}/message/{messageId}")
        return objects.Message(response.json()["message"]).Message
    
    def get_user_following(self, userId: str, start: int = 0, size: int = 25):
        """
        List of Users that the User is Following.

        **Parameters**
            - **userId** : ID of the User.
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`User List <AminoLightPy.lib.util.objects.UserProfileList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"{self.path}/s/user-profile/{userId}/joined?start={start}&size={size}")
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList
    
    def get_user_followers(self, userId: str, start: int = 0, size: int = 25):
        """
        List of Users that are Following the User.

        **Parameters**
            - **userId** : ID of the User.
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`User List <AminoLightPy.lib.util.objects.UserProfileList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"{self.path}/user-profile/{userId}/member?start={start}&size={size}")
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList
    
    def get_blocked_users(self, start: int = 0, size: int = 25):
        """
        List of Users that the User Blocked.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Users List <AminoLightPy.lib.util.objects.UserProfileList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"{self.path}/s/block?start={start}&size={size}")
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList
    
    def get_blog_info(self, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None):
        """
        Get information about a blog, wiki, quiz, or file.

        Parameters:
            blogId (str): ID of the blog.
            wikiId (str): ID of the wiki.
            quizId (str): ID of the quiz.
            fileId (str): ID of the file.

        Returns:
            object: Information about the blog, wiki, quiz, or file.
        """
        if blogId or quizId:
            blogId = quizId if quizId is not None else blogId
            response = self.session.get(f"{self.path}/s/blog/{blogId}")
            return objects.GetBlogInfo(response.json()).GetBlogInfo

        if wikiId:
            response = self.session.get(f"{self.path}/s/item/{wikiId}")
            return objects.GetWikiInfo(response.json()).GetWikiInfo

        if fileId:
            response = self.session.get(f"{self.path}/s/shared-folder/files/{fileId}")
            return objects.SharedFolderFile(response.json()["file"]).SharedFolderFile

        raise exceptions.SpecifyType()
    
    def get_blog_comments(self, blogId: str = None, wikiId: str = None, quizId: str = None,
            fileId: str = None, sorting: str = "newest", start: int = 0, size: int = 25):
        """
        Get comments from a blog, wiki, quiz, or file.

        Parameters:
            blogId (str): ID of the blog.
            wikiId (str): ID of the wiki.
            quizId (str): ID of the quiz.
            fileId (str): ID of the file.
            sorting (str): Sorting order of comments. Can be "newest", "oldest", or "top".
            start (int): Starting index of comments.
            size (int): Number of comments to fetch.

        Returns:
            CommentList: List of comments.
        """
        sorting_dict = {"newest": "newest", "oldest": "oldest", "top": "vote"}
        sorting = sorting_dict.get(sorting)
        if sorting is None:
            raise exceptions.WrongType(sorting)

        if blogId or quizId:
            blogId = quizId if not blogId else blogId
            url = f"{self.path}/s/blog/{blogId}/comment"
        elif wikiId:
            url = f"{self.path}/s/item/{wikiId}/comment"
        elif fileId:
            url = f"{self.path}/s/shared-folder/files/{fileId}/comment"
        else: raise exceptions.SpecifyType

        params = {"sort": sorting, "start": start, "size": size}
        response = self.session.get(url, params=params)
        return objects.CommentList(response.json()["commentList"]).CommentList
    
    def get_blocker_users(self, start: int = 0, size: int = 25):
        """
        List of Users that are Blocking the User.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`List of User IDs <None>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"{self.path}/s/block/full-list?start={start}&size={size}")
        return response.json()["blockerUidList"]
    
    def get_wall_comments(self, userId: str, sorting: str = "newest", start: int = 0, size: int = 25):
        """
        List of Wall Comments of an User.

        **Parameters**
            - **userId** : ID of the User.
            - **sorting** : Order of the Comments.
                - ``newest``, ``oldest``, ``top``
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Comments List <AminoLightPy.lib.util.objects.CommentList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        sorting_dict = {"newest": "newest", "oldest": "oldest", "top": "vote"}
        sorting = sorting_dict.get(sorting)
        if sorting is None:
            raise exceptions.WrongType(sorting)

        response = self.session.get(f"{self.path}/s/user-profile/{userId}/g-comment?sort={sorting}&start={start}&size={size}")
        return objects.CommentList(response.json()["commentList"]).CommentList
    
    def flag(self, reason: str, flagType: int,
            userId: str = None, blogId: str = None, wikiId: str = None,
            asGuest: bool = False):
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

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if not reason: raise exceptions.ReasonNeeded
        if not flagType: raise exceptions.FlagTypeNeeded

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

        return self.session.post(f"{self.path}/s/{flg}", json=data).status_code
    
    def _check_values(self, *args):
        return any(arg is None for arg in args)

    def send_message(self, chatId: str, message: str = None, messageType: int = 0,
                        file: BinaryIO = None, fileType: str = None, replyTo: str = None,
                        mentionUserIds: list = None, stickerId: str = None, embedId: str = None,
                        embedType: int = None, embedLink: str = None, embedTitle: str = None,
                        embedContent: str = None, embedImage: BinaryIO = None, linkSnippet: list[dict] = None):
        """
        Send a Message to a Chat.

        **Parameters**
            - **message** : Message to be sent
            - **chatId** : ID of the Chat.
            - **file** : File to be sent.
            - **fileType** : Type of the file.
                - It's deprecated
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

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """

        data = {
            "type": messageType,
            "content": message,
        }

        if not self._check_values(embedId, embedType, embedLink, embedTitle, embedContent, embedImage):
            attachedObject = {}

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
                attachedObject["mediaList"] = [[100, upload_media(self, embedImage), None]]

            data["attachedObject"] = attachedObject

            extensions = {}

        if mentionUserIds:
            mentions = [{"uid": mention_uid} for mention_uid in mentionUserIds]
            extensions = {"mentionedArray": mentions}

        if linkSnippet:
            # [{
            #     "link": embedLink,
            #     "mediaType": 100,
            #     "mediaUploadValue": b64encode(readEmbed).decode(),
            #     "mediaUploadValueContentType": embedImageType
            # }]
            extensions = {"linkSnippetList": linkSnippet}

        if extensions:
            data["extensions"] = extensions

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
                data["mediaUploadValue"] = b64encode(file.read()).decode()

            else:
                data["mediaValue"] = upload_media(self, file)

        response = self.session.post(
            url=f"{self.path}/s/chat/thread/{chatId}/message",
            json=data
        )

        return objects.Message(response.json()["message"]).Message
    
    def edit_chat(self, chatId: str, doNotDisturb: bool = None, pinChat: bool = None,
                title: str = None, icon: str = None, backgroundImage: str = None,
                content: str = None, announcement: str = None, coHosts: list = None,
                keywords: list = None, pinAnnouncement: bool = None, publishToGlobal: bool = None,
                canTip: bool = None, viewOnly: bool = None, canInvite: bool = None,
                fansOnly: bool = None):
        """
        Edit a Chat.

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
            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = self._prepare_data(title, content, icon, keywords, announcement, pinAnnouncement, fansOnly, publishToGlobal)
        res = []

        res.extend(self._set_do_not_disturb(chatId, doNotDisturb))
        res.extend(self._pin_chat(chatId, pinChat))
        res.extend(self._set_background_image(chatId, backgroundImage))
        res.extend(self._set_co_hosts(chatId, coHosts))
        res.extend(self._set_view_only(chatId, viewOnly))
        res.extend(self._set_can_invite(chatId, canInvite))
        res.extend(self._set_can_tip(chatId, canTip))

        response = self.session.post(f"/{self.path}/s/chat/thread/{chatId}", json=data)
        res.append(response.status_code)

        return res

    def _prepare_data(self, title, content, icon, keywords, announcement, pinAnnouncement, fansOnly, publishToGlobal):
        data = {}
        if title: data["title"] = title
        if content: data["content"] = content
        if icon: data["icon"] = upload_media(self, icon)
        if keywords: data["keywords"] = keywords
        extensions = {}
        if announcement: extensions["announcement"] = announcement
        if pinAnnouncement: extensions["pinAnnouncement"] = pinAnnouncement
        if fansOnly: extensions["fansOnly"] = fansOnly
        if extensions: data["extensions"] = extensions
        if publishToGlobal is not None:
            data["publishToGlobal"] = 0 if publishToGlobal else 1
        return data

    def _set_do_not_disturb(self, chatId, doNotDisturb):
        if doNotDisturb is None:
            return []
        alertOption = 2 if doNotDisturb else 1
        data = {"alertOption": alertOption}
        response = self.session.post(
            url=f"/{self.path}/s/chat/thread/{chatId}/member/{self.session.headers['AUID']}/alert",
            json=data
        )
        return [response.status_code]

    def _pin_chat(self, chatId, pinChat):
        if pinChat is None:
            return []
        url_suffix = "pin" if pinChat else "unpin"
        response = self.session.post(
            url=f"{self.path}/s/chat/thread/{chatId}/{url_suffix}",
            json={}
        )
        return [response.status_code]

    def _set_background_image(self, chatId, backgroundImage):
        if not backgroundImage:
            return []
        data = {"media": [100, upload_media(self, backgroundImage), None]}
        response = self.session.post(
            url=f"{self.path}/s/chat/thread/{chatId}/member/{self.session.headers['AUID']}/background",
            json=data
        )
        return [response.status_code]

    def _set_co_hosts(self, chatId, coHosts):
        if coHosts is None:
            return []
        data = {"uidList": coHosts}
        response = self.session.post(
            url=f"{self.path}/s/chat/thread/{chatId}/co-host",
            json=data
        )
        return [response.status_code]

    def _set_view_only(self, chatId, viewOnly):
        if viewOnly is None:
            return []
        url_suffix = "enable" if viewOnly else "disable"
        response = self.session.post(
            url=f"{self.path}/s/chat/thread/{chatId}/view-only/{url_suffix}"
        )
        return [response.status_code]

    def _set_can_invite(self, chatId, canInvite):
        if canInvite is None:
            return []
        url_suffix = "enable" if canInvite else "disable"
        response = self.session.post(
            url=f"{self.path}/s/chat/thread/{chatId}/members-can-invite/{url_suffix}",
            json={}
        )
        return [response.status_code]

    def _set_can_tip(self, chatId, canTip):
        if canTip is None:
            return []
        url_suffix = "enable" if canTip else "disable"
        response = self.session.post(
            url=f"{self.path}/s/chat/thread/{chatId}/tipping-perm-status/{url_suffix}",
            json={}
        )
        return [response.status_code]
    
    def send_coins(self, coins: int, blogId: str = None, chatId: str = None, objectId: str = None, transactionId: str = None):
        if not transactionId: transactionId = str(uuid4())

        data = {
            "coins": coins,
            "tippingContext": {"transactionId": transactionId}
        }

        if blogId: url = f"{self.path}/s/blog/{blogId}/tipping"
        elif chatId: url = f"{self.path}/s/chat/thread/{chatId}/tipping"
        elif objectId:
            data["objectId"] = objectId
            data["objectType"] = 2
            url = f"{self.path}/s/tipping"

        else: raise exceptions.SpecifyType

        return self.session.post(url, json=data).status_code
    
    def follow(self, userId: str | list):
        """
        Follow an User or Multiple Users.

        **Parameters**
            - **userId** : ID of the User or List of IDs of the Users.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if isinstance(userId, str):
            response = self.session.post(f"{self.path}/s/user-profile/{userId}/member")

        elif isinstance(userId, list):
            response = self.session.post(
                url=f"{self.path}/s/user-profile/{self.session.headers['AUID']}/joined",
                json={"targetUidList": userId}
            )

        else: raise exceptions.WrongType(type(userId))

        return response.status_code

    def unfollow(self, userId: str):
        """
        Unfollow an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.delete(f"{self.path}/s/user-profile/{self.session.headers['AUID']}/joined/{userId}")
        return response.status_code
    
    def block(self, userId: str):
        """
        Block an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        return self.session.post(f"{self.path}/s/block/{userId}").status_code

    def unblock(self, userId: str):
        """
        Unblock an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        return self.session.delete(f"{self.path}/s/block/{userId}").status_code
    
    def edit_profile(self, nickname: str = None, content: str = None, icon: BinaryIO = None,
                            chatRequestPrivilege: str = None, imageList: list = None,
                            captionList: list = None, backgroundImage: str = None,
                            backgroundColor: str = None, titles: list = None, colors: list = None,
                            defaultBubbleId: str = None):
        mediaList = []
        data = {}
        if captionList:
            for image, caption in zip(imageList, captionList):
                mediaList.append([100, upload_media(self, image), caption])

        else:
            if imageList:
                for image in imageList:
                    mediaList.append([100, upload_media(self, image), None])

        if imageList or captionList: data["mediaList"] = mediaList

        if nickname: data["nickname"] = nickname
        if icon: data["icon"] = upload_media(self, icon)
        if content: data["content"] = content

        if chatRequestPrivilege: data["extensions"] = {"privilegeOfChatInviteRequest": chatRequestPrivilege}
        if backgroundImage:
            data["extensions"] = {"style": {
                "backgroundMediaList": [[100, backgroundImage, None, None, None]]
                }}
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if defaultBubbleId: data["extensions"] = {"defaultBubbleId": defaultBubbleId}

        if titles or colors:
            tlt = []
            for titles, colors in zip(titles, colors):
                tlt.append({"title": titles, "color": colors})

            data["extensions"] = {"customTitles": tlt}

        return self.session.post(
            url=f"{self.path}/s/user-profile/{self.profile.userId}",
            json=data
        ).status_code
    
    def comment(self, message: str, userId: str = None, blogId: str = None, wikiId: str = None,
                replyTo: str = None, isGuest: bool = False, image: BinaryIO = None):
        data = {
            "content": message,
            "stickerId": None,
            "type": 0
        }
        if image:
            data["mediaList"] = [[100, upload_media(self, image), None]]

        if replyTo: data["respondTo"] = replyTo

        comType = "g-comment" if isGuest else "comment"

        if userId:
            data["eventSource"] = "UserProfileView"
            url = f"{self.path}/s/user-profile/{userId}/{comType}"

        elif blogId:
            data["eventSource"] = "PostDetailView"
            url = f"{self.path}/s/blog/{blogId}/{comType}"

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            url = f"{self.path}/s/item/{wikiId}/{comType}"

        else: raise exceptions.SpecifyType

        return self.session.post(url, json=data).status_code

    def delete_comment(self, commentId: str, userId: str = None, blogId: str = None,
                        wikiId: str = None):
        if userId:
            url = f"{self.path}/s/user-profile/{userId}/comment/{commentId}"
        elif blogId:
            url = f"{self.path}/s/blog/{blogId}/comment/{commentId}"
        elif wikiId:
            url = f"{self.path}/s/item/{wikiId}/comment/{commentId}"
        else:
            raise exceptions.SpecifyType

        return self.session.delete(url).status_code
    
    def like_blog(self, blogId: str | list = None, wikiId: str = None):
        """
        Like a Blog, Multiple Blogs or a Wiki.

        **Parameters**
            - **blogId** : ID of the Blog or List of IDs of the Blogs. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "value": 4,
        }

        if blogId:
            if isinstance(blogId, str):
                data["eventSource"] = "UserProfileView"
                url = f"{self.path}/s/blog/{blogId}/g-vote?cv=1.2"

            elif isinstance(blogId, list):
                data["targetIdList"] = blogId
                url = f"{self.path}/s/feed/g-vote"

            else: raise exceptions.WrongType(type(blogId))

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            url = f"{self.path}/s/item/{wikiId}/g-vote?cv=1.2"

        else: raise exceptions.SpecifyType

        return self.session.post(url, json=data).status_code

    def unlike_blog(self, blogId: str = None, wikiId: str = None):
        """
        Remove a like from a Blog or Wiki.

        **Parameters**
            - **blogId** : ID of the Blog. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if blogId:
            url = f"{self.path}/s/blog/{blogId}/g-vote?eventSource=UserProfileView"
        elif wikiId:
            url = f"{self.path}/s/item/{wikiId}/g-vote?eventSource=PostDetailView"
        else: raise exceptions.SpecifyType

        return self.session.delete(url).status_code

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

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "value": 4,
        }

        if userId:
            data["eventSource"] = "UserProfileView"
            url = f"{self.path}/s/user-profile/{userId}/comment/{commentId}/g-vote?cv=1.2&value=1"

        elif blogId:
            data["eventSource"] = "PostDetailView"
            url = f"{self.path}/s/blog/{blogId}/comment/{commentId}/g-vote?cv=1.2&value=1"

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            url = f"{self.path}/s/item/{wikiId}/comment/{commentId}/g-vote?cv=1.2&value=1"

        else: raise exceptions.SpecifyType

        return self.session.post(url, json=data).status_code

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

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if userId:
            url = f"{self.path}/s/user-profile/{userId}/comment/{commentId}/g-vote?eventSource=UserProfileView"
        elif blogId:
            url = f"{self.path}/s/blog/{blogId}/comment/{commentId}/g-vote?eventSource=PostDetailView"
        elif wikiId:
            url = f"{self.path}/s/item/{wikiId}/comment/{commentId}/g-vote?eventSource=PostDetailView"
        else:
            raise exceptions.SpecifyType

        return self.session.delete(url).status_code
    
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

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {"adminOpName": 102}

        if asStaff and reason:
            data["adminOpNote"] = {"content": reason}

        if asStaff:
            response = self.session.post(f"{self.path}/s/chat/thread/{chatId}/message/{messageId}/admin", json=data)
        else:
            response = self.session.delete(f"{self.path}/s/chat/thread/{chatId}/message/{messageId}")

        return response.status_code
    
    def mark_as_read(self, chatId: str, messageId: str):
        """
        Mark a Message from a Chat as Read.

        **Parameters**
            - **messageId** : ID of the Message.
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {"messageId": messageId}

        return self.session.post(f"{self.path}/s/chat/thread/{chatId}/mark-as-read", json=data).status_code
    
    def get_all_users(self, type: str = "recent", start: int = 0, size: int = 25):
        """
        Get list of users of Amino.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`User Profile Count List Object <AminoLightPy.lib.util.objects.UserProfileCountList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        types = ("recent", "banned", "featured", "leaders", "curators", "online")

        if type not in types:
            raise exceptions.WrongType(type)

        response = self.session.get(f"{self.path}/s/user-profile?type={type}&start={start}&size={size}")
        return objects.UserProfileCountList(response.json()).UserProfileCountList
    
    def accept_host(self, chatId: str, requestId: str):
        """
        Accepts a host request for a chat.

        **Parameters**
            - **chatId** (str): ID of the chat.
            - **requestId** (str): ID of the host request.

        **Returns**
            - **Success** : 200 (int)
            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        return self.session.post(
                url=f"{self.path}/s/chat/thread/{chatId}/transfer-organizer/{requestId}/accept"
            ).status_code

    def accept_organizer(self, chatId: str, requestId: str):
        """
        Accepts a host request for a chat.

        **Parameters**
            - **chatId** (str): ID of the chat.
            - **requestId** (str): ID of the host request.

        **Returns**
            - **Success** : 200 (int)
            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        return self.accept_host(chatId, requestId)
    
    def transfer_host(self, chatId: str, userIds: list):
        return self.session.post(
            url=f"{self.path}/s/chat/thread/{chatId}/transfer-organizer",
            json={"uidList": userIds}
        ).status_code

    def transfer_organizer(self, chatId: str, userIds: list):
        self.transfer_host(chatId, userIds)

    def delete_chat(self, chatId: str):
        """
        Delete a Chat.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        return self.session.delete(f"{self.path}/s/chat/thread/{chatId}").status_code
    
    def invite_to_vc(self, chatId: str, userId: str):
        """
        Invite a User to a Voice Chat

        **Parameters**
            - **chatId** - ID of the Chat
            - **userId** - ID of the User

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """

        data = {"uid": userId}

        response = self.session.post(f"{self.path}/s/chat/thread/{chatId}/vvchat-presenter/invite/", json=data)
        return response.status_code
    
    # Provided by "spectrum#4691"
    def purchase(self, objectId: str, objectType: int, aminoPlus: bool = True, autoRenew: bool = False):
        """
        Makes a purchase in the store.

        **Parameters**
            - **objectId** (str): ID of the object to be purchased.
            - *isAutoRenew* (bool, optional): Whether the purchase should be auto-renewed. Defaults to False.

        **Returns**
            - **Success** : 200 (int)
            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "objectId": objectId,
            "objectType": objectType,
            "v": 1,
        }

        data["paymentContext"] = {"discountStatus": int(aminoPlus), "discountValue": 1, "isAutoRenew": autoRenew}

        return self.session.post(f"{self.path}/s/store/purchase", json=data).status_code