# pylint: disable=invalid-name
# pylint: disable=too-many-lines

from uuid import uuid4
from typing import BinaryIO
from requests import Session

from .constants import upload_media
from .abstract_client import AbstractClient
from .lib.util import exceptions, objects

class SubClient(AbstractClient):
    "Module for work with community"
    def __init__(self, comId: int = None, *, profile: objects.UserProfile):
        self.profile = profile
        self.session: Session = self.profile.session
    
        super().__init__(self.session, f"/x{comId}")

        self.comId = comId

    def get_invite_codes(self, status: str = "normal", start: int = 0, size: int = 25):
        """
        Retrieves the invite codes for the community.

        **Parameters**
            - *status* : The status of the invite codes to be retrieved. Defaults to "normal".
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Invite Code List <AminoLightPy.lib.util.objects.InviteCodeList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        params = {
            "status": status,
            "start": start,
            "size": size
        }
        response = self.session.get(f"/g/s-x{self.comId}/community/invitation", params=params)
        return objects.InviteCodeList(response.json()["communityInvitationList"]).InviteCodeList

    def generate_invite_code(self, duration: int = 0, force: bool = True):
        """
        Generate an invitation code for the community.

        **Parameters**
            - **duration** : The validity duration of the invite code in seconds.
            - **force** : A boolean to force the creation of a new invite code.

        **Returns**
            - **InviteCode** : An object containing the invite code details.

        **Raises**
            - **Exceptions** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "duration": duration,
            "force": force
        }
        response = self.session.post(f"/g/s-x{self.comId}/community/invitation", json=data)
        return objects.InviteCode(response.json()["communityInvitation"]).InviteCode

    def delete_invite_code(self, inviteId: str):
        """
        Delete an existing invitation code from the community.

        **Parameters**
            - **inviteId** : The unique identifier of the invite code to be deleted.

        **Returns**
            - **Success** : 200 (int) if the invite code is successfully deleted.
            - **Fail** : Corresponding HTTP status code (int) if the deletion fails.

        **Raises**
            - **Exceptions** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.delete(f"/g/s-x{self.comId}/community/invitation/{inviteId}")
        return response.status_code

    def post_blog(self, title: str, content: str, imageList: list = None, captionList: list = None,
                        categoriesList: list = None, backgroundColor: str = None,
                        fansOnly: bool = False, extensions: dict = None):
        """
        Post a blog entry to the community.

        **Parameters**
            - **title** : The title of the blog post.
            - **content** : The main content of the blog post.
            - **imageList** : A list of image URLs to be included in the post. Default is None.
            - **captionList** : A list of captions corresponding to each image. Default is None.
            - **categoriesList** : A list of category IDs to tag the blog post with. Default is None.
            - **backgroundColor** : The background color for the blog post. Default is None.
            - **fansOnly** : A boolean to set the blog post as accessible to fans only. Default is False.
            - **extensions** : Additional extension data for the blog post. Default is None.

        **Returns**
            - **Success** : 200 (int) if the blog post is successfully created.
            - **Fail** : Corresponding HTTP status code (int) if the creation fails.

        **Raises**
            - **Exceptions** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>` if the request fails.
        """
        mediaList = []

        if captionList:
            for image, caption in zip(imageList, captionList):
                mediaList.append([100, upload_media(self, image), caption])

        else:
            if imageList:
                for image in imageList:
                    mediaList.append([100, upload_media(self, image), None])

        data = {
            "content": content,
            "title": title,
            "mediaList": mediaList,
            "extensions": extensions,
            "latitude": 0,
            "longitude": 0,
            "eventSource": "GlobalComposeMenu",
        }

        if fansOnly:
            data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor:
            data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if categoriesList:
            data["taggedBlogCategoryIdList"] = categoriesList
        response = self.session.post(f"/x{self.comId}/s/blog", json=data)

        return response.status_code

    def post_wiki(self, title: str, content: str, icon: str = None, imageList: list = None,
                        keywords: str = None, backgroundColor: str = None, props: list = None,
                        backgroundMediaList: list = None):

        if imageList is None:
            imageList = []
        if props is None:
            props = []
        if backgroundMediaList is None:
            backgroundMediaList = []
        data = {
            "label": title,
            "content": content,
            "mediaList": imageList,
            "eventSource": "GlobalComposeMenu",
            "extensions": {},
        }
        if icon:
            data["icon"] = icon
        if keywords:
            data["keywords"] = keywords
        if props:
            data["extensions"].update({"props": props})
        if backgroundMediaList:
            data["extensions"].update({"style": {"backgroundMediaList": backgroundMediaList}})
        if backgroundColor:
            data["extensions"].update({"style": {"backgroundColor": backgroundColor}})

        response = self.session.post(f"/x{self.comId}/s/item", json=data)
        return response.status_code

    def edit_blog(self, blogId: str, title: str = None, content: str = None,
                imageList: list = None, categoriesList: list = None,
                backgroundColor: str = None, fansOnly: bool = False):
        mediaList = []

        for image in imageList:
            mediaList.append([100, upload_media(self, image), None])

        data = {
            "address": None,
            "mediaList": mediaList,
            "latitude": 0,
            "longitude": 0,
            "eventSource": "PostDetailView",
        }

        if title:
            data["title"] = title
        if content:
            data["content"] = content
        if fansOnly:
            data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor:
            data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if categoriesList:
            data["taggedBlogCategoryIdList"] = categoriesList

        return self.session.post(f"/x{self.comId}/s/blog/{blogId}", json=data).status_code

    def delete_blog(self, blogId: str):
        return self.session.delete(f"/x{self.comId}/s/blog/{blogId}").status_code

    def delete_wiki(self, wikiId: str):
        return self.session.delete(f"/x{self.comId}/s/item/{wikiId}").status_code

    def repost_blog(self, content: str = None, blogId: str = None, wikiId: str = None):
        if blogId:
            refObjectId, refObjectType = blogId, 1
        elif wikiId:
            refObjectId, refObjectType = wikiId, 2
        else: raise exceptions.SpecifyType

        data = {
            "content": content,
            "refObjectId": refObjectId,
            "refObjectType": refObjectType,
            "type": 2,
        }
        response = self.session.post(f"/x{self.comId}/s/blog", json=data)
        return response.status_code

    def check_in(self, tz: int = 180):
        data = { "timezone": tz }
        response = self.session.post(f"/x{self.comId}/s/check-in", json=data)
        return response.status_code

    def repair_check_in(self, method: int = 0):
        data = {
            "repairMethod": str(method+1)
        }
        response = self.session.post(f"/x{self.comId}/s/check-in/repair", json=data)
        return response.status_code

    def lottery(self, tz: int = 180):
        data = { "timezone": tz }
        response = self.session.post(f"/x{self.comId}/s/check-in/lottery", json=data)
        return objects.LotteryLog(response.json()["lotteryLog"]).LotteryLog
    
    def vote_poll(self, blogId: str, optionId: str):
        data = {
            "value": 1,
            "eventSource": "PostDetailView"
        }

        return self.session.post(
            url=f"/x{self.comId}/s/blog/{blogId}/poll/option/{optionId}/vote",
            json=data
        ).status_code


    def upvote_comment(self, blogId: str, commentId: str):
        data = {
            "value": 1,
            "eventSource": "PostDetailView"
        }
        params = {
            "cv": "1.2",
            "value": "1"
        }
        return self.session.post(
            url=f"/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote",
            params=params,
            json=data
        ).status_code

    def downvote_comment(self, blogId: str, commentId: str):
        data = {
            "value": -1,
            "eventSource": "PostDetailView"
        }
        params = {
            "cv": "1.2",
            "value": "-1"
        }

        return self.session.post(
            url=f"/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote",
            json=data,
            params=params
        ).status_code

    def unvote_comment(self, blogId: str, commentId: str):
        response = self.session.delete(f"/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?eventSource=PostDetailView")
        return response.status_code

    def reply_wall(self, userId: str, commentId: str, message: str):
        data = {
            "content": message,
            "stackedId": None,
            "respondTo": commentId,
            "type": 0,
            "eventSource": "UserProfileView"
        }

        response = self.session.post(f"/x{self.comId}/s/user-profile/{userId}/comment", json=data)
        return response.status_code

    def send_active_obj(self, startTime: int = None, endTime: int = None,
                        tz: int = 180, timers: list = None):
        data = {
            "userActiveTimeChunkList": [{
                "start": startTime,
                "end": endTime
            }],
            "optInAdsFlags": 2147483647,
            "timezone": tz
        }
        if timers: data["userActiveTimeChunkList"] = timers

        response = self.session.post(f"/x{self.comId}/s/community/stats/user-active-time", json=data)
        return response.status_code

    def activity_status(self, status: str):
        """
        Edit online status.

        **Parameters**
            - **status** : on or off.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if "on" in status.lower(): status = 1
        elif "off" in status.lower(): status = 2
        else: raise exceptions.WrongType(status)

        data = {
            "onlineStatus": status,
            "duration": 86400
        }

        response = self.session.post(f"/x{self.comId}/s/user-profile/{self.profile.userId}/online-status", json=data)
        return response.status_code

    def check_notifications(self):
        return self.session.post(f"/x{self.comId}/s/notification/checked").status_code

    def delete_notification(self, notificationId: str):
        response = self.session.delete(f"/x{self.comId}/s/notification/{notificationId}")
        return response.status_code

    def clear_notifications(self):
        return self.session.delete(f"/x{self.comId}/s/notification").status_code

    def add_to_favorites(self, userId: str):
        return self.session.post(f"/x{self.comId}/s/user-group/quick-access/{userId}").status_code

    

    def thank_tip(self, chatId: str, userId: str):
        return self.session.post(
            url=f"/x{self.comId}/s/chat/thread/{chatId}/tipping/tipped-users/{userId}/thank"
        ).status_code


    def full_embed(self, link: str, image: BinaryIO, message: str, chatId: str):
        url = upload_media(self, image)
        data = {
            "type": 0,
            "content": message,
            "extensions": {
                "linkSnippetList": [{
                    "link": link,
                    "mediaValue": url
                }]
            },
            "attachedObject": None
        }

        response = self.session.post(f"/x{self.comId}/s/chat/thread/{chatId}/message", json=data)
        return response.status_code

    def subscribe(self, userId: str, autoRenew: str = False, transactionId: str = None):
        if transactionId is None: transactionId = str(uuid4())

        data = {
            "paymentContext": {
                "transactionId": transactionId,
                "isAutoRenew": autoRenew
            }
        }

        response = self.session.post(f"/x{self.comId}/s/influencer/{userId}/subscribe", json=data)
        return response.status_code

    def promotion(self, noticeId: str, type: str = "accept"):
        return self.session.post(f"/x{self.comId}/s/notice/{noticeId}/{type}").status_code

    def play_quiz_raw(self, quizId: str, quizAnswerList: list, quizMode: int = 0):
        data = {
            "mode": quizMode,
            "quizAnswerList": quizAnswerList
        }

        response = self.session.post(f"/x{self.comId}/s/blog/{quizId}/quiz/result", json=data)
        return response.status_code

    def play_quiz(self, quizId: str, questionIdsList: list, answerIdsList: list, quizMode: int = 0):
        quizAnswerList = []

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
        response = self.session.post(f"/x{self.comId}/s/blog/{quizId}/quiz/result", json=data)
        return response.status_code

    def vc_permission(self, chatId: str, permission: int):
        """Voice Chat Join Permissions
        1 - Open to Everyone
        2 - Approval Required
        3 - Invite Only
        """
        data = { "vvChatJoinType": permission }
        return self.session.post(
            url=f"/x{self.comId}/s/chat/thread/{chatId}/vvchat-permission",
            json=data
        ).status_code

    def get_vc_reputation_info(self, chatId: str):
        response = self.session.get(f"/x{self.comId}/s/chat/thread/{chatId}/avchat-reputation")
        return objects.VcReputation(response.json()).VcReputation

    def claim_vc_reputation(self, chatId: str):
        response = self.session.post(f"/x{self.comId}/s/chat/thread/{chatId}/avchat-reputation")
        return objects.VcReputation(response.json()).VcReputation

    def get_online_users(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/live-layer?topic=ndtopic:x{self.comId}:online-members&start={start}&size={size}")
        return objects.UserProfileCountList(response.json()).UserProfileCountList

    def get_online_favorite_users(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/user-group/quick-access?type=online&start={start}&size={size}")
        return objects.UserProfileCountList(response.json()).UserProfileCountList

    def get_user_checkins(self, userId: str):
        response = self.session.get(f"/x{self.comId}/s/check-in/stats/{userId}?timezone=180")
        return objects.UserCheckIns(response.json()).UserCheckIns

    def get_user_blogs(self, userId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/blog?type=user&q={userId}&start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_user_wikis(self, userId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/item?type=user-all&start={start}&size={size}&cv=1.2&uid={userId}")
        return objects.WikiList(response.json()["itemList"]).WikiList

    def get_user_achievements(self, userId: str):
        response = self.session.get(f"/x{self.comId}/s/user-profile/{userId}/achievements")
        return objects.UserAchievements(response.json()["achievements"]).UserAchievements

    def get_influencer_fans(self, userId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/influencer/{userId}/fans?start={start}&size={size}")
        return objects.InfluencerFans(response.json()).InfluencerFans

    def search_users(self, nickname: str, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/user-profile?type=name&q={nickname}&start={start}&size={size}")
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList

    def get_saved_blogs(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/bookmark?start={start}&size={size}")
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
        url = f"/g/s-x{self.comId}/community/leaderboard?rankingType={ranking_type}&start={start}"
        if ranking_type != 4:
            url += f"&size={size}"

        response = self.session.get(url)
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList

    def get_wiki_info(self, wikiId: str):
        response = self.session.get(f"/x{self.comId}/s/item/{wikiId}")
        return objects.GetWikiInfo(response.json()).GetWikiInfo

    def get_recent_wiki_items(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/item?type=catalog-all&start={start}&size={size}")
        return objects.WikiList(response.json()["itemList"]).WikiList

    def get_wiki_categories(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/item-category?start={start}&size={size}")
        return objects.WikiCategoryList(response.json()["itemCategoryList"]).WikiCategoryList

    def get_wiki_category(self, categoryId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/item-category/{categoryId}?pagingType=t&start={start}&size={size}")
        return objects.WikiCategory(response.json()).WikiCategory

    def get_tipped_users(self, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, chatId: str = None, start: int = 0, size: int = 25):
        object_types = {
            'blogId': {'id': blogId or quizId, 'url': f"/x{self.comId}/s/blog/{blogId or quizId}/tipping/tipped-users-summary"},
            'wikiId': {'id': wikiId, 'url': f"/x{self.comId}/s/item/{wikiId}/tipping/tipped-users-summary"},
            'chatId': {'id': chatId, 'url': f"/x{self.comId}/s/chat/thread/{chatId}/tipping/tipped-users-summary"},
            'fileId': {'id': fileId, 'url': f"/x{self.comId}/s/shared-folder/files/{fileId}/tipping/tipped-users-summary"}
        }

        for key, value in object_types.items():
            if value['id']:
                response = self.session.get(f"{value['url']}?start={start}&size={size}")
                break
        else:
            raise exceptions.SpecifyType

        return objects.TippedUsersSummary(response.json()).TippedUsersSummary

    def get_public_chat_threads(self, type: str = "recommended", start: int = 0, size: int = 25):
        """
        List of Public Chats of the Community.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Chat List <AminoLightPy.lib.util.objects.ThreadList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"/x{self.comId}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}")
        return objects.ThreadList(response.json()["threadList"]).ThreadList


    def get_blog_categories(self, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/blog-category?size={size}")
        return objects.BlogCategoryList(response.json()["blogCategoryList"]).BlogCategoryList

    def get_blogs_by_category(self, categoryId: str,start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/blog-category/{categoryId}/blog-list?start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_quiz_rankings(self, quizId: str, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/blog/{quizId}/quiz/result?start={start}&size={size}")
        return objects.QuizRankings(response.json()).QuizRankings

    def get_recent_blogs(self, pageToken: str = None, start: int = 0, size: int = 25):
        params = {
            "pagingType": "t",
            "start": start,
            "size": size,
        }
        if pageToken:
            params["pageToken"] = pageToken

        response = self.session.get(f"/x{self.comId}/s/feed/blog-all", params=params)
        return objects.RecentBlogs(response.json()).RecentBlogs

    def get_notifications(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/notification?pagingType=t&start={start}&size={size}")
        return objects.NotificationList(response.json()["notificationList"]).NotificationList

    def get_notices(self, start: int = 0, size: int = 25):
        """
        :param start: Start of the List (Start: 0)
        :param size: Amount of Notices to Show
        :return: Notices List
        """
        response = self.session.get(f"/x{self.comId}/s/notice?type=usersV2&status=1&start={start}&size={size}")
        return objects.NoticeList(response.json()["noticeList"]).NoticeList

    def get_sticker_pack_info(self, sticker_pack_id: str):
        response = self.session.get(f"/x{self.comId}/s/sticker-collection/{sticker_pack_id}?includeStickers=true")
        return objects.StickerCollection(response.json()["stickerCollection"]).StickerCollection

    def get_sticker_packs(self):
        response = self.session.get(f"/x{self.comId}/s/sticker-collection?includeStickers=false&type=my-active-collection")
        return objects.StickerCollection(response.json()["stickerCollection"]).StickerCollection

    def get_store_chat_bubbles(self, start: int = 0, size: int = 25):
        params = {
            "sectionGroupId": "chat-bubble",
            "start": start,
            "size": size
        }
        response = self.session.get(f"/x{self.comId}/s/store/items", params=params)
        return objects.StoreChatBubble(response.json()).StoreChatBubble

    # TODO : Finish this
    def get_store_stickers(self, start: int = 0, size: int = 25):
        params = {
            "sectionGroupId": "sticker",
            "start": start,
            "size": size
        }

        return self.session.get(f"/x{self.comId}/s/store/items", params=params).json()

    def get_community_stickers(self):
        response = self.session.get(
            url=f"/x{self.comId}/s/sticker-collection",
            paams={ "type": "community-shared" }
        )
        return objects.CommunityStickerCollection(response.json()).CommunityStickerCollection

    def get_sticker_collection(self, collectionId: str):
        response = self.session.get(
            url=f"/x{self.comId}/s/sticker-collection/{collectionId}",
            parmas={ "includeStickers": True }
        )
        return objects.StickerCollection(response.json()["stickerCollection"]).StickerCollection

    def get_shared_folder_info(self):
        response = self.session.get(f"/x{self.comId}/s/shared-folder/stats")
        return objects.GetSharedFolderInfo(response.json()["stats"]).GetSharedFolderInfo

    def get_shared_folder_files(self, type: str = "latest", start: int = 0, size: int = 25):
        params = {
            "type": type,
            "start": start,
            "size": size
        }
        response = self.session.get(f"/x{self.comId}/s/shared-folder/files", params=params)
        return objects.SharedFolderFileList(response.json()["fileList"]).SharedFolderFileList

    #
    # MODERATION MENU
    #

    def moderation_history(self, userId: str = None, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, size: int = 25):
        types = {"userId": 0, "blogId": 1, "wikiId": 2, "quizId": 1, "fileId": 109}
        ids = (userId, blogId, wikiId, quizId, fileId)
        for id, type in zip(ids, types.values()):
            if id:
                url = f"/x{self.comId}/s/admin/operation?objectId={id}&objectType={type}&pagingType=t&size={size}"
                break
        else:
            url = f"/x{self.comId}/s/admin/operation?pagingType=t&size={size}"
        return objects.AdminLogList(self.session.get(url).json()["adminLogList"]).AdminLogList

    def feature(self, time: int, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None):
        time_map = {1: 3600, 2: 7200, 3: 10800} if chatId else {1: 86400, 2: 172800, 3: 259200}
        if time not in time_map:
            raise exceptions.WrongType(time)

        data = {
            "adminOpName": 114,
            "adminOpValue": {
                "featuredDuration": time_map[time],
                "featuredType": 5 if chatId else 4 if userId else 1
            }
        }

        url = f"/x{self.comId}/s/"
        if userId:
            url += f"user-profile/{userId}/admin"
        elif blogId:
            url += f"blog/{blogId}/admin"
        elif wikiId:
            url += f"item/{wikiId}/admin"
        elif chatId:
            url += f"chat/thread/{chatId}/admin"
        else:
            raise exceptions.SpecifyType

        return self.session.post(url, json=data).json()

    def unfeature(self, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None):
        data = {
            "adminOpName": 114,
            "adminOpValue": {"featuredType": 0}
        }

        if userId:
            url = f"/x{self.comId}/s/user-profile/{userId}/admin"

        elif blogId:
            url = f"/x{self.comId}/s/blog/{blogId}/admin"

        elif wikiId:
            url = f"/x{self.comId}/s/item/{wikiId}/admin"

        elif chatId:
            url = f"/x{self.comId}/s/chat/thread/{chatId}/admin"

        else: raise exceptions.SpecifyType

        return self.session.post(url, json=data).json()

    def hide(self, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, reason: str = None):
        data = {
            "adminOpNote": {
                "content": reason
            }
        }

        if userId:
            data["adminOpName"] = 18

            url = f"/x{self.comId}/s/user-profile/{userId}/admin"

        elif blogId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
            url = f"/x{self.comId}/s/blog/{blogId}/admin"

        elif quizId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9

            url = f"/x{self.comId}/s/blog/{quizId}/admin"

        elif wikiId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
            url = f"/x{self.comId}/s/item/{wikiId}/admin"

        elif chatId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
            url = f"/x{self.comId}/s/chat/thread/{chatId}/admin"

        elif fileId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9

            url = f"/x{self.comId}/s/shared-folder/files/{fileId}/admin"

        else: raise exceptions.SpecifyType

        return self.session.post(url, json=data).json()

    def unhide(self, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None, quizId: str = None, fileId: str = None, reason: str = None):
        data = {
            "adminOpNote": {
                "content": reason
            }
        }

        if userId:
            data["adminOpName"] = 19
            url = f"/x{self.comId}/s/user-profile/{userId}/admin"

        elif blogId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0

            url = f"/x{self.comId}/s/blog/{blogId}/admin"

        elif quizId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0

            url = f"/x{self.comId}/s/blog/{quizId}/admin"

        elif wikiId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0

            url = f"/x{self.comId}/s/item/{wikiId}/admin"

        elif chatId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0

            url = f"/x{self.comId}/s/chat/thread/{chatId}/admin"

        elif fileId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0

            url = f"/x{self.comId}/s/shared-folder/files/{fileId}/admin"

        else: raise exceptions.SpecifyType

        return self.session.post(url, json=data).json()

    def edit_titles(self, userId: str, tlt: list):

        data = {
            "adminOpName": 207,
            "adminOpValue": {
                "titles": tlt
            }
        }

        return self.session.post(f"/x{self.comId}/s/user-profile/{userId}/admin", json=data)

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

        return self.session.post(f"/x{self.comId}/s/notice", json=data).json()

    # TODO : List all strike texts
    def strike(self, userId: str, time: int, title: str = None, reason: str = None):
        time_map = {1: 86400, 2: 10800, 3: 21600, 4: 43200, 5: 86400}
        if time not in time_map:
            raise exceptions.WrongType(time)

        data = {
            "uid": userId,
            "title": title,
            "content": reason,
            "attachedObject": {
                "objectId": userId,
                "objectType": 0
            },
            "penaltyType": 1,
            "penaltyValue": time_map[time],
            "adminOpNote": {},
            "noticeType": 4
        }

        return self.session.post(f"/x{self.comId}/s/notice", json=data).json()

    def ban(self, userId: str, reason: str, banType: int = None):
        data = {
            "reasonType": banType,
            "note": {
                "content": reason
            }
        }

        return self.session.post(f"/x{self.comId}/s/user-profile/{userId}/ban", json=data).json()

    def unban(self, userId: str, reason: str):
        data = {
            "note": {
                "content": reason
            }
        }

        return self.session.post(f"/x{self.comId}/s/user-profile/{userId}/unban", json=data).json()

    def reorder_featured_users(self, userIds: list):
        data = { "uidList": userIds }

        response = self.session.post(f"/x{self.comId}/s/user-profile/featured/reorder", json=data)
        return response.json()

    def get_hidden_blogs(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/feed/blog-disabled?start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_featured_users(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/user-profile?type=featured&start={start}&size={size}")
        return objects.UserProfileCountList(response.json()).UserProfileCountList

    def review_quiz_questions(self, quizId: str):
        response = self.session.get(f"/x{self.comId}/s/blog/{quizId}?action=review")
        return objects.QuizQuestionList(response.json()["blog"]["quizQuestionList"]).QuizQuestionList

    def get_recent_quiz(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/blog?type=quizzes-recent&start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_trending_quiz(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/feed/quiz-trending?start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    def get_best_quiz(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/feed/quiz-best-quizzes?start={start}&size={size}")
        return objects.BlogList(response.json()["blogList"]).BlogList

    # Provided by "spectrum#4691"
    def apply_avatar_frame(self, avatarId: str, applyToAll: bool = True):
        """
        Apply avatar frame.

        **Parameters**
            - **avatarId** : ID of the avatar frame.
            - **applyToAll** : Apply to all.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`

        """

        data = {
            "frameId": avatarId,
            "applyToAll": int(applyToAll),
        }

        return self.session.post(f"/x{self.comId}/s/avatar-frame/apply", json=data).status_code

    def add_poll_option(self, blogId: str, question: str):
        data = {
            "mediaList": None,
            "title": question,
            "type": 0
        }

        response = self.session.post(f"/x{self.comId}/s/blog/{blogId}/poll/option", json=data)
        return response.status_code

    def create_wiki_category(self, title: str, parentCategoryId: str, media: list = None):
        data = {
            "icon": None,
            "label": title,
            "mediaList": media,
            "parentCategoryId": parentCategoryId,
        }

        return self.session.post(f"/x{self.comId}/s/item-category", json=data).status_code

    def create_shared_folder(self,title: str):
        data = {"title": title}
        return self.session.post(f"/x{self.comId}/s/shared-folder/folders", json=data).status_code

    def submit_to_wiki(self, wikiId: str, message: str):
        data = {
            "message": message,
            "itemId": wikiId
        }

        return self.session.post(f"/x{self.comId}/s/knowledge-base-request", json=data).status_code

    def accept_wiki_request(self, requestId: str, destinationCategoryIdList: list):
        data = {
            "destinationCategoryIdList": destinationCategoryIdList,
            "actionType": "create"
        }

        response = self.session.post(f"/x{self.comId}/s/knowledge-base-request/{requestId}/approve", json=data)
        return response.status_code

    def reject_wiki_request(self, requestId: str):
        response = self.session.post(f"/x{self.comId}/s/knowledge-base-request/{requestId}/reject", json={})
        return response.status_code

    def get_wiki_submissions(self, start: int = 0, size: int = 25):
        response = self.session.get(f"/x{self.comId}/s/knowledge-base-request?type=all&start={start}&size={size}")
        return objects.WikiRequestList(response.json()["knowledgeBaseRequestList"]).WikiRequestList

    def get_live_layer(self):
        response = self.session.get(f"/x{self.comId}/s/live-layer/homepage?v=2")
        return objects.LiveLayer(response.json()["liveLayerList"]).LiveLayer

    def apply_bubble(self, bubbleId: str, chatId: str, applyToAll: bool = False):
        data = {
            "applyToAll": int(applyToAll),
            "bubbleId": bubbleId,
            "threadId": chatId,
        }

        response = self.session.post(f"/x{self.comId}/s/chat/thread/apply-bubble", json=data)
        return response.status_code