# pylint: disable=invalid-name

from time import time as timestamp
from typing import BinaryIO
from requests import Session

from .lib.util import exceptions, objects
from .constants import api, device_id, upload_media

class ACM():
    "Module for work with ACM requests."
    def __init__(self, comId: int = None, *, profile: objects.UserProfile):
        self.session: Session = profile.session
        self.profile = profile
        self.comId = comId

    # TODO : Finish the imaging sizing, might not work for every picture...
    def create_community(self, name: str, tagline: str, icon: BinaryIO,
                themeColor: str, joinType: int = 0, primaryLanguage: str = "en"):
        """
        Creates a community with the given parameters.

        **Parameters**
            - **name** (str): The name of the community.
            - **tagline** (str): The tagline of the community.
            - **icon** (BinaryIO): The icon of the community in BinaryIO format.
            - **themeColor** (str): The theme color of the community.
            - **joinType** (int, optional): The type of joining the community. Defaults to 0.
            - **primaryLanguage** (str, optional): The primary language of the community. Defaults to "en".

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "icon": {
                "height": 512.0,
                "imageMatrix": [1.6875, 0.0, 108.0, 0.0, 1.6875, 497.0, 0.0, 0.0, 1.0],
                "path": upload_media(self, icon, "image/jpeg"),
                "width": 512.0,
                "x": 0.0,
                "y": 0.0
            },
            "joinType": joinType,
            "name": name,
            "primaryLanguage": primaryLanguage,
            "tagline": tagline,
            "templateId": 9,
            "themeColor": themeColor
        }

        response = self.session.post(f"{api}/g/s/community", json=data)
        return response.status_code

    def delete_community(self, email: str, password: str, verificationCode: str):
        """
        Deletes a community with the given parameters.

        **Parameters**
            - **email** (str): The email address associated with the community.
            - **password** (str): The password associated with the community.
            - **verificationCode** (str): The verification code with mail.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "secret": f"0 {password}",
            "validationContext": {
                "data": {
                    "code": verificationCode
                },
                "type": 1,
                "identity": email
            },
            "deviceID": device_id
        }

        response = self.session.post(f"{api}/g/s-x{self.comId}/community/delete-request", json=data)
        return response.status_code

    def list_communities(self, start: int = 0, size: int = 25):
        """
        List of Communities the account is admin.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Community List <AminoLightPy.lib.util.objects.CommunityList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """

        response = self.session.get(f"{api}/g/s/community/managed?start={start}&size={size}")
        return objects.CommunityList(response.json()["communityList"]).CommunityList

    def get_categories(self, start: int = 0, size: int = 25):
        """
        Gets the categories of the blog in the community.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`dict`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """

        response = self.session.get(f"{api}/x{self.comId}/s/blog-category?start={start}&size={size}")
        return response.json()

    def change_sidepanel_color(self, color: str):
        """
        Changes the color of the side panel in the community.

        **Parameters**
            - *color* : The color to be applied to the side panel.

        **Returns**
            - **Success** : :meth:`dict`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """

        data = {
            "path": "appearance.leftSidePanel.style.iconColor",
            "value": color
        }

        response = self.session.post(f"{api}/x{self.comId}/s/community/configuration", json=data)
        return response.json()

    def promote(self, userId: str, rank: str):
        """
        Promotes a user to a specified rank in the community.

        **Parameters**
            - *userId* : The ID of the user to be promoted.
            - *rank* : The rank to which the user is to be promoted. Can be "transfer-agent", "leader", or "curator".

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        rank = rank.lower().replace("agent", "transfer-agent")

        if rank.lower() not in ["transfer-agent", "leader", "curator"]:
            raise exceptions.WrongType(rank)

        response = self.session.post(f"{api}/x{self.comId}/s/user-profile/{userId}/{rank}")
        return response.status_code

    def get_join_requests(self, start: int = 0, size: int = 25):
        """
        Retrieves the join requests for the community.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Join Request <AminoLightPy.lib.util.objects.JoinRequest>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "status": "pending",
            "start": start,
            "size": size
        }

        response = self.session.get(f"{api}/x{self.comId}/s/community/membership-request", params=data)
        return objects.JoinRequest(response.json()).JoinRequest

    def accept_join_request(self, userId: str):
        """
        Accepts a join request from a user in the community.

        **Parameters**
            - *userId* : The ID of the user whose join request is to be accepted.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {}
        response = self.session.post(f"{api}/x{self.comId}/s/community/membership-request/{userId}/accept", json=data)
        return response.status_code

    def reject_join_request(self, userId: str):
        """
        Rejects a join request from a user in the community.

        **Parameters**
            - *userId* : The ID of the user whose join request is to be rejected.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {}
        response = self.session.post(f"{api}/x{self.comId}/s/community/membership-request/{userId}/reject", json=data)
        return response.status_code

    def get_community_stats(self):
        """
        Retrieves the statistics of the community.

        **Returns**
            - **Success** : :meth:`Community Stats <AminoLightPy.lib.util.objects.CommunityStats>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.get(f"{api}/x{self.comId}/s/community/stats")
        if response.status_code != 200: return exceptions.CheckException(response.text)
        else: return objects.CommunityStats(response.json()["communityStats"]).CommunityStats

    def get_community_user_stats(self, type: str, start: int = 0, size: int = 25):
        """
        Retrieves the user statistics of the community based on the specified type.

        **Parameters**
            - *type* : The type of user statistics to be retrieved. Can be "leader" or "curator".
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`User Profile List <AminoLightPy.lib.util.objects.UserProfileList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if type.lower() == "leader":
            target = "leader"
        elif type.lower() == "curator":
            target = "curator"
        else: raise exceptions.WrongType(type)

        data = {
            "type": target,
            "start": start,
            "size": size
        }

        response = self.session.get(
            url=f"{api}/x{self.comId}/s/community/stats/moderation",
            params=data
        )
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList

    def change_welcome_message(self, message: str, isEnabled: bool = True):
        """
        Changes the welcome message of the community.

        **Parameters**
            - *message* : The new welcome message for the community.
            - *isEnabled* : Whether the welcome message is enabled or not.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "path": "general.welcomeMessage",
            "value": {
                "enabled": isEnabled,
                "text": message
            }
        }

        response = self.session.post(f"{api}/x{self.comId}/s/community/configuration", json=data)
        return response.status_code

    def change_guidelines(self, message: str):
        """
        Changes the guidelines of the community.

        **Parameters**
            - *message* : The new guidelines for the community.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = { "content": message }
        
        response = self.session.post(f"{api}/x{self.comId}/s/community/guideline", json=data)
        return response.status_code

    def edit_community(self, name: str = None, description: str = None, aminoId: str = None, primaryLanguage: str = None, themePackUrl: str = None):
        """
        Edits the community settings with the given parameters.

        **Parameters**
            - *name* : The new name of the community. If not provided, the current name will be kept.
            - *description* : The new description of the community. If not provided, the current description will be kept.
            - *aminoId* : The new Amino ID of the community. If not provided, the current Amino ID will be kept.
            - *primaryLanguage* : The new primary language of the community. If not provided, the current primary language will be kept.
            - *themePackUrl* : The new theme pack URL of the community. If not provided, the current theme pack URL will be kept.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {"timestamp": int(timestamp() * 1000)}

        if name is not None:
            data["name"] = name
        if description is not None:
            data["content"] = description
        if aminoId is not None:
            data["endpoint"] = aminoId
        if primaryLanguage is not None:
            data["primaryLanguage"] = primaryLanguage
        if themePackUrl is not None:
            data["themePackUrl"] = themePackUrl

        response = self.session.post(f"{api}/x{self.comId}/s/community/settings", json=data)
        return response.status_code

    def change_module(self, module: str, isEnabled: bool):
        """
        Changes the status of a specified module in the community.

        **Parameters**
            - *module* : The module to be changed. Can be one of the following: "chat", "livechat", "screeningroom", "publicchats", "posts", "ranking", "leaderboards", "featured", "featuredposts", "featuredusers", "featuredchats", "sharedfolder", "influencer", "catalog", "externalcontent", "topiccategories".
            - *isEnabled* : The status to be applied to the module. True for enabled, False for disabled.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        if module.lower() == "chat":
            mod = "module.chat.enabled"
        elif module.lower() == "livechat":
            mod = "module.chat.avChat.videoEnabled"
        elif module.lower() == "screeningroom":
            mod = "module.chat.avChat.screeningRoomEnabled"
        elif module.lower() == "publicchats":
            mod = "module.chat.publicChat.enabled"
        elif module.lower() == "posts":
            mod = "module.post.enabled"
        elif module.lower() == "ranking":
            mod = "module.ranking.enabled"
        elif module.lower() == "leaderboards":
            mod = "module.ranking.leaderboardEnabled"
        elif module.lower() == "featured":
            mod = "module.featured.enabled"
        elif module.lower() == "featuredposts":
            mod = "module.featured.postEnabled"
        elif module.lower() == "featuredusers":
            mod = "module.featured.memberEnabled"
        elif module.lower() == "featuredchats":
            mod = "module.featured.publicChatRoomEnabled"
        elif module.lower() == "sharedfolder":
            mod = "module.sharedFolder.enabled"
        elif module.lower() == "influencer":
            mod = "module.influencer.enabled"
        elif module.lower() == "catalog":
            mod = "module.catalog.enabled"
        elif module.lower() == "externalcontent":
            mod = "module.externalContent.enabled"
        elif module.lower() == "topiccategories":
            mod = "module.topicCategories.enabled"
        else:
            raise exceptions.SpecifyType()

        data = {
            "path": mod,
            "value": isEnabled
        }

        response = self.session.post(f"{api}/x{self.comId}/s/community/configuration", json=data)
        return response.status_code

    def add_influencer(self, userId: str, monthlyFee: int):
        """
        Adds a user as an influencer in the community.

        **Parameters**
            - *userId* : The ID of the user to be added as an influencer.
            - *monthlyFee* : The monthly fee for the influencer.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        data = {
            "monthlyFee": monthlyFee
        }

        response = self.session.post(f"{api}/x{self.comId}/s/influencer/{userId}", json=data)
        return response.status_code

    def remove_influencer(self, userId: str):
        """
        Removes a user from being an influencer in the community.

        **Parameters**
            - *userId* : The ID of the user to be removed from being an influencer.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.delete(f"{api}/x{self.comId}/s/influencer/{userId}")
        return response.status_code

    def get_notice_list(self, start: int = 0, size: int = 25):
        """
        Retrieves the list of notices in the community.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **Success** : :meth:`Notice List <AminoLightPy.lib.util.objects.NoticeList>`

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        params = {
            "type": "management",
            "status": "1",
            "start": start,
            "size": size
        }
        response = self.session.get(f"{api}/x{self.comId}/s/notice", params=params)
        return objects.NoticeList(response.json()["noticeList"]).NoticeList

    def delete_pending_role(self, noticeId: str):
        """
        Deletes a pending role with the given notice ID.

        **Parameters**
            - *noticeId* : The ID of the notice for the pending role.

        **Returns**
            - **Success** : 200 (int)

            - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
        """
        response = self.session.delete(f"{api}/x{self.comId}/s/notice/{noticeId}")
        return response.status_code
