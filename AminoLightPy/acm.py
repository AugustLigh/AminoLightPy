from typing import BinaryIO
from requests import Session
from time import time as timestamp

from .lib.util import exceptions, objects
from .constants import api, device_id, upload_media

class ACM():
    def __init__(self, comId: int = None, *, profile: objects.UserProfile):
        self.session: Session = profile.session
        self.profile = profile
        self.comId = comId

    # TODO : Finish the imaging sizing, might not work for every picture...
    def create_community(self, name: str, tagline: str, icon: BinaryIO, themeColor: str, joinType: int = 0, primaryLanguage: str = "en"):
        data = {
            "icon": {
                "height": 512.0,
                "imageMatrix": [1.6875, 0.0, 108.0, 0.0, 1.6875, 497.0, 0.0, 0.0, 1.0],
                "path": upload_media(self, icon),
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
        response = self.session.get(f"{api}/g/s/community/managed?start={start}&size={size}")
        return objects.CommunityList(response.json()["communityList"]).CommunityList

    def get_categories(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/blog-category?start={start}&size={size}")
        return response.json()

    def change_sidepanel_color(self, color: str):
        data = {
            "path": "appearance.leftSidePanel.style.iconColor",
            "value": color
        }

        response = self.session.post(f"{api}/x{self.comId}/s/community/configuration", json=data)
        return response.json()

    def promote(self, userId: str, rank: str):
        rank = rank.lower().replace("agent", "transfer-agent")

        if rank.lower() not in ["transfer-agent", "leader", "curator"]:
            raise exceptions.WrongType(rank)

        response = self.session.post(f"{api}/x{self.comId}/s/user-profile/{userId}/{rank}")
        return response.status_code

    def get_join_requests(self, start: int = 0, size: int = 25):
        data = {
            "status": "pending",
            "start": start,
            "size": size
        }
        
        response = self.session.get(f"{api}/x{self.comId}/s/community/membership-request", params=data)
        return objects.JoinRequest(response.json()).JoinRequest

    def accept_join_request(self, userId: str):
        data = dict()
        response = self.session.post(f"{api}/x{self.comId}/s/community/membership-request/{userId}/accept", json=data)
        return response.status_code

    def reject_join_request(self, userId: str):
        data = dict()
        response = self.session.post(f"{api}/x{self.comId}/s/community/membership-request/{userId}/reject", json=data)
        return response.status_code

    def get_community_stats(self):
        response = self.session.get(f"{api}/x{self.comId}/s/community/stats")
        if response.status_code != 200: return exceptions.CheckException(response.text)
        else: return objects.CommunityStats(response.json()["communityStats"]).CommunityStats

    def get_community_user_stats(self, type: str, start: int = 0, size: int = 25):
        if type.lower() == "leader": target = "leader"
        elif type.lower() == "curator": target = "curator"
        else: raise exceptions.WrongType(type)

        data = {
            "type": target,
            "start": start,
            "size": size
        }

        response = self.session.get(f"{api}/x{self.comId}/s/community/stats/moderation", params=data)
        return objects.UserProfileList(response.json()["userProfileList"]).UserProfileList

    def change_welcome_message(self, message: str, isEnabled: bool = True):
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
        data = { "content": message }
        
        response = self.session.post(f"{api}/x{self.comId}/s/community/guideline", json=data)
        return response.status_code

    def edit_community(self, name: str = None, description: str = None, aminoId: str = None, primaryLanguage: str = None, themePackUrl: str = None):
        data = {"timestamp": int(timestamp() * 1000)}

        if name is not None: data["name"] = name
        if description is not None: data["content"] = description
        if aminoId is not None: data["endpoint"] = aminoId
        if primaryLanguage is not None: data["primaryLanguage"] = primaryLanguage
        if themePackUrl is not None: data["themePackUrl"] = themePackUrl
        
        response = self.session.post(f"{api}/x{self.comId}/s/community/settings", json=data)
        return response.status_code

    def change_module(self, module: str, isEnabled: bool):
        if module.lower() == "chat": mod = "module.chat.enabled"
        elif module.lower() == "livechat": mod = "module.chat.avChat.videoEnabled"
        elif module.lower() == "screeningroom": mod = "module.chat.avChat.screeningRoomEnabled"
        elif module.lower() == "publicchats": mod = "module.chat.publicChat.enabled"
        elif module.lower() == "posts": mod = "module.post.enabled"
        elif module.lower() == "ranking": mod = "module.ranking.enabled"
        elif module.lower() == "leaderboards": mod = "module.ranking.leaderboardEnabled"
        elif module.lower() == "featured": mod = "module.featured.enabled"
        elif module.lower() == "featuredposts": mod = "module.featured.postEnabled"
        elif module.lower() == "featuredusers": mod = "module.featured.memberEnabled"
        elif module.lower() == "featuredchats": mod = "module.featured.publicChatRoomEnabled"
        elif module.lower() == "sharedfolder": mod = "module.sharedFolder.enabled"
        elif module.lower() == "influencer": mod = "module.influencer.enabled"
        elif module.lower() == "catalog": mod = "module.catalog.enabled"
        elif module.lower() == "externalcontent": mod = "module.externalContent.enabled"
        elif module.lower() == "topiccategories": mod = "module.topicCategories.enabled"
        else: raise exceptions.SpecifyType()

        data = {
            "path": mod,
            "value": isEnabled
        }

        response = self.session.post(f"{api}/x{self.comId}/s/community/configuration", json=data)
        return response.status_code

    def add_influencer(self, userId: str, monthlyFee: int):
        data = {
            "monthlyFee": monthlyFee
        }

        response = self.session.post(f"{api}/x{self.comId}/s/influencer/{userId}", json=data)
        return response.status_code

    def remove_influencer(self, userId: str):
        response = self.session.delete(f"{api}/x{self.comId}/s/influencer/{userId}")
        return response.status_code

    def get_notice_list(self, start: int = 0, size: int = 25):
        response = self.session.get(f"{api}/x{self.comId}/s/notice?type=management&status=1&start={start}&size={size}")
        return objects.NoticeList(response.json()["noticeList"]).NoticeList

    def delete_pending_role(self, noticeId: str):
        response = self.session.delete(f"{api}/x{self.comId}/s/notice/{noticeId}")
        return response.status_code
