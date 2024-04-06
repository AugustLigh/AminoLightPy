from uuid import uuid4
from time import timezone
from requests import Session
from base64 import b64encode
from typing import BinaryIO, Union

from .constants import api, upload_media
from .lib.util import exceptions, objects


class SubClient():
    def __init__(self, comId: int = None, *, profile: objects.UserProfile):
        self.vc_connect = False
        self.profile = profile
        self.session: Session = self.profile.session

        self.comId = comId

    def get_invite_codes(self, status: str = "normal", start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/g/s-x{self.comId}/community/invitation?status={status}&start={start}&size={size}")
        return objects.InviteCodeList(response.json()["communityInvitationList"]).InviteCodeList

    def generate_invite_code(self, duration: int = 0, force: bool = True):
        data = {
            "duration": duration,
            "force": force
        }
        
        response = self.session.post(f"{api}/g/s-x{self.comId}/community/invitation", json=data)
        return objects.InviteCode(response.json()["communityInvitation"]).InviteCode

    def delete_invite_code(self, inviteId: str):
        response = self.session.delete(f"{api}/g/s-x{self.comId}/community/invitation/{inviteId}")
        return response.status_code

    def post_blog(self, title: str, content: str, imageList: list = None, captionList: list = None, categoriesList: list = None, backgroundColor: str = None, fansOnly: bool = False, extensions: dict = None, crash: bool = False):
        mediaList = list()

        if captionList is not None:
            for image, caption in zip(imageList, captionList):
                mediaList.append([100, upload_media(self, image, "image"), caption])

        else:
            if imageList is not None:
                for image in imageList:
                    mediaList.append([100, upload_media(self, image, "image"), None])

        data = {
            "address": None,
            "content": content,
            "title": title,
            "mediaList": mediaList,
            "extensions": extensions,
            "latitude": 0,
            "longitude": 0,
            "eventSource": "GlobalComposeMenu",
        }

        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if categoriesList: data["taggedBlogCategoryIdList"] = categoriesList
        
        response = self.session.post(f"{api}/x{self.comId}/s/blog", json=data)

        return response.status_code

    def post_wiki(self, title: str, content: str, icon: str = None, imageList: list = None, keywords: str = None, backgroundColor: str = None, props: list = [], backgroundMediaList: list = []):

        data = {
            "label": title,
            "content": content,
            "mediaList": imageList,
            "eventSource": "GlobalComposeMenu",
            "extensions": {},
        }
        
        if icon: data["icon"] = icon
        if keywords: data["keywords"] = keywords
        if props: data["extensions"].update({"props": props})
        if backgroundMediaList: data["extensions"].update({"style": {"backgroundMediaList": backgroundMediaList}})
        if backgroundColor: data["extensions"].update({"style": {"backgroundColor": backgroundColor}})


        response = self.session.post(f"{api}/x{self.comId}/s/item", json=data)
        return response.status_code

    def edit_blog(self, blogId: str, title: str = None, content: str = None, imageList: list = None, categoriesList: list = None, backgroundColor: str = None, fansOnly: bool = False):
        mediaList = list()

        for image in imageList:
            mediaList.append([100, upload_media(self, image, "image"), None])

        data = {
            "address": None,
            "mediaList": mediaList,
            "latitude": 0,
            "longitude": 0,
            "eventSource": "PostDetailView",
        }

        if title: data["title"] = title
        if content: data["content"] = content
        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if categoriesList: data["taggedBlogCategoryIdList"] = categoriesList
        
        response = self.session.post(f"{api}/x{self.comId}/s/blog/{blogId}", json=data)
        return response.status_code

    def delete_blog(self, blogId: str):
        response = self.session.delete(f"{api}/x{self.comId}/s/blog/{blogId}")
        return response.status_code

    def delete_wiki(self, wikiId: str):
        response = self.session.delete(f"{api}/x{self.comId}/s/item/{wikiId}")
        return response.status_code

    def repost_blog(self, content: str = None, blogId: str = None, wikiId: str = None):
        if blogId is not None: refObjectId, refObjectType = blogId, 1
        elif wikiId is not None: refObjectId, refObjectType = wikiId, 2
        else: raise exceptions.SpecifyType

        data = {
            "content": content,
            "refObjectId": refObjectId,
            "refObjectType": refObjectType,
            "type": 2,
        }
        
        response = self.session.post(f"{api}/x{self.comId}/s/blog", json=data)
        return response.status_code

    def check_in(self, tz: int = -timezone // 1000):
        data = { "timezone": tz }
        
        response = self.session.post(f"{api}/x{self.comId}/s/check-in", json=data)
        return response.status_code

    def repair_check_in(self, method: int = 0):
        data = dict()
        if method == 0: data["repairMethod"] = "1"  # Coins
        if method == 1: data["repairMethod"] = "2"  # Amino+
        
        response = self.session.post(f"{api}/x{self.comId}/s/check-in/repair", json=data)
        return response.status_code

    def lottery(self, tz: int = -timezone // 1000):
        data = { "timezone": tz }
        
        response = self.session.post(f"{api}/x{self.comId}/s/check-in/lottery", json=data)
        return objects.LotteryLog(response.json()["lotteryLog"]).LotteryLog

    def edit_profile(self, nickname: str = None, content: str = None, icon: BinaryIO = None, chatRequestPrivilege: str = None, imageList: list = None, captionList: list = None, backgroundImage: str = None, backgroundColor: str = None, titles: list = None, colors: list = None, defaultBubbleId: str = None):
        mediaList = list()

        data = dict()

        if captionList is not None:
            for image, caption in zip(imageList, captionList):
                mediaList.append([100, upload_media(self, image, "image"), caption])

        else:
            if imageList is not None:
                for image in imageList:
                    mediaList.append([100, upload_media(self, image, "image"), None])

        if imageList is not None or captionList is not None:
            data["mediaList"] = mediaList

        if nickname: data["nickname"] = nickname
        if icon: data["icon"] = upload_media(self, icon, "image")
        if content: data["content"] = content

        if chatRequestPrivilege: data["extensions"] = {"privilegeOfChatInviteRequest": chatRequestPrivilege}
        if backgroundImage: data["extensions"] = {"style": {"backgroundMediaList": [[100, backgroundImage, None, None, None]]}}
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if defaultBubbleId: data["extensions"] = {"defaultBubbleId": defaultBubbleId}

        if titles or colors:
            tlt = []
            for titles, colors in zip(titles, colors):
                tlt.append({"title": titles, "color": colors})

            data["extensions"] = {"customTitles": tlt}
        

        response = self.session.post(f"{api}/x{self.comId}/s/user-profile/{self.profile.userId}", json=data)
        return response.status_code

    def vote_poll(self, blogId: str, optionId: str):
        data = {
            "value": 1,
            "eventSource": "PostDetailView"
        }
        
        response = self.session.post(f"{api}/x{self.comId}/s/blog/{blogId}/poll/option/{optionId}/vote", json=data)
        return response.status_code

    def comment(self, message: str, userId: str = None, blogId: str = None, wikiId: str = None, replyTo: str = None, isGuest: bool = False):
        data = {
            "content": message,
            "stickerId": None,
            "type": 0
        }

        if replyTo: data["respondTo"] = replyTo

        if isGuest: comType = "g-comment"
        else: comType = "comment"

        if userId:
            data["eventSource"] = "UserProfileView"
            url = f"{api}/x{self.comId}/s/user-profile/{userId}/{comType}"

        elif blogId:
            data["eventSource"] = "PostDetailView"
            url = f"{api}/x{self.comId}/s/blog/{blogId}/{comType}"

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            url = f"{api}/x{self.comId}/s/item/{wikiId}/{comType}"

        else: raise exceptions.SpecifyType

        response = self.session.post(url, json=data)

        return response.status_code

    def delete_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None):
        if userId: url = f"{api}/x{self.comId}/s/user-profile/{userId}/comment/{commentId}"
        elif blogId: url = f"{api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}"
        elif wikiId: url = f"{api}/x{self.comId}/s/item/{wikiId}/comment/{commentId}"
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
            "value": 4
        }

        if blogId:
            if isinstance(blogId, str):
                data["eventSource"] = "UserProfileView"
                url = f"{api}/x{self.comId}/s/blog/{blogId}/vote?cv=1.2"

            elif isinstance(blogId, list):
                data["targetIdList"] = blogId
                url = f"{api}/x{self.comId}/s/feed/vote"

            else: raise exceptions.WrongType

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            url = f"{api}/x{self. comId}/s/item/{wikiId}/vote?cv=1.2"

        else: raise exceptions.SpecifyType()

        response = self.session.post(url, json=data)
        return response.status_code

    def unlike_blog(self, blogId: str = None, wikiId: str = None):
        if blogId: url = f"{api}/x{self.comId}/s/blog/{blogId}/vote?eventSource=UserProfileView"
        elif wikiId: url = f"{api}/x{self.comId}/s/item/{wikiId}/vote?eventSource=PostDetailView"
        else: raise exceptions.SpecifyType()

        response = self.session.delete(url)
        return response.status_code

    def like_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None):
        data = {
            "value": 1
        }

        if userId:
            data["eventSource"] = "UserProfileView"
            
            url = f"{api}/x{self.comId}/s/user-profile/{userId}/comment/{commentId}/vote?cv=1.2&value=1"

        elif blogId:
            data["eventSource"] = "PostDetailView"
            
            url = f"{api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?cv=1.2&value=1"

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            
            url = f"{api}/x{self.comId}/s/item/{wikiId}/comment/{commentId}/g-vote?cv=1.2&value=1"

        else: raise exceptions.SpecifyType()

        response = self.session.post(url, json=data)
        return response.status_code

    def unlike_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None):
        if userId: url = f"{api}/x{self.comId}/s/user-profile/{userId}/comment/{commentId}/g-vote?eventSource=UserProfileView"
        elif blogId: url = f"{api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}/g-vote?eventSource=PostDetailView"
        elif wikiId: url = f"{api}/x{self.comId}/s/item/{wikiId}/comment/{commentId}/g-vote?eventSource=PostDetailView"
        else: raise exceptions.SpecifyType()

        response = self.session.delete(url)
        return response.status_code

    def upvote_comment(self, blogId: str, commentId: str):
        data = {
            "value": 1,
            "eventSource": "PostDetailView"
        }
        
        response = self.session.post(f"{api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?cv=1.2&value=1", json=data)
        return response.status_code

    def downvote_comment(self, blogId: str, commentId: str):
        data = {
            "value": -1,
            "eventSource": "PostDetailView"
        }
        
        response = self.session.post(f"{api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?cv=1.2&value=-1", json=data)
        return response.status_code

    def unvote_comment(self, blogId: str, commentId: str):
        response = self.session.delete(f"{api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?eventSource=PostDetailView")
        return response.status_code

    def reply_wall(self, userId: str, commentId: str, message: str):
        data = {
            "content": message,
            "stackedId": None,
            "respondTo": commentId,
            "type": 0,
            "eventSource": "UserProfileView"
        }
        
        response = self.session.post(f"{api}/x{self.comId}/s/user-profile/{userId}/comment", json=data)
        return response.status_code

    def send_active_obj(self, startTime: int = None, endTime: int = None, optInAdsFlags: int = 2147483647, tz: int = -timezone // 1000, timers: list = None): 
        data = {"userActiveTimeChunkList": [{"start": startTime, "end": endTime}], "optInAdsFlags": optInAdsFlags, "timezone": tz} 
        if timers: data["userActiveTimeChunkList"] = timers 
        
        response = self.session.post(f"{api}/x{self.comId}/s/community/stats/user-active-time", json=data) 
        return response.status_code

    def activity_status(self, status: str):
        if "on" in status.lower(): status = 1
        elif "off" in status.lower(): status = 2
        else: raise exceptions.WrongType(status)

        data = {
            "onlineStatus": status,
            "duration": 86400
        }
        
        response = self.session.post(f"{api}/x{self.comId}/s/user-profile/{self.profile.userId}/online-status", json=data)
        return response.status_code

    # TODO : Finish this
    def watch_ad(self):
        response = self.session.post(f"{api}/g/s/wallet/ads/video/start")
        return response.status_code

    def check_notifications(self):
        response = self.session.post(f"{api}/x{self.comId}/s/notification/checked")
        return response.status_code

    def delete_notification(self, notificationId: str):
        response = self.session.delete(f"{api}/x{self.comId}/s/notification/{notificationId}")
        return response.status_code

    def clear_notifications(self):
        response = self.session.delete(f"{api}/x{self.comId}/s/notification")
        return response.status_code

    def start_chat(self, userId: Union[str, list], message: str, title: str = None, content: str = None, isGlobal: bool = False, publishToGlobal: bool = False):
        if isinstance(userId, str): userIds = [userId]
        elif isinstance(userId, list): userIds = userId
        elif isinstance(userId, tuple): userIds = userId
        else: raise exceptions.WrongType(type(userId))

        data = {
            "title": title,
            "inviteeUids": userIds,
            "initialMessageContent": message,
            "content": content
        }

        if isGlobal is True:
            data["type"] = 2
            data["eventSource"] = "GlobalComposeMenu"
        else: 
            data["type"] = 0

        if publishToGlobal is True: 
            data["publishToGlobal"] = 1
        else: 
            data["publishToGlobal"] = 0

        
        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread", json=data)
        return objects.Thread(response.json()["thread"]).Thread

    def invite_to_chat(self, userId: Union[str, list], chatId: str):
        if isinstance(userId, str): userIds = [userId]
        elif isinstance(userId, list): userIds = userId
        elif isinstance(userId, tuple): userIds = userId
        else: raise exceptions.WrongType(type(userId))

        data = { "uids": userIds }
        
        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/member/invite", json=data)
        return response.status_code

    def add_to_favorites(self, userId: str):
        response = self.session.post(f"{api}/x{self.comId}/s/user-group/quick-access/{userId}")
        return response.status_code

    def send_coins(self, coins: int, blogId: str = None, chatId: str = None, objectId: str = None, transactionId: str = None):
        url = None
        if transactionId is None: transactionId = str(uuid4())

        data = {
            "coins": coins,
            "tippingContext": {"transactionId": transactionId}
        }

        if blogId is not None: url = f"{api}/x{self.comId}/s/blog/{blogId}/tipping"
        if chatId is not None: url = f"{api}/x{self.comId}/s/chat/thread/{chatId}/tipping"
        if objectId is not None:
            data["objectId"] = objectId
            data["objectType"] = 2
            url = f"{api}/x{self.comId}/s/tipping"

        if url is None: raise exceptions.SpecifyType
        
        response = self.session.post(url, json=data)
        return response.status_code

    def thank_tip(self, chatId: str, userId: str):
        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/tipping/tipped-users/{userId}/thank")
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
            response = self.session.post(f"{api}/x{self.comId}/s/user-profile/{userId}/member")

        elif isinstance(userId, list):
            data = { "targetUidList": userId }
            
            response = self.session.post(f"{api}/x{self.comId}/s/user-profile/{self.profile.userId}/joined", json=data)

        else: raise exceptions.WrongType(type(userId))

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
        response = self.session.delete(f"{api}/x{self.comId}/s/user-profile/{self.profile.userId}/joined/{userId}")
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
        response = self.session.post(f"{api}/x{self.comId}/s/block/{userId}")
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
        response = self.session.delete(f"{api}/x{self.comId}/s/block/{userId}")
        return response.status_code

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

        
        response = self.session.post(f"{api}/x{self.comId}/s/{flg}", json=data)
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


        response = self.session.post(
            url=f"{api}/x{self.comId}/s/chat/thread/{chatId}/message",
            json=data
        )

        return response.status_code

    def full_embed(self, link: str, image: BinaryIO, message: str, chatId: str):
        data = {
            "type": 0,
            "content": message,
            "extensions": {
                "linkSnippetList": [{
                    "link": link,
                    "mediaType": 100,
                    "mediaUploadValue": b64encode(image.read()).decode(),
                    "mediaUploadValueContentType": "image/png"
                }]
            },
            "attachedObject": None
        }
        
        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/message", json=data)
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

        
        if not asStaff: response = self.session.delete(f"{api}/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}")
        else: response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}/admin", json=data)

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
            "messageId": messageId
        }
        
        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/mark-as-read", json=data)
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

        res = list()

        if doNotDisturb is not None:
            if doNotDisturb:
                data = {"alertOption": 2 }
                
                response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.profile.userId}/alert", json=data)
                res.append(response.status_code)

            if not doNotDisturb:
                data = {"alertOption": 1 }
                
                response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.profile.userId}/alert", json=data)
                res.append(response.status_code)

        if pinChat is not None:
            if pinChat:
                response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/pin", json=data)
                res.append(response.status_code)

            if not pinChat:
                response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/unpin", json=data)
                res.append(response.status_code)

        if backgroundImage is not None:
            data = {"media": [100, backgroundImage, None] }
            
            response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.profile.userId}/background", json=data)
            res.append(response.status_code)

        if coHosts is not None:
            data = {"uidList": coHosts }
            
            response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/co-host", json=data)
            res.append(response.status_code)

        if viewOnly is not None:
            if viewOnly:
                response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/view-only/enable")
                res.append(response.status_code)

            if not viewOnly:
                response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/view-only/disable")
                res.append(response.status_code)

        if canInvite is not None:
            if canInvite:
                response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/members-can-invite/enable", json=data)
                res.append(response.status_code)

            if not canInvite:
                response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/members-can-invite/disable", json=data)
                res.append(response.status_code)

        if canTip is not None:
            if canTip:
                response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/tipping-perm-status/enable", json=data)
                res.append(response.status_code)

            if not canTip:
                response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/tipping-perm-status/disable", json=data)
                res.append(response.status_code)

        
        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}", json=data)
        res.append(response.status_code)

        return res

    def transfer_host(self, chatId: str, userIds: list):
        data = { "uidList": userIds }
        
        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/transfer-organizer", json=data)
        return response.status_code

    def transfer_organizer(self, chatId: str, userIds: list):
        self.transfer_host(chatId, userIds)

    def accept_host(self, chatId: str, requestId: str):
        data = dict()
        
        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/transfer-organizer/{requestId}/accept", json=data)
        return response.status_code

    def accept_organizer(self, chatId: str, requestId: str):
        self.accept_host(chatId, requestId)

    def kick(self, userId: str, chatId: str, allowRejoin: bool = True):
        if allowRejoin: allowRejoin = 1
        if not allowRejoin: allowRejoin = 0
        response = self.session.delete(f"{api}/x{self.comId}/s/chat/thread/{chatId}/member/{userId}?allowRejoin={allowRejoin}")
        return response.status_code

    def join_chat(self, chatId: str):
        """
        Join an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.profile.userId}")
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
        response = self.session.delete(f"{api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.profile.userId}")
        return response.status_code
        
    def delete_chat(self, chatId: str):
        """
        Delete a Chat.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.delete(f"{api}/x{self.comId}/s/chat/thread/{chatId}")
        return response.status_code
        
    def subscribe(self, userId: str, autoRenew: str = False, transactionId: str = None):
        if transactionId is None: transactionId = str(uuid4())

        data = {
            "paymentContext": {
                "transactionId": transactionId,
                "isAutoRenew": autoRenew
            }
        }
        
        response = self.session.post(f"{api}/x{self.comId}/s/influencer/{userId}/subscribe", json=data)
        return response.status_code

    def promotion(self, noticeId: str, type: str = "accept"):
        response = self.session.post(f"{api}/x{self.comId}/s/notice/{noticeId}/{type}")
        return response.status_code

    def play_quiz_raw(self, quizId: str, quizAnswerList: list, quizMode: int = 0):
        data = {
            "mode": quizMode,
            "quizAnswerList": quizAnswerList
        }
        
        response = self.session.post(f"{api}/x{self.comId}/s/blog/{quizId}/quiz/result", json=data)
        return response.status_code

    def play_quiz(self, quizId: str, questionIdsList: list, answerIdsList: list, quizMode: int = 0):
        quizAnswerList = list()

        for question, answer in zip(questionIdsList, answerIdsList):
            part = {
                "optIdList": [answer],
                "quizQuestionId": question,
                "timeSpent": 0.0
            }

            quizAnswerList.append(part)

        data = {
            "mode": quizMode,
            "quizAnswerList": quizAnswerList
        }
        
        response = self.session.post(f"{api}/x{self.comId}/s/blog/{quizId}/quiz/result", json=data)
        return response.status_code

    def vc_permission(self, chatId: str, permission: int):
        """Voice Chat Join Permissions
        1 - Open to Everyone
        2 - Approval Required
        3 - Invite Only
        """
        data = { "vvChatJoinType": permission }
        
        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/vvchat-permission", json=data)
        return response.status_code

    def get_vc_reputation_info(self, chatId: str):
        response = self.session.get(f"{api}/x{self.comId}/s/chat/thread/{chatId}/avchat-reputation")
        return objects.VcReputation(response.json()).VcReputation

    def claim_vc_reputation(self, chatId: str):
        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/avchat-reputation")
        return objects.VcReputation(response.json()).VcReputation

    def get_all_users(self, type: str = "recent", start: int = 0, size: int = 25):
        types = ["recent", "banned", "featured", "leaders", "curators"]

        if type not in types:
            raise exceptions.WrongType(type)

        response = self.session.get(f"{api}/x{self.comId}/s/user-profile?type={type}&start={start}&size={size}")
        return objects.UserProfileCountList(response.json()).UserProfileCountList

    def get_online_users(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/live-layer?topic=ndtopic:x{self.comId}:online-members&start={start}&size={size}")
        return objects.UserProfileCountList(response.json()).UserProfileCountList

    def get_online_favorite_users(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/user-group/quick-access?type=online&start={start}&size={size}")
        return objects.UserProfileCountList(response.json()).UserProfileCountList

    def get_user_info(self, userId: str):
        """
        Information of an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **Success** : :meth:`User Object <amino.lib.util.objects.UserProfile>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/x{self.comId}/s/user-profile/{userId}")
        return objects.UserProfile(response.json()["userProfile"]).UserProfile

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
        response = self.session.get(f"{api}/x{self.comId}/s/user-profile/{userId}/joined?start={start}&size={size}")
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
        response = self.session.get(f"{api}/x{self.comId}/s/user-profile/{userId}/member?start={start}&size={size}")
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList

    def get_user_checkins(self, userId: str):
        response = self.session.get(f"{api}/x{self.comId}/s/check-in/stats/{userId}?timezone={timezone // 1000}")
        return objects.UserCheckIns(response.json()).UserCheckIns

    def get_user_blogs(self, userId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/blog?type=user&q={userId}&start={start}&size={size}", headers=self.parse_headers())
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_user_wikis(self, userId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/item?type=user-all&start={start}&size={size}&cv=1.2&uid={userId}", headers=self.parse_headers())
        return objects.WikiList(response.json()["itemList"]).WikiList

    def get_user_achievements(self, userId: str):
        response = self.session.get(f"{api}/x{self.comId}/s/user-profile/{userId}/achievements", headers=self.parse_headers())
        return objects.UserAchievements(response.json()["achievements"]).UserAchievements

    def get_influencer_fans(self, userId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/influencer/{userId}/fans?start={start}&size={size}", headers=self.parse_headers())
        return objects.InfluencerFans(response.json()).InfluencerFans

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
        response = self.session.get(f"{api}/x{self.comId}/s/block?start={start}&size={size}")
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList

    def get_blocker_users(self, start: int = 0, size: int = 25):
        """
        List of Users that are Blocking the User.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`List of User IDs <List>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        response = self.session.get(f"{api}/x{self.comId}/s/block?start={start}&size={size}")
        return response.json()["blockerUidList"]

    def search_users(self, nickname: str, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/user-profile?type=name&q={nickname}&start={start}&size={size}")
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList

    def get_saved_blogs(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/bookmark?start={start}&size={size}")
        return objects.UserSavedBlogs(response.json()["bookmarkList"]).UserSavedBlogs

    def get_leaderboard_info(self, type: str, start: int = 0, size: int = 25):
        ranking_types = {
            '24': 1,
            'hour': 1,
            '7': 2,
            'day': 2,
            'rep': 3,
            'check': 4,
            'quiz': 5
        }

        if type not in ranking_types:
            raise exceptions.WrongType(type)

        ranking_type = ranking_types[type]
        url = f"{api}/g/s-x{self.comId}/community/leaderboard?rankingType={ranking_type}&start={start}"
        if ranking_type != 4:
            url += f"&size={size}"

        response = self.session.get(url)
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList


    def get_wiki_info(self, wikiId: str):
        response = self.session.get(f"{api}/x{self.comId}/s/item/{wikiId}")
        return objects.GetWikiInfo(response.json()).GetWikiInfo

    def get_recent_wiki_items(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/item?type=catalog-all&start={start}&size={size}")
        return objects.WikiList(response.json()["itemList"]).WikiList

    def get_wiki_categories(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/item-category?start={start}&size={size}")
        return objects.WikiCategoryList(response.json()["itemCategoryList"]).WikiCategoryList

    def get_wiki_category(self, categoryId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/item-category/{categoryId}?pagingType=t&start={start}&size={size}")
        return objects.WikiCategory(response.json()).WikiCategory

    def get_tipped_users(self, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, chatId: str = None, start: int = 0, size: int = 25):
        object_types = {
            'blogId': {'id': blogId or quizId, 'url': f"{api}/x{self.comId}/s/blog/{blogId or quizId}/tipping/tipped-users-summary"},
            'wikiId': {'id': wikiId, 'url': f"{api}/x{self.comId}/s/item/{wikiId}/tipping/tipped-users-summary"},
            'chatId': {'id': chatId, 'url': f"{api}/x{self.comId}/s/chat/thread/{chatId}/tipping/tipped-users-summary"},
            'fileId': {'id': fileId, 'url': f"{api}/x{self.comId}/s/shared-folder/files/{fileId}/tipping/tipped-users-summary"}
        }

        for key, value in object_types.items():
            if value['id']:
                response = self.session.get(f"{value['url']}?start={start}&size={size}")
                break
        else:
            raise exceptions.SpecifyType

        return objects.TippedUsersSummary(response.json()).TippedUsersSummary


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
        response = self.session.get(f"{api}/x{self.comId}/s/chat/thread?type=joined-me&start={start}&size={size}")
        return objects.ThreadList(response.json()["threadList"]).ThreadList

    def get_public_chat_threads(self, type: str = "recommended", start: int = 0, size: int = 25):
        """
        List of Public Chats of the Community.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Chat List <amino.lib.util.objects.ThreadList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/x{self.comId}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}")
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
        response = self.session.get(f"{api}/x{self.comId}/s/chat/thread/{chatId}")
        return objects.Thread(response.json()["thread"]).Thread

    def get_chat_messages(self, chatId: str, size: int = 25, pageToken: str = None):
        """
        List of Messages from an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.
            - *size* : Size of the list.
            - *pageToken* : Next Page Token.

        **Returns**
            - **Success** : :meth:`Message List <amino.lib.util.objects.MessageList>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """

        if pageToken is not None: url = f"{api}/x{self.comId}/s/chat/thread/{chatId}/message?v=2&pagingType=t&pageToken={pageToken}&size={size}"
        else: url = f"{api}/x{self.comId}/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}"

        response = self.session.get(url)
        return objects.GetMessages(response.json()).GetMessages

    def get_message_info(self, chatId: str, messageId: str):
        """
        Information of an Message from an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.
            - **message** : ID of the Message.

        **Returns**
            - **Success** : :meth:`Message Object <amino.lib.util.objects.Message>`

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}")
        return objects.Message(response.json()["message"]).Message

    def get_blog_info(self, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None):
        if blogId or quizId:
            if quizId is not None: blogId = quizId
            response = self.session.get(f"{api}/x{self.comId}/s/blog/{blogId}")
            return objects.GetBlogInfo(response.json()).GetBlogInfo

        elif wikiId:
            response = self.session.get(f"{api}/x{self.comId}/s/item/{wikiId}")
            return objects.GetWikiInfo(response.json()).GetWikiInfo

        elif fileId:
            response = self.session.get(f"{api}/x{self.comId}/s/shared-folder/files/{fileId}")
            return objects.SharedFolderFile(response.json()["file"]).SharedFolderFile

        else: raise exceptions.SpecifyType

    def get_blog_comments(self, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, sorting: str = "newest", start: int = 0, size: int = 25):
        if sorting not in ["newest", "oldest", "top"]:
            raise ValueError("Invalid sorting type. Must be 'newest', 'oldest' or 'top'.")

        sorting = "vote" if sorting == "top" else sorting

        object_types = {
            'blogId': {'id': blogId or quizId, 'url': f"{api}/x{self.comId}/s/blog/{blogId or quizId}/comment"},
            'wikiId': {'id': wikiId, 'url': f"{api}/x{self.comId}/s/item/{wikiId}/comment"},
            'fileId': {'id': fileId, 'url': f"{api}/x{self.comId}/s/shared-folder/files/{fileId}/comment"}
        }

        for key, value in object_types.items():
            if value['id']:
                response = self.session.get(f"{value['url']}?sort={sorting}&start={start}&size={size}")
                break
        else:
            raise exceptions.SpecifyType

        return objects.CommentList(response.json()["commentList"]).CommentList


    def get_blog_categories(self, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/blog-category?size={size}")
        return objects.BlogCategoryList(response.json()["blogCategoryList"]).BlogCategoryList

    def get_blogs_by_category(self, categoryId: str,start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/blog-category/{categoryId}/blog-list?start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_quiz_rankings(self, quizId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/blog/{quizId}/quiz/result?start={start}&size={size}")
        return objects.QuizRankings(response.json()).QuizRankings

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
        if sorting == "newest": sorting = "newest"
        elif sorting == "oldest": sorting = "oldest"
        elif sorting == "top": sorting = "vote"
        else: raise exceptions.WrongType(sorting)

        response = self.session.get(f"{api}/x{self.comId}/s/user-profile/{userId}/comment?sort={sorting}&start={start}&size={size}")
        return objects.CommentList(response.json()["commentList"]).CommentList

    def get_recent_blogs(self, pageToken: str = None, start: int = 0, size: int = 25):
        if pageToken is not None: url = f"{api}/x{self.comId}/s/feed/blog-all?pagingType=t&pageToken={pageToken}&size={size}"
        else: url = f"{api}/x{self.comId}/s/feed/blog-all?pagingType=t&start={start}&size={size}"

        response = self.session.get(url)
        return objects.RecentBlogs(response.json()).RecentBlogs

    def get_chat_users(self, chatId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2")
        return objects.UserProfileList(response.json()["memberList"]).UserProfileList

    def get_notifications(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/notification?pagingType=t&start={start}&size={size}")
        return objects.NotificationList(response.json()["notificationList"]).NotificationList

    def get_notices(self, start: int = 0, size: int = 25):
        """
        :param start: Start of the List (Start: 0)
        :param size: Amount of Notices to Show
        :return: Notices List
        """
        response = self.session.get(f"{api}/x{self.comId}/s/notice?type=usersV2&status=1&start={start}&size={size}")
        return objects.NoticeList(response.json()["noticeList"]).NoticeList

    def get_sticker_pack_info(self, sticker_pack_id: str):
        response = self.session.get(f"{api}/x{self.comId}/s/sticker-collection/{sticker_pack_id}?includeStickers=true")
        return objects.StickerCollection(response.json()["stickerCollection"]).StickerCollection

    def get_sticker_packs(self):
        response = self.session.get(f"{api}/x{self.comId}/s/sticker-collection?includeStickers=false&type=my-active-collection")
        return objects.StickerCollection(response.json()["stickerCollection"]).StickerCollection

    # TODO : Finish this
    def get_store_chat_bubbles(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/store/items?sectionGroupId=chat-bubble&start={start}&size={size}")
        return response.json()

    # TODO : Finish this
    def get_store_stickers(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/store/items?sectionGroupId=sticker&start={start}&size={size}")
        return response.json()

    def get_community_stickers(self):
        response = self.session.get(f"{api}/x{self.comId}/s/sticker-collection?type=community-shared")
        return objects.CommunityStickerCollection(response.json()).CommunityStickerCollection

    def get_sticker_collection(self, collectionId: str):
        response = self.session.get(f"{api}/x{self.comId}/s/sticker-collection/{collectionId}?includeStickers=true")
        return objects.StickerCollection(response.json()["stickerCollection"]).StickerCollection

    def get_shared_folder_info(self):
        response = self.session.get(f"{api}/x{self.comId}/s/shared-folder/stats")
        return objects.GetSharedFolderInfo(response.json()["stats"]).GetSharedFolderInfo

    def get_shared_folder_files(self, type: str = "latest", start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/shared-folder/files?type={type}&start={start}&size={size}")
        return objects.SharedFolderFileList(response.json()["fileList"]).SharedFolderFileList

    #
    # MODERATION MENU
    #

    def moderation_history(self, userId: str = None, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, size: int = 25):
        object_types = {
            'userId': {'id': userId, 'type': 0},
            'blogId': {'id': blogId, 'type': 1},
            'wikiId': {'id': wikiId, 'type': 2},
            'quizId': {'id': quizId, 'type': 1},
            'fileId': {'id': fileId, 'type': 109}
        }

        for key, value in object_types.items():
            if value['id']:
                response = self.session.get(f"{api}/x{self.comId}/s/admin/operation?objectId={value['id']}&objectType={value['type']}&pagingType=t&size={size}")
                break
        else:
            response = self.session.get(f"{api}/x{self.comId}/s/admin/operation?pagingType=t&size={size}")

        return objects.AdminLogList(response.json()["adminLogList"]).AdminLogList

    def feature(self, time: int, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None):
        if chatId:
            if time == 1: time = 3600
            if time == 1: time = 7200
            if time == 1: time = 10800

        else:
            if time == 1: time = 86400
            elif time == 2: time = 172800
            elif time == 3: time = 259200
            else: raise exceptions.WrongType(time)

        data = {
            "adminOpName": 114,
            "adminOpValue": {
                "featuredDuration": time
            }
        }

        if userId:
            data["adminOpValue"] = {"featuredType": 4}
            url = f"{api}/x{self.comId}/s/user-profile/{userId}/admin"

        elif blogId:
            data["adminOpValue"] = {"featuredType": 1}
            url = f"{api}/x{self.comId}/s/blog/{blogId}/admin"

        elif wikiId:
            data["adminOpValue"] = {"featuredType": 1}
            url = f"{api}/x{self.comId}/s/item/{wikiId}/admin"

        elif chatId:
            data["adminOpValue"] = {"featuredType": 5}
            url = f"{api}/x{self.comId}/s/chat/thread/{chatId}/admin"

        else: raise exceptions.SpecifyType

        response = self.session.post(url, json=data)

        return response.json()

    def unfeature(self, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None):
        data = {
            "adminOpName": 114,
            "adminOpValue": {}
        }

        if userId:
            data["adminOpValue"] = {"featuredType": 0}

            url = f"{api}/x{self.comId}/s/user-profile/{userId}/admin"

        elif blogId:
            data["adminOpValue"] = {"featuredType": 0}

            url = f"{api}/x{self.comId}/s/blog/{blogId}/admin"

        elif wikiId:
            data["adminOpValue"] = {"featuredType": 0}
            
            url = f"{api}/x{self.comId}/s/item/{wikiId}/admin"

        elif chatId:
            data["adminOpValue"] = {"featuredType": 0}
            
            url = f"{api}/x{self.comId}/s/chat/thread/{chatId}/admin"

        else: raise exceptions.SpecifyType

        response = self.session.post(url, json=data)

        return response.json()

    def hide(self, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, reason: str = None):
        data = {
            "adminOpNote": {
                "content": reason
            }
        }

        if userId:
            data["adminOpName"] = 18

            url = f"{api}/x{self.comId}/s/user-profile/{userId}/admin"

        elif blogId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9

            url = f"{api}/x{self.comId}/s/blog/{blogId}/admin"

        elif quizId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
 
            url = f"{api}/x{self.comId}/s/blog/{quizId}/admin"

        elif wikiId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9

            url = f"{api}/x{self.comId}/s/item/{wikiId}/admin"

        elif chatId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
 
            url = f"{api}/x{self.comId}/s/chat/thread/{chatId}/admin"

        elif fileId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9

            url = f"{api}/x{self.comId}/s/shared-folder/files/{fileId}/admin"

        else: raise exceptions.SpecifyType

        response = self.session.post(url, json=data)
        return response.json()

    def unhide(self, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, reason: str = None):
        data = {
            "adminOpNote": {
                "content": reason
            }
        }

        if userId:
            data["adminOpName"] = 19

            url = f"{api}/x{self.comId}/s/user-profile/{userId}/admin"

        elif blogId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0

            url = f"{api}/x{self.comId}/s/blog/{blogId}/admin"

        elif quizId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0

            url = f"{api}/x{self.comId}/s/blog/{quizId}/admin"

        elif wikiId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0

            url = f"{api}/x{self.comId}/s/item/{wikiId}/admin"

        elif chatId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0

            url = f"{api}/x{self.comId}/s/chat/thread/{chatId}/admin"

        elif fileId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0

            url = f"{api}/x{self.comId}/s/shared-folder/files/{fileId}/admin"

        else: raise exceptions.SpecifyType

        response = self.session.post(url, json=data)
        return response.json()

    def edit_titles(self, userId: str, tlt: list):

        data = {
            "adminOpName": 207,
            "adminOpValue": {
                "titles": tlt
            }
        }

        response = self.session.post(f"{api}/x{self.comId}/s/user-profile/{userId}/admin", json=data)
        return response.json()

    # TODO : List all warning texts
    def warn(self, userId: str, reason: str = None):
        data = {
            "uid": userId,
            "title": "Custom",
            "content": reason,
            "attachedObject": {
                "objectId": userId,
                "objectType": 0
            },
            "penaltyType": 0,
            "adminOpNote": {},
            "noticeType": 7
        }

        response = self.session.post(f"{api}/x{self.comId}/s/notice", json=data)
        return response.json()

    # TODO : List all strike texts
    def strike(self, userId: str, time: int, title: str = None, reason: str = None):
        if time == 1: time = 86400
        elif time == 2: time = 10800
        elif time == 3: time = 21600
        elif time == 4: time = 43200
        elif time == 5: time = 86400
        else: raise exceptions.WrongType(time)

        data = {
            "uid": userId,
            "title": title,
            "content": reason,
            "attachedObject": {
                "objectId": userId,
                "objectType": 0
            },
            "penaltyType": 1,
            "penaltyValue": time,
            "adminOpNote": {},
            "noticeType": 4
        }

        response = self.session.post(f"{api}/x{self.comId}/s/notice", json=data)
        return response.json()

    def ban(self, userId: str, reason: str, banType: int = None):
        data = {
            "reasonType": banType,
            "note": {
                "content": reason
            }
        }

        response = self.session.post(f"{api}/x{self.comId}/s/user-profile/{userId}/ban", json=data)
        return response.json()

    def unban(self, userId: str, reason: str):
        data = {
            "note": {
                "content": reason
            }
        }

        response = self.session.post(f"{api}/x{self.comId}/s/user-profile/{userId}/unban", json=data)
        return response.json()

    def reorder_featured_users(self, userIds: list):
        data = { "uidList": userIds }

        response = self.session.post(f"{api}/x{self.comId}/s/user-profile/featured/reorder", json=data)
        return response.json()

    def get_hidden_blogs(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/feed/blog-disabled?start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_featured_users(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/user-profile?type=featured&start={start}&size={size}")
        return objects.UserProfileCountList(response.json()).UserProfileCountList

    def review_quiz_questions(self, quizId: str):
        response = self.session.get(f"{api}/x{self.comId}/s/blog/{quizId}?action=review")
        return objects.QuizQuestionList(response.json()["blog"]["quizQuestionList"]).QuizQuestionList

    def get_recent_quiz(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/blog?type=quizzes-recent&start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_trending_quiz(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/feed/quiz-trending?start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_best_quiz(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/feed/quiz-best-quizzes?start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    # Provided by "spectrum#4691"
    def purchase(self, objectId: str, objectType: int, aminoPlus: bool = True, autoRenew: bool = False):
        data = {
            "objectId": objectId,
            "objectType": objectType,
            "v": 1,
        }

        if aminoPlus: data['paymentContext'] = {'discountStatus': 1, 'discountValue': 1, 'isAutoRenew': autoRenew}
        else: data['paymentContext'] = {'discountStatus': 0, 'discountValue': 1, 'isAutoRenew': autoRenew}

        response = self.session.post(f"{api}/x{self.comId}/s/store/purchase", json=data)
        return response.status_code

    # Provided by "spectrum#4691"
    def apply_avatar_frame(self, avatarId: str, applyToAll: bool = True):
        """
        Apply avatar frame.

        **Parameters**
            - **avatarId** : ID of the avatar frame.
            - **applyToAll** : Apply to all.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`

        """

        data = {
            "frameId": avatarId,
            "applyToAll": 0,
        }

        if applyToAll: data["applyToAll"] = 1

        response = self.session.post(f"{api}/x{self.comId}/s/avatar-frame/apply", json=data)
        return response.status_code

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

        data = { "uid": userId }

        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/{chatId}/vvchat-presenter/invite/", json=data)
        return response.status_code

    def add_poll_option(self, blogId: str, question: str):
        data = {
            "mediaList": None,
            "title": question,
            "type": 0
        }

        response = self.session.post(f"{api}/x{self.comId}/s/blog/{blogId}/poll/option", json=data)
        return response.status_code

    def create_wiki_category(self, title: str, parentCategoryId: str, media: list = None):
        data = {
            "icon": None,
            "label": title,
            "mediaList": media,
            "parentCategoryId": parentCategoryId,
        }

        response = self.session.post(f"{api}/x{self.comId}/s/item-category", json=data)
        return response.status_code

    def create_shared_folder(self,title: str):
        data = { "title": title }
        
        response = self.session.post(f"{api}/x{self.comId}/s/shared-folder/folders", json=data)
        return response.status_code

    def submit_to_wiki(self, wikiId: str, message: str):
        data = {
            "message": message,
            "itemId": wikiId
        }

        response = self.session.post(f"{api}/x{self.comId}/s/knowledge-base-request", json=data)
        return response.status_code

    def accept_wiki_request(self, requestId: str, destinationCategoryIdList: list):
        data = {
            "destinationCategoryIdList": destinationCategoryIdList,
            "actionType": "create"
        }

        response = self.session.post(f"{api}/x{self.comId}/s/knowledge-base-request/{requestId}/approve", json=data)
        return response.status_code

    def reject_wiki_request(self, requestId: str):
        data = dict()

        response = self.session.post(f"{api}/x{self.comId}/s/knowledge-base-request/{requestId}/reject", json=data)
        return response.status_code

    def get_wiki_submissions(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/knowledge-base-request?type=all&start={start}&size={size}")
        return objects.WikiRequestList(response.json()["knowledgeBaseRequestList"]).WikiRequestList

    def get_live_layer(self):
        response = self.session.get(f"{api}/x{self.comId}/s/live-layer/homepage?v=2")
        return objects.LiveLayer(response.json()["liveLayerList"]).LiveLayer

    def apply_bubble(self, bubbleId: str, chatId: str, applyToAll: bool = False):
        data = {
            "applyToAll": 0,
            "bubbleId": bubbleId,
            "threadId": chatId,
        }

        if applyToAll is True:
            data["applyToAll"] = 1

        response = self.session.post(f"{api}/x{self.comId}/s/chat/thread/apply-bubble", json=data)
        return response.status_code
