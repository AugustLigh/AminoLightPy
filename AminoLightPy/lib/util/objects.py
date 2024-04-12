# pylint: disable=invalid-name
# You don't even know how long this shit took...
# F*ck you Sand for making me do this.

from typing import List, Optional, Dict, TypeVar

class UserProfile:
    __slots__ = (
        "json", "fanClub", "accountMembershipStatus", "activation", "activePublicLiveThreadId",
        "age", "aminoId", "aminoIdEditable", "avatarFrame", "avatarFrameId",
        "blogsCount", "commentsCount", "content", "createdTime",
        "followersCount", "followingCount", "followingStatus", "gender",
        "icon", "isGlobal", "isNicknameVerified", "itemsCount", "level",
        "mediaList", "membershipStatus", "modifiedTime", "mood", "moodSticker", "nickname",
        "notificationSubscriptionStatus", "onlineStatus", "onlineStatus2",
        "postsCount", "pushEnabled", "race", "reputation", "role", "securityLevel",
        "status", "storiesCount", "tagList", "userId", "verified",
        "totalQuizHighestScore", "totalQuizPlayedTimes", "requestId", "message", "applicant",
        "avgDailySpendTimeIn7Days", "adminLogCountIn7Days", "extensions", "style",
        "backgroundImage", "backgroundColor", "coverAnimation", "customTitles", "defaultBubbleId",
        "disabledLevel", "disabledStatus", "disabledTime", "isMemberOfTeamAmino",
        "privilegeOfChatInviteRequest", "privilegeOfCommentOnUserProfile", "influencerInfo",
        "fansCount", "influencerCreatedTime", "influencerMonthlyFee", "influencerPinned",
        "staffInfo", "globalStrikeCount", "lastStrikeTime", "lastWarningTime", "strikeCount",
        "warningCount", "session"
    )

    def __init__(self, data: Dict):
        if data is None:
            for attr in self.__slots__:
                setattr(self, attr, None)

            return

        self.json: Optional[Dict] = data

        self.fanClub = FanClubList(data.get("fanClubList", [])).FanClubList

        self.accountMembershipStatus: Optional[int] = data.get("accountMembershipStatus")
        self.activation: Optional[int] = data.get("activation")
        self.activePublicLiveThreadId: Optional[str] = data.get("activePublicLiveThreadId")
        self.age: Optional[int] = data.get("age")
        self.aminoId: Optional[str] = data.get("aminoId")
        self.aminoIdEditable: Optional[bool] = data.get("aminoIdEditable")
        self.avatarFrame: Optional[str] = data.get("avatarFrame")
        self.avatarFrameId: Optional[str] = data.get("avatarFrameId")
        self.blogsCount: Optional[int] = data.get("blogsCount")
        self.commentsCount: Optional[int] = data.get("commentsCount")
        self.content: Optional[str] = data.get("content")
        self.createdTime: Optional[int] = data.get("createdTime")
        self.followersCount: Optional[int] = data.get("followersCount")
        self.followingCount: Optional[int] = data.get("followingCount")
        self.followingStatus: Optional[int] = data.get("followingStatus")
        self.gender: Optional[str] = data.get("gender")
        self.icon: Optional[str] = data.get("icon")
        self.isGlobal: Optional[bool] = data.get("isGlobal")
        self.isNicknameVerified: Optional[bool] = data.get("isNicknameVerified")
        self.itemsCount: Optional[int] = data.get("itemsCount")
        self.level: Optional[int] = data.get("level")
        self.mediaList: Optional[MediaObject] = data.get("mediaList")
        self.membershipStatus: Optional[int] = data.get("membershipStatus")
        self.modifiedTime: Optional[int] = data.get("modifiedTime")
        self.mood: Optional[str] = data.get("mood")
        self.moodSticker: Optional[str] = data.get("moodSticker")
        self.nickname: Optional[str] = data.get("nickname")
        self.notificationSubscriptionStatus: Optional[int] = data.get("notificationSubscriptionStatus")
        self.onlineStatus: Optional[int] = data.get("onlineStatus")
        self.onlineStatus2: Optional[int] = data.get("onlineStatus2")
        self.postsCount: Optional[int] = data.get("postsCount")
        self.pushEnabled: Optional[bool] = data.get("pushEnabled")
        self.race: Optional[str] = data.get("race")
        self.reputation: Optional[int] = data.get("reputation")
        self.role: Optional[str] = data.get("role")
        self.securityLevel: Optional[int] = data.get("securityLevel")
        self.status: Optional[str] = data.get("status")
        self.storiesCount: Optional[int] = data.get("storiesCount")
        self.tagList: Optional[List[str]] = data.get("tagList")
        self.userId: Optional[str] = data.get("uid")
        self.verified: Optional[bool] = data.get("verified")
        self.totalQuizHighestScore: Optional[int] = data.get("totalQuizHighestScore")
        self.totalQuizPlayedTimes: Optional[int] = data.get("totalQuizPlayedTimes")
        self.requestId: Optional[str] = data.get("requestId")
        self.message: Optional[str] = data.get("message")
        self.applicant: Optional[str] = data.get("applicant")
        self.avgDailySpendTimeIn7Days: Optional[int] = data.get("avgDailySpendTimeIn7Days")
        self.adminLogCountIn7Days: Optional[int] = data.get("adminLogCountIn7Days")

        # extensions
        self.extensions: Optional[Dict] = data.get("extensions") or {}
        # style
        self.style: Optional[Dict] = self.extensions.get("style") or {}
        self.backgroundImage: Optional[str] = self.style.get("backgroundImage")
        self.backgroundColor: Optional[str] = self.style.get("backgroundColor")

        self.coverAnimation: Optional[str] = self.extensions.get("coverAnimation")
        self.customTitles: Optional[List[str]] = self.extensions.get("customTitles")
        self.defaultBubbleId: Optional[str] = self.extensions.get("defaultBubbleId")
        self.disabledLevel: Optional[int] = self.extensions.get("__disabledLevel__")
        self.disabledStatus: Optional[str] = self.extensions.get("__disabledStatus__")
        self.disabledTime: Optional[int] = self.extensions.get("__disabledTime__")
        self.isMemberOfTeamAmino: Optional[bool] = self.extensions.get("isMemberOfTeamAmino")
        self.privilegeOfChatInviteRequest: Optional[bool] = self.extensions.get("privilegeOfChatInviteRequest")
        self.privilegeOfCommentOnUserProfile: Optional[bool] = self.extensions.get("privilegeOfCommentOnUserProfile")

        # influencerInfo
        self.influencerInfo: Optional[Dict] = data.get("influencerInfo") or {}
        self.fansCount: Optional[int] = self.influencerInfo.get("fansCount")
        self.influencerCreatedTime: Optional[int] = self.influencerInfo.get("createdTime")
        self.influencerMonthlyFee: Optional[int] = data.get("monthlyFee")
        self.influencerPinned: Optional[bool] = data.get("pinned")

        # adminInfo
        self.staffInfo: Optional[Dict] = data.get("adminInfo") or {}
        self.globalStrikeCount: Optional[int] = self.staffInfo.get("globalStrikeCount")
        self.lastStrikeTime: Optional[int] = self.staffInfo.get("lastStrikeTime")
        self.lastWarningTime: Optional[int] = self.staffInfo.get("lastWarningTime")
        self.strikeCount: Optional[int] = self.staffInfo.get("strikeCount")
        self.warningCount: Optional[int] = self.staffInfo.get("warningCount")

        self.session = None

    @property
    def UserProfile(self):

        return self

class UserProfileList:
    __slots__ = UserProfile.__slots__

    def __init__(self, data):
        self.json = data
        _userObjects = tuple(UserProfile(x).UserProfile for x in data)

        set_attributes(self, _userObjects)

    @property
    def UserProfileList(self):
        return self

class BlogList:
    def __init__(self, data, nextPageToken = None, prevPageToken = None):
        _author, _quizQuestionList = [], []

        self.json = data
        self.nextPageToken = nextPageToken
        self.prevPageToken = prevPageToken

        for y in data:
            _author.append(y.get("author"))
            _quizQuestionList.append(QuizQuestionList(y.get("quizQuestionList", [])).QuizQuestionList)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.quizQuestionList = _quizQuestionList

        self.createdTime = []
        self.globalVotesCount = []
        self.globalVotedValue = []
        self.keywords = []
        self.mediaList: Optional[List[MediaObject]] = []
        self.style = []
        self.totalQuizPlayCount = []
        self.title = []
        self.tipInfo = []
        self.tippersCount = []
        self.tippable = []
        self.tippedCoins = []
        self.contentRating = []
        self.needHidden = []
        self.guestVotesCount = []
        self.type = []
        self.status = []
        self.globalCommentsCount = []
        self.modifiedTime = []
        self.widgetDisplayInterval = []
        self.totalPollVoteCount = []
        self.blogId = []
        self.viewCount = []
        self.fansOnly = []
        self.votesCount = []
        self.endTime = []
        self.refObjectId = []
        self.refObject = []
        self.votedValue = []
        self.extensions = []
        self.commentsCount = []
        self.content = []
        self.featuredType = []
        self.shareUrl = []
        self.disabledTime = []
        self.quizPlayedTimes = []
        self.quizTotalQuestionCount = []
        self.quizTrendingTimes = []
        self.quizLastAddQuestionTime = []
        self.isIntroPost = []

    @property
    def BlogList(self):
        for x in self.json:
            tipInfo = x.get("tipInfo") or {}
            extensions = x.get("extensions") or {}

            self.globalVotesCount.append(x.get("globalVotesCount"))
            self.globalVotedValue.append(x.get("globalVotedValue"))
            self.keywords.append(x.get("keywords"))
            self.mediaList.append(x.get("mediaList"))
            self.style.append(x.get("style"))
            self.totalQuizPlayCount.append(x.get("totalQuizPlayCount"))
            self.title.append(x.get("title"))
            self.contentRating.append(x.get("contentRating"))
            self.needHidden.append(x.get("needHidden"))
            self.guestVotesCount.append(x.get("guestVotesCount"))
            self.type.append(x.get("type"))
            self.status.append(x.get("status"))
            self.globalCommentsCount.append(x.get("globalCommentsCount"))
            self.modifiedTime.append(x.get("modifiedTime"))
            self.widgetDisplayInterval.append(x.get("widgetDisplayInterval"))
            self.totalPollVoteCount.append(x.get("totalPollVoteCount"))
            self.blogId.append(x.get("blogId"))
            self.viewCount.append(x.get("viewCount"))
            self.votesCount.append(x.get("votesCount"))
            self.endTime.append(x.get("endTime"))
            self.refObjectId.append(x.get("refObjectId"))
            self.refObject.append(x.get("refObject"))
            self.votedValue.append(x.get("votedValue"))
            self.content.append(x.get("content"))
            self.createdTime.append(x.get("createdTime"))
            self.shareUrl.append(x.get("shareURLFullPath"))
            self.commentsCount.append(x.get("commentsCount"))

            # tip info
            self.tipInfo.append(tipInfo)
            self.tippersCount.append(tipInfo.get("tippersCount"))
            self.tippable.append(tipInfo.get("tippable"))
            self.tippedCoins.append(tipInfo.get("tippedCoins"))

            # extensions
            self.extensions.append(extensions)
            self.fansOnly.append(extensions.get("fansOnly"))
            self.featuredType.append(extensions.get("featuredType"))
            self.disabledTime.append(extensions.get("__disabledTime__"))
            self.quizPlayedTimes.append(extensions.get("quizPlayedTimes"))
            self.quizTotalQuestionCount.append(extensions.get("quizTotalQuestionCount"))
            self.quizTrendingTimes.append(extensions.get("quizTrendingTimes"))
            self.quizLastAddQuestionTime.append(extensions.get("quizLastAddQuestionTime"))
            self.isIntroPost.append(extensions.get("isIntroPost"))

        return self

class RecentBlogs:
    __slots__ = (
        'json', 
        'nextPageToken', 
        'prevPageToken'
    )

    def __init__(self, data):
        if data is None:
            for attr in self.__slots__:
                setattr(self, attr, None)

            return
        self.json = data

        self.nextPageToken = None
        self.prevPageToken = None

    @property
    def RecentBlogs(self):
        paging = self.json.get("paging") or {}
        self.nextPageToken = paging.get("nextPageToken")
        self.prevPageToken = paging.get("prevPageToken")

        return BlogList(self.json.get("blogList"), self.nextPageToken, self.prevPageToken).BlogList

class BlogCategoryList:
    def __init__(self, data):
        self.json = data
        self.status = []
        self.modifiedTime = []
        self.icon = []
        self.style = []
        self.title = []
        self.content = []
        self.createdTime = []
        self.position = []
        self.type = []
        self.categoryId = []
        self.blogsCount = []

    @property
    def BlogCategoryList(self):
        for x in self.json:
            self.status.append(x.get("status"))
            self.modifiedTime.append(x.get("modifiedTime"))
            self.icon.append(x.get("icon"))
            self.style.append(x.get("style"))
            self.title.append(x.get("label"))
            self.content.append(x.get("content"))
            self.createdTime.append(x.get("createdTime"))
            self.position.append(x.get("position"))
            self.type.append(x.get("type"))
            self.categoryId.append(x.get("categoryId"))
            self.blogsCount.append(x.get("blogsCount"))

        return self

class Blog:
    def __init__(self, data):
        self.json = data

        self.author: UserProfile = UserProfile(data.get("author", [])).UserProfile
        self.quizQuestionList: QuizQuestionList = QuizQuestionList(data.get("quizQuestionList", [])).QuizQuestionList

        extensions = self.json.get("extensions") or {}
        tipInfo = self.json.get("tipInfo") or {}
        style = extensions.get("style") or {}

        self.globalVotesCount = self.json.get("globalVotesCount")
        self.globalVotedValue = self.json.get("globalVotedValue")
        self.keywords = self.json.get("keywords")
        self.mediaList: Optional[MediaObject] = self.json.get("mediaList")
        self.style = self.json.get("style")
        self.totalQuizPlayCount = self.json.get("totalQuizPlayCount")
        self.title = self.json.get("title")
        self.tipInfo = tipInfo
        self.tippersCount = tipInfo.get("tippersCount")
        self.tippable = tipInfo.get("tippable")
        self.tippedCoins = tipInfo.get("tippedCoins")
        self.contentRating = self.json.get("contentRating")
        self.needHidden = self.json.get("needHidden")
        self.guestVotesCount = self.json.get("guestVotesCount")
        self.type = self.json.get("type")
        self.status = self.json.get("status")
        self.globalCommentsCount = self.json.get("globalCommentsCount")
        self.modifiedTime = self.json.get("modifiedTime")
        self.widgetDisplayInterval = self.json.get("widgetDisplayInterval")
        self.totalPollVoteCount = self.json.get("totalPollVoteCount")
        self.blogId = self.json.get("blogId")
        self.comId = self.json.get("ndcId")
        self.viewCount = self.json.get("viewCount")
        self.shareUrl = self.json.get("shareURLFullPath")
        self.fansOnly = extensions.get("fansOnly")
        self.backgroundColor = style.get("backgroundColor")
        self.votesCount = self.json.get("votesCount")
        self.endTime = self.json.get("endTime")
        self.refObjectId = self.json.get("refObjectId")
        self.refObject = self.json.get("refObject")
        self.votedValue = self.json.get("votedValue")
        self.content = self.json.get("content")
        self.createdTime = self.json.get("createdTime")
        self.extensions = extensions
        self.commentsCount = self.json.get("commentsCount")
        self.featuredType = extensions.get("featuredType")
        self.disabledTime = extensions.get("__disabledTime__")
        self.quizPlayedTimes = extensions.get("quizPlayedTimes")
        self.quizTotalQuestionCount = extensions.get("quizTotalQuestionCount")
        self.quizTrendingTimes = extensions.get("quizTrendingTimes")
        self.quizLastAddQuestionTime = extensions.get("quizLastAddQuestionTime")
        self.isIntroPost = extensions.get("isIntroPost")

    @property
    def Blog(self):
        return self

class Wiki:
    def __init__(self, data):
        self.json = data

        self.author: UserProfile = UserProfile(data.get("author", [])).UserProfile
        try: self.labels: WikiLabelList = WikiLabelList(data["extensions"]["props"]).WikiLabelList
        except (KeyError, TypeError): self.labels: WikiLabelList = WikiLabelList([])

        extensions = self.json.get("extensions") or {}
        style = extensions.get("style") or {}
        knowledgeBase = extensions.get("knowledgeBase") or {}

        self.wikiId = self.json.get("itemId")
        self.status = self.json.get("status")
        self.style = self.json.get("style")
        self.globalCommentsCount = self.json.get("globalCommentsCount")
        self.modifiedTime = self.json.get("modifiedTime")
        self.votedValue = self.json.get("votedValue")
        self.globalVotesCount = self.json.get("globalVotesCount")
        self.globalVotedValue = self.json.get("globalVotedValue")
        self.contentRating = self.json.get("contentRating")
        self.title = self.json.get("label")
        self.content = self.json.get("content")
        self.keywords = self.json.get("keywords")
        self.needHidden = self.json.get("needHidden")
        self.guestVotesCount = self.json.get("guestVotesCount")
        self.extensions = extensions
        self.votesCount = self.json.get("votesCount")
        self.comId = self.json.get("ndcId")
        self.createdTime = self.json.get("createdTime")
        self.mediaList: Optional[MediaObject] = self.json.get("mediaList")
        self.commentsCount = self.json.get("commentsCount")
        self.backgroundColor = style.get("backgroundColor")
        self.fansOnly = extensions.get("fansOnly")
        self.knowledgeBase = knowledgeBase
        self.version = knowledgeBase.get("version")
        self.originalWikiId = knowledgeBase.get("originalItemId")
        self.contributors = knowledgeBase.get("contributors")

    @property
    def Wiki(self):
        return self

class WikiList:
    def __init__(self, data: Dict):
        self.json = data

        self.author = UserProfileList(tuple(y.get("author") for y in data)).UserProfileList
        self.labels = tuple(WikiLabelList(y["extensions"]["props"]).WikiLabelList if "extensions" in y and "props" in y["extensions"] else None for y in data)

        _wikiObjects = tuple(Wiki(x).Wiki for x in data)

        set_attributes(self, _wikiObjects)

    @property
    def WikiList(self):

        return self


class WikiLabelList:
    def __init__(self, data: dict):
        self.json = data
        self.title = data.get("title")
        self.content = data.get("value")
        self.type = data.get("type")

    @property
    def WikiLabelList(self):

        return self

class RankingTableList:
    def __init__(self, data: dict):
        self.json = data
        self.title = tuple(x.get("title") for x in data)
        self.level = tuple(x.get("level") for x in data)
        self.reputation = tuple(x.get("reputation") for x in data)
        self.id = tuple(x.get("id") for x in data)

    @property
    def RankingTableList(self):

        return self

class Community:
    __slots__ = (
        "json", "agent", "rankingTable", "usersCount", "createdTime", "aminoId",
        "icon", "link", "comId", "modifiedTime", "status", "joinType", "tagline",
        "primaryLanguage", "heat", "themePack", "probationStatus", "listedStatus",
        "userAddedTopicList", "name", "isStandaloneAppDeprecated", "searchable",
        "influencerList", "keywords", "mediaList", "description",
        "isStandaloneAppMonetizationEnabled", "advancedSettings", "activeInfo",
        "configuration", "extensions", "nameAliases", "templateId",
        "promotionalMediaList", "defaultRankingTypeInLeaderboard",
        "joinedBaselineCollectionIdList", "newsfeedPages", "catalogEnabled",
        "pollMinFullBarVoteCount", "leaderboardStyle", "facebookAppIdList",
        "welcomeMessage", "welcomeMessageEnabled", "hasPendingReviewRequest",
        "frontPageLayout", "themeColor", "themeHash", "themeVersion", "themeUrl",
        "themeHomePageAppearance", "themeLeftSidePanelTop", "themeLeftSidePanelBottom",
        "themeLeftSidePanelColor", "customList"
    )

    def __init__(self, data: Dict):
        if data is None:
            for attr in self.__slots__:
                setattr(self, attr, None)

            return

        self.json = data

        self.agent: UserProfile = UserProfile(data.get("agent", [])).UserProfile

        try: self.rankingTable: RankingTableList = RankingTableList(data["advancedSettings"]["rankingTable"]).RankingTableList
        except (KeyError, TypeError): self.rankingTable: RankingTableList = RankingTableList([])

        themePack: Dict = data.get("themePack") or {}
        configuration: Dict = data.get("configuration") or {}
        appearance: Dict = configuration.get("appearance") or {}
        leftSidePanel: Dict = appearance.get("leftSidePanel") or {}
        style: Dict = leftSidePanel.get("style") or {}
        page: Dict = configuration.get("page") or {}
        advancedSettings: Dict = data.get("advancedSettings") or {}
        extensions: Dict = data.get("extensions") or {}

        self.name: Optional[str] = data.get("name")
        self.usersCount: Optional[int] = data.get("membersCount")
        self.createdTime: Optional[str] = data.get("createdTime")
        self.aminoId = data.get("endpoint")
        self.icon = data.get("icon")
        self.link = data.get("link")
        self.comId = data.get("ndcId")
        self.modifiedTime = data.get("modifiedTime")
        self.status = data.get("status")
        self.joinType = data.get("joinType")
        self.primaryLanguage = data.get("primaryLanguage")
        self.heat = self.json.get("communityHeat")
        self.userAddedTopicList = self.json.get("userAddedTopicList")
        self.probationStatus = self.json.get("probationStatus")
        self.listedStatus = self.json.get("listedStatus")
        self.themePack = themePack
        self.themeColor = themePack.get("themeColor")
        self.themeHash = themePack.get("themePackHash")
        self.themeVersion = themePack.get("themePackRevision")
        self.themeUrl = themePack.get("themePackUrl")
        self.themeHomePageAppearance = appearance.get("homePage") or {}.get("navigation")
        self.themeLeftSidePanelTop = leftSidePanel.get("navigation") or {}.get("level1")
        self.themeLeftSidePanelBottom = leftSidePanel.get("navigation") or {}.get("level2")
        self.themeLeftSidePanelColor = style.get("iconColor")
        self.customList = page.get("customList")
        self.tagline = self.json.get("tagline")
        self.searchable = self.json.get("searchable")
        self.isStandaloneAppDeprecated = self.json.get("isStandaloneAppDeprecated")
        self.influencerList = self.json.get("influencerList")
        self.keywords = data.get("keywords")
        self.mediaList: Optional[MediaObject] = data.get("mediaList")
        self.description = data.get("content")
        self.isStandaloneAppMonetizationEnabled = data.get("isStandaloneAppMonetizationEnabled")
        self.advancedSettings = advancedSettings
        self.defaultRankingTypeInLeaderboard = advancedSettings.get("defaultRankingTypeInLeaderboard")
        self.frontPageLayout = advancedSettings.get("frontPageLayout")
        self.hasPendingReviewRequest = advancedSettings.get("hasPendingReviewRequest")
        self.welcomeMessageEnabled = advancedSettings.get("welcomeMessageEnabled")
        self.welcomeMessage = advancedSettings.get("welcomeMessageText")
        self.pollMinFullBarVoteCount = advancedSettings.get("pollMinFullBarVoteCount")
        self.catalogEnabled = advancedSettings.get("catalogEnabled")
        self.leaderboardStyle = advancedSettings.get("leaderboardStyle")
        self.facebookAppIdList = advancedSettings.get("facebookAppIdList")
        self.newsfeedPages = advancedSettings.get("newsfeedPages")
        self.joinedBaselineCollectionIdList = advancedSettings.get("joinedBaselineCollectionIdList")
        self.activeInfo = data.get("activeInfo")
        self.configuration = configuration
        self.extensions = extensions
        self.nameAliases = extensions.get("communityNameAliases")
        self.templateId = data.get("templateId")
        self.promotionalMediaList: Optional[MediaObject] = data.get("promotionalMediaList")


    @property
    def Community(self):
        return self

class CommunityList:
    __slots__ = Community.__slots__

    def __init__(self, data: dict):
        self.json = data
        _communtyObjects = tuple(Community(x).Community for x in data)

        set_attributes(self, _communtyObjects)

    @property
    def CommunityList(self):
        return self

class CommentList:
    def __init__(self, data):
        self.json = data
        self.author = UserProfileList(tuple(y.get("author") for y in data)).UserProfileList
        self.votesSum = tuple(x.get("votesSum") for x in data)
        self.votedValue = tuple(x.get("votedValue") for x in data)
        self.mediaList: Optional[List[MediaObject]] = tuple(x.get("mediaList") for x in data)
        self.parentComId = tuple(x.get("parentNdcId") for x in data)
        self.parentId = tuple(x.get("parentId") for x in data)
        self.parentType = tuple(x.get("parentType") for x in data)
        self.content = tuple(x.get("content") for x in data)
        self.extensions = tuple(x.get("extensions") for x in data)
        self.comId = tuple(x.get("ndcId") for x in data)
        self.modifiedTime = tuple(x.get("modifiedTime") for x in data)
        self.createdTime = tuple(x.get("createdTime") for x in data)
        self.commentId = tuple(x.get("commentId") for x in data)
        self.subcommentsCount = tuple(x.get("subcommentsCount") for x in data)
        self.type = tuple(x.get("type") for x in data)

    @property
    def CommentList(self):
        return self


class Membership:
    def __init__(self, data):
        self.json = data

        membership = data.get("membership") or {}

        self.premiumFeature = data.get("premiumFeatureEnabled")
        self.hasAnyAndroidSubscription = data.get("hasAnyAndroidSubscription")
        self.hasAnyAppleSubscription = data.get("hasAnyAppleSubscription")
        self.accountMembership = data.get("accountMembershipEnabled")
        self.paymentType = data.get("paymentType")
        self.membershipStatus = membership.get("membershipStatus")
        self.isAutoRenew = membership.get("isAutoRenew")
        self.createdTime = membership.get("createdTime")
        self.modifiedTime = membership.get("modifiedTime")
        self.renewedTime = membership.get("renewedTime")
        self.expiredTime = membership.get("expiredTime")

    @property
    def Membership(self):
        return self

class FromCode:
    def __init__(self, data):
        self.json = data

        extensions = data.get("extensions") or {}
        linkInfo = extensions.get("linkInfo") or {}

        community = Community(extensions.get("community")).Community
        self.community: Community = community
        self.path = data.get("path")
        self.objectType = linkInfo.get("objectType")
        self.shortCode = linkInfo.get("shortCode")
        self.fullPath = linkInfo.get("fullPath")
        self.targetCode = linkInfo.get("targetCode")
        self.objectId = linkInfo.get("objectId")
        self.shortUrl = linkInfo.get("shareURLShortCode")
        self.fullUrl = linkInfo.get("shareURLFullPath")
        self.comIdPost = linkInfo.get("ndcId")
        self.comId = self.comIdPost or community.comId

    @property
    def FromCode(self):
        return self

class UserProfileCountList:
    __slots__ = (
        "json", "profile", "userProfileCount"
    )

    def __init__(self, data):
        if data is None:
            for attr in self.__slots__:
                setattr(self, attr, None)

            return

        self.json = data

        self.profile: UserProfileList = UserProfileList(data.get("userProfileList")).UserProfileList

        self.userProfileCount = data.get("userProfileCount")

    @property
    def UserProfileCountList(self):
        return self


class WalletInfo:
    def __init__(self, data):
        self.json = data
        self.totalCoinsFloat = data.get("totalCoinsFloat")
        self.adsEnabled = data.get("adsEnabled")
        self.adsVideoStats = data.get("adsVideoStats")
        self.adsFlags = data.get("adsFlags")
        self.totalCoins = data.get("totalCoins")
        self.businessCoinsEnabled = data.get("businessCoinsEnabled")
        self.totalBusinessCoins = data.get("totalBusinessCoins")
        self.totalBusinessCoinsFloat = data.get("totalBusinessCoinsFloat")

    @property
    def WalletInfo(self):
        return self

class WalletHistory:
    def __init__(self, data):
        self.json = data
        self.taxCoins = []
        self.bonusCoinsFloat = []
        self.isPositive = []
        self.bonusCoins = []
        self.taxCoinsFloat = []
        self.transanctionId = []
        self.changedCoins = []
        self.totalCoinsFloat = []
        self.changedCoinsFloat = []
        self.sourceType = []
        self.createdTime = []
        self.totalCoins = []
        self.originCoinsFloat = []
        self.originCoins = []
        self.extData = []
        self.title = []
        self.description = []
        self.icon = []
        self.objectDeeplinkUrl = []

    @property
    def WalletHistory(self):
        for x in self.json:
            _extData = x.get("extData")
            self.taxCoins.append(x.get("taxCoins"))
            self.bonusCoinsFloat.append(x.get("bonusCoinsFloat"))
            self.isPositive.append(x.get("isPositive"))
            self.bonusCoins.append(x.get("bonusCoins"))
            self.taxCoinsFloat.append(x["taxCoinsFloat"])
            self.transanctionId.append(x.get("uid"))
            self.changedCoins.append(x.get("changedCoins"))
            self.totalCoinsFloat.append(x.get("totalCoinsFloat"))
            self.changedCoinsFloat.append(x.get("changedCoinsFloat"))
            self.sourceType.append(x.get("sourceType"))
            self.createdTime.append(x.get("createdTime"))
            self.totalCoins.append(x.get("totalCoins"))
            self.originCoinsFloat.append(x.get("originCoinsFloat"))
            self.originCoins.append(x.get("originCoins"))
            self.extData.append(_extData)
            self.title.append(_extData.get("description"))
            self.icon.append(_extData.get("icon"))
            self.description.append(_extData.get("subtitle"))
            self.objectDeeplinkUrl.append(_extData.get("objectDeeplinkUrl"))


        return self


class UserAchievements:
    def __init__(self, data):
        self.json = data
        self.secondsSpentOfLast24Hours = data.get("secondsSpentOfLast24Hours")
        self.secondsSpentOfLast7Days = data.get("secondsSpentOfLast7Days")
        self.numberOfFollowersCount = data.get("numberOfMembersCount")
        self.numberOfPostsCreated = data.get("numberOfPostsCreated")

    @property
    def UserAchievements(self):
        return self

class UserSavedBlogs:
    def __init__(self, data):
        _object = []

        self.json = data

        for y in data:
            if y["refObjectType"] == 1:
                _object.append(Blog(y.get("refObject")).Blog)

            elif y["refObjectType"] == 2:
                _object.append(Wiki(y.get("refObject")).Wiki)

            else:
                _object.append(y.get("refObject"))

        self.object = _object
        self.objectType = []
        self.bookmarkedTime = []
        self.objectId = []
        self.objectJson = []

    @property
    def UserSavedBlogs(self):
        for x in self.json:
            self.objectType.append(x.get("refObjectType"))
            self.bookmarkedTime.append(x.get("bookmarkedTime"))
            self.objectId.append(x.get("refObjectId"))
            self.objectJson.append(x.get("refObject"))

        return self

class GetWikiInfo:
    def __init__(self, data):
        self.json = data

        self.wiki: Wiki = Wiki(data.get("item")).Wiki

        self.inMyFavorites = data.get("inMyFavorites")
        self.isBookmarked = data.get("isBookmarked")

    @property
    def GetWikiInfo(self):

        return self

class GetBlogInfo:
    def __init__(self, data):
        self.json = data

        self.blog: Blog = Blog(data.get("blog")).Blog
        self.isBookmarked = data.get("isBookmarked")

    @property
    def GetBlogInfo(self):

        return self

class GetSharedFolderInfo:
    def __init__(self, data):
        self.json = data
        self.folderCount = data.get("folderCount")
        self.fileCount = data.get("fileCount")

    @property
    def GetSharedFolderInfo(self):

        return self

class WikiCategoryList:
    def __init__(self, data):
        self.json = data
        _categoryObjects = tuple(WikiCategory(x).WikiCategory for x in data)

        set_attributes(self, _categoryObjects)

    @property
    def WikiCategoryList(self):

        return self

class WikiCategory:
    def __init__(self, data):
        self.json = data

        try: self.author = UserProfile(data["itemCategory"]["author"]).UserProfile
        except (KeyError, TypeError): self.author: UserProfile = UserProfile([])
        try: self.subCategory = WikiCategoryList(data["childrenWrapper"]["itemCategoryList"]).WikiCategoryList
        except (KeyError, TypeError): self.subCategory: WikiCategoryList = WikiCategoryList([])

        itemCategory = data.get("itemCategory") or {}
        childrenWrapper = data.get("childrenWrapper") or {}

        self.itemsCount = itemCategory.get("itemsCount")
        self.parentCategoryId = itemCategory.get("parentCategoryId")
        self.categoryId = itemCategory.get("categoryId")
        self.extensions = itemCategory.get("extensions")
        self.createdTime = itemCategory.get("createdTime")
        self.title = itemCategory.get("label")
        self.mediaList: Optional[MediaObject] = itemCategory.get("mediaList")
        self.icon = itemCategory.get("icon")
        self.parentType = childrenWrapper.get("type")

    @property
    def WikiCategory(self):
        return self

class TippedUsersSummary:
    def __init__(self, data):
        _author = []

        self.json = data

        for y in data["tippedUserList"]:
            _author.append(y.get("tipper"))

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.tipSummary = data.get("tipSummary") or {}
        self.totalCoins = self.tipSummary.get("totalCoins")
        self.tippersCount = self.tipSummary.get("tippersCount")
        self.globalTipSummary = data.get("globalTipSummary") or {}
        self.globalTippersCount = self.globalTipSummary.get("tippersCount")
        self.globalTotalCoins = self.globalTipSummary.get("totalCoins")

        self.lastTippedTime = []
        self.totalTippedCoins = []
        self.lastThankedTime = []

    @property
    def TippedUsersSummary(self):
        for tippedUserList in self.json["tippedUserList"]:
            self.lastTippedTime.append(tippedUserList.get("lastTippedTime"))
            self.totalTippedCoins.append(tippedUserList.get("totalTippedCoins"))
            self.lastThankedTime.append(tippedUserList.get("lastThankedTime"))

        return self

class Thread:
    __slots__ = (
        "json", "author", "membersSummary", "userAddedTopicList", "membersQuota", "chatId",
        "keywords", "membersCount", "isPinned", "title", "membershipStatus", "content",
        "needHidden", "alertOption", "lastReadTime", "type", "status", "publishToGlobal", "modifiedTime",
        "condition", "icon", "latestActivityTime", "comId", "createdTime", "extensions", "viewOnly",
        "coHosts", "membersCanInvite", "language", "announcement", "backgroundImage", "lastMembersSummaryUpdateTime",
        "channelType", "creatorId", "bannedUsers", "visibility", "fansOnly", "pinAnnouncement",
        "vvChatJoinType", "disabledTime", "tippingPermStatus", "screeningRoomHostId", "screeningRoomPermission",
        "organizerTransferCreatedTime", "organizerTransferId"
    )
    def __init__(self, data):
        if data is None:
            for attr in self.__slots__:
                setattr(self, attr, None)

            return

        self.json = data

        self.author: UserProfile = UserProfile(data.get("author")).UserProfile
        self.membersSummary: UserProfileList = UserProfileList(data.get("membersSummary")).UserProfileList

        self.userAddedTopicList = data.get("userAddedTopicList")
        self.membersQuota = data.get("membersQuota")
        self.chatId = data.get("threadId")
        self.keywords = data.get("keywords")
        self.membersCount = data.get("membersCount")
        self.isPinned = data.get("isPinned")
        self.title = data.get("title")
        self.membershipStatus = data.get("membershipStatus")
        self.content = data.get("content")
        self.needHidden = data.get("needHidden")
        self.alertOption = data.get("alertOption")
        self.lastReadTime = data.get("lastReadTime")
        self.type = data.get("type")
        self.status = data.get("status")
        self.publishToGlobal = data.get("publishToGlobal")
        self.modifiedTime = data.get("modifiedTime")
        self.condition = data.get("condition")
        self.icon = data.get("icon")
        self.latestActivityTime = data.get("latestActivityTime")
        self.comId = data.get("ndcId")
        self.createdTime = data.get("createdTime")

        # extensions
        self.extensions = data.get("extensions") or {}
        self.viewOnly = self.extensions.get("viewOnly")
        self.coHosts = self.extensions.get("coHost")
        self.membersCanInvite = self.extensions.get("membersCanInvite")
        self.language = self.extensions.get("language")
        self.announcement = self.extensions.get("announcement")
        self.backgroundImage = self.extensions.get("bm", [None, None])[1]
        self.lastMembersSummaryUpdateTime = self.extensions.get("lastMembersSummaryUpdateTime")
        self.channelType = self.extensions.get("channelType")
        self.creatorId = self.extensions.get("creatorUid")
        self.bannedUsers = self.extensions.get("bannedMemberUidList")
        self.visibility = self.extensions.get("visibility")
        self.fansOnly = self.extensions.get("fansOnly")
        self.pinAnnouncement = self.extensions.get("pinAnnouncement")
        self.vvChatJoinType = self.extensions.get("vvChatJoinType")
        self.disabledTime = self.extensions.get("__disabledTime__")
        self.tippingPermStatus = self.extensions.get("tippingPermStatus")
        self.screeningRoomHostId = self.extensions.get("screeningRoomHostUid")

        # screeningRoomPermission
        screeningRoomPermission = self.extensions.get("screeningRoomPermission") or {}
        self.screeningRoomPermission = screeningRoomPermission.get("action")

        # organizerTransferRequest
        organizerTransferRequest = self.extensions.get("organizerTransferRequest") or {}
        self.organizerTransferCreatedTime = organizerTransferRequest.get("createdTime")
        self.organizerTransferId = organizerTransferRequest.get("requestId")

    @property
    def Thread(self):
        return self


class ThreadList:
    def __init__(self, data):
        _author, _membersSummary = [], []

        self.json = data

        for y in data:
            _author.append(y.get("author"))
            _membersSummary.append(UserProfileList(y.get("membersSummary")).UserProfileList)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.membersSummary = _membersSummary
        self.userAddedTopicList = []
        self.membersQuota = []
        self.chatId = []
        self.keywords = []
        self.membersCount = []
        self.isPinned = []
        self.title = []
        self.membershipStatus = []
        self.content = []
        self.needHidden = []
        self.alertOption = []
        self.lastReadTime = []
        self.type = []
        self.status = []
        self.publishToGlobal = []
        self.modifiedTime = []
        self.condition = []
        self.icon = []
        self.latestActivityTime = []
        self.extensions = []
        self.viewOnly = []
        self.coHosts = []
        self.membersCanInvite = []
        self.announcement = []
        self.language = []
        self.lastMembersSummaryUpdateTime = []
        self.backgroundImage = []
        self.channelType = []
        self.comId = []
        self.createdTime = []
        self.creatorId = []
        self.bannedUsers = []
        self.tippingPermStatus = []
        self.visibility = []
        self.fansOnly = []
        self.pinAnnouncement = []
        self.vvChatJoinType = []
        self.screeningRoomHostId = []
        self.screeningRoomPermission = []
        self.disabledTime = []
        self.organizerTransferCreatedTime = []
        self.organizerTransferId = []

    @property
    def ThreadList(self):
        for chat in self.json:
            extensions = chat.get("extensions") or {}
            screeningRoomPermission = extensions.get("screeningRoomPermission") or {}
            organizerTransferRequest = extensions.get("organizerTransferRequest") or {}

            self.userAddedTopicList.append(chat.get("userAddedTopicList"))
            self.membersQuota.append(chat.get("membersQuota"))
            self.chatId.append(chat.get("threadId"))
            self.keywords.append(chat.get("keywords"))
            self.membersCount.append(chat.get("membersCount"))
            self.isPinned.append(chat.get("isPinned"))
            self.title.append(chat.get("title"))
            self.membershipStatus.append(chat.get("membershipStatus"))
            self.content.append(chat.get("content"))
            self.needHidden.append(chat.get("needHidden"))
            self.alertOption.append(chat.get("alertOption"))
            self.lastReadTime.append(chat.get("lastReadTime"))
            self.type.append(chat.get("type"))
            self.status.append(chat.get("status"))
            self.publishToGlobal.append(chat.get("publishToGlobal"))
            self.modifiedTime.append(chat.get("modifiedTime"))
            self.condition.append(chat.get("condition"))
            self.icon.append(chat.get("icon"))
            self.latestActivityTime.append(chat.get("latestActivityTime"))
            self.comId.append(chat.get("ndcId"))
            self.createdTime.append(chat.get("createdTime"))
            self.extensions.append(extensions)
            self.viewOnly.append(extensions.get("viewOnly"))
            self.coHosts.append(extensions.get("coHost"))
            self.membersCanInvite.append(extensions.get("membersCanInvite"))
            self.language.append(extensions.get("language"))
            self.announcement.append(extensions.get("announcement"))
            self.backgroundImage.append(extensions.get("bm", [None, None])[1])
            self.lastMembersSummaryUpdateTime.append(extensions.get("lastMembersSummaryUpdateTime"))
            self.channelType.append(extensions.get("channelType"))
            self.creatorId.append(extensions.get("creatorUid"))
            self.bannedUsers.append(extensions.get("bannedMemberUidList"))
            self.visibility.append(extensions.get("visibility"))
            self.fansOnly.append(extensions.get("fansOnly"))
            self.pinAnnouncement.append(extensions.get("pinAnnouncement"))
            self.vvChatJoinType.append(extensions.get("vvChatJoinType"))
            self.tippingPermStatus.append(extensions.get("tippingPermStatus"))
            self.screeningRoomHostId.append(extensions.get("screeningRoomHostUid"))
            self.disabledTime.append(extensions.get("__disabledTime__"))
            self.screeningRoomPermission.append(screeningRoomPermission.get("action"))
            self.organizerTransferCreatedTime.append(organizerTransferRequest.get("createdTime"))
            self.organizerTransferId.append(organizerTransferRequest.get("requestId"))

        return self

class Sticker:
    __slots__ = (
        "json", "collection", "status", "icon", "iconV2", "name", "stickerId",
        "smallIcon", "smallIconV2", "stickerCollectionId", "mediumIcon",
        "mediumIconV2", "extensions", "usedCount", "createdTime"
    )

    def __init__(self, data):
        if data is None:
            for attr in self.__slots__:
                setattr(self, attr, None)

            return

        self.json = data

        self.collection: StickerCollection = StickerCollection(data.get("stickerCollectionSummary")).StickerCollection

        self.status: Optional[str] = data.get("status")
        self.icon: Optional[str] = data.get("icon")
        self.iconV2: Optional[str] = data.get("iconV2")
        self.name: Optional[str] = data.get("name")
        self.stickerId: Optional[str] = data.get("stickerId")
        self.smallIcon: Optional[str] = data.get("smallIcon")
        self.smallIconV2: Optional[str] = data.get("smallIconV2")
        self.stickerCollectionId: Optional[str] = data.get("stickerCollectionId")
        self.mediumIcon: Optional[str] = data.get("mediumIcon")
        self.mediumIconV2: Optional[str] = data.get("mediumIconV2")
        self.extensions: Optional[str] = data.get("extensions")
        self.usedCount: Optional[str] = data.get("usedCount")
        self.createdTime: Optional[str] = data.get("createdTime")

    @property
    def Sticker(self):
        return self

class StickerList:
    __slots__ = Sticker.__slots__

    def __init__(self, data: dict):
        self.json = data

        _StickerObjects = tuple(Sticker(x).Sticker for x in data)
        set_attributes(self, _StickerObjects)

    @property
    def StickerList(self):
        return self

class StickerCollection:
    def __init__(self, data):
        self.json = data

        self.author: UserProfile = UserProfile(data.get("author")).UserProfile

        self.status = data.get("status")
        self.collectionType = data.get("collectionType")
        self.modifiedTime = data.get("modifiedTime")
        self.bannerUrl = data.get("bannerUrl")
        self.smallIcon = data.get("smallIcon")
        self.stickersCount = data.get("stickersCount")
        self.usedCount = data.get("usedCount")
        self.icon = data.get("icon")
        self.title = data.get("name")
        self.collectionId = data.get("collectionId")

        self.isActivated = data.get("isActivated")
        self.ownershipStatus = data.get("ownershipStatus")
        self.isNew = data.get("isNew")
        self.availableComIds = data.get("availableNdcIds")
        self.description = data.get("description")

        #extensions
        self.extensions = data.get("extensions") or {}
        self.iconSourceStickerId = self.extensions.get("iconSourceStickerId")
        self.originalAuthor: UserProfile = UserProfile(self.extensions.get("originalAuthor")).UserProfile
        self.originalCommunity: Community = Community(self.extensions.get("originalCommunity")).Community

        #restrictionInfo
        self.restrictionInfo = data.get("restrictionInfo") or {}
        self.discountStatus = self.restrictionInfo.get("discountStatus")
        self.discountValue = self.restrictionInfo.get("discountValue")
        self.ownerId = self.restrictionInfo.get("ownerUid")
        self.ownerType = self.restrictionInfo.get("ownerType")
        self.restrictType = self.restrictionInfo.get("restrictType")
        self.restrictValue = self.restrictionInfo.get("restrictValue")
        self.availableDuration = self.restrictionInfo.get("availableDuration")

    @property
    def StickerCollection(self):

        return self

class StickerCollectionList:
    def __init__(self, data):
        _author, _originalAuthor, _originalCommunity = [], [], []

        self.json = data

        for y in data:
            _author.append(y.get("author"))

            try: _originalAuthor.append(y["extensions"]["originalAuthor"])
            except (KeyError, TypeError): _originalAuthor.append(None)
            try: _originalCommunity.append(y["extensions"]["originalCommunity"])
            except (KeyError, TypeError): _originalCommunity.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.originalAuthor: UserProfileList = UserProfileList(_originalAuthor).UserProfileList
        self.originalCommunity: CommunityList = CommunityList(_originalCommunity).CommunityList
        self.status = []
        self.collectionType = []
        self.modifiedTime = []
        self.bannerUrl = []
        self.smallIcon = []
        self.stickersCount = []
        self.usedCount = []
        self.icon = []
        self.name = []
        self.collectionId = []
        self.extensions = []
        self.isActivated = []
        self.ownershipStatus = []
        self.isNew = []
        self.availableComIds = []
        self.description = []
        self.iconSourceStickerId = []
        self.restrictionInfo = []
        self.discountValue = []
        self.discountStatus = []
        self.ownerId = []
        self.ownerType = []
        self.restrictType = []
        self.restrictValue = []
        self.availableDuration = []

    @property
    def StickerCollectionList(self):
        for x in self.json:
            extensions = x.get("extensions") or {}
            restrictionInfo = x.get("restrictionInfo") or {}

            self.status.append(x.get("status"))
            self.collectionType.append(x.get("collectionType"))
            self.modifiedTime.append(x.get("modifiedTime"))
            self.bannerUrl.append(x.get("bannerUrl"))
            self.smallIcon.append(x.get("smallIcon"))
            self.stickersCount.append(x.get("stickersCount"))
            self.usedCount.append(x.get("usedCount"))
            self.icon.append(x.get("icon"))
            self.name.append(x.get("name"))
            self.collectionId.append(x.get("collectionId"))
            self.extensions.append(extensions)
            self.iconSourceStickerId.append(extensions.get("iconSourceStickerId"))
            self.isActivated.append(x.get("isActivated"))
            self.ownershipStatus.append(x.get("ownershipStatus"))
            self.isNew.append(x.get("isNew"))
            self.availableComIds.append(x.get("availableNdcIds"))
            self.description.append(x.get("description"))
            self.restrictionInfo.append(restrictionInfo)
            self.discountStatus.append(restrictionInfo.get("discountStatus"))
            self.discountValue.append(restrictionInfo.get("discountValue"))
            self.ownerId.append(restrictionInfo.get("ownerUid"))
            self.ownerType.append(restrictionInfo.get("ownerType"))
            self.restrictType.append(restrictionInfo.get("restrictType"))
            self.restrictValue.append(restrictionInfo.get("restrictValue"))
            self.availableDuration.append(restrictionInfo.get("availableDuration"))

        return self

class Message:
    def __init__(self, data):
        self.json = data

        self.author: UserProfile = UserProfile(data.get("author", None)).UserProfile

        extensions = data.get("extensions") or {}
        videoExtensions = extensions.get("videoExtensions") or {}

        self.sticker: Sticker = Sticker(extensions.get("sticker")).Sticker

        self.content = data.get("content")
        self.includedInSummary = data.get("includedInSummary")
        self.isHidden = data.get("isHidden")
        self.messageId = data.get("messageId")
        self.messageType = data.get("messageType")
        self.mediaType = data.get("mediaType")
        self.chatBubbleId = data.get("chatBubbleId")
        self.clientRefId = data.get("clientRefId")
        self.chatId = data.get("threadId")
        self.createdTime = data.get("createdTime")
        self.chatBubbleVersion = data.get("chatBubbleVersion")
        self.type = data.get("type")
        self.replyMessage = extensions.get("replyMessage")
        self.mediaValue = data.get("mediaValue")
        self.extensions = extensions
        self.duration = extensions.get("duration")
        self.videoDuration = videoExtensions.get("duration")
        self.videoHeight = videoExtensions.get("height")
        self.videoWidth = videoExtensions.get("width")
        self.videoCoverImage = videoExtensions.get("coverImage")
        self.originalStickerId = extensions.get("originalStickerId")
        self.mentionUserIds = tuple(m.get("uid") for m in extensions.get("mentionedArray", ()))
        self.tippingCoins = extensions.get("tippingCoins")


    @property
    def Message(self):
        return self

class MessageList:
    def __init__(self, data, nextPageToken = None, prevPageToken = None):
        _author = [x.get("author") for x in data]
        _sticker = []

        self.json = data
        self.nextPageToken = nextPageToken
        self.prevPageToken = prevPageToken

        for y in data:
            try: _sticker.append(y["extensions"]["sticker"])
            except (KeyError, TypeError): _sticker.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.sticker: StickerList = StickerList(_sticker).StickerList
        self.content = []
        self.includedInSummary = []
        self.isHidden = []
        self.messageType = []
        self.messageId = []
        self.mediaType = []
        self.mediaValue = []
        self.chatBubbleId = []
        self.clientRefId = []
        self.chatId = []
        self.createdTime = []
        self.chatBubbleVersion = []
        self.type = []
        self.extensions = []
        self.mentionUserIds = []
        self.duration = []
        self.originalStickerId = []
        self.videoExtensions = []
        self.videoDuration = []
        self.videoHeight = []
        self.videoWidth = []
        self.videoCoverImage = []
        self.tippingCoins = []

    @property
    def MessageList(self):
        for n, x in enumerate(self.json):
            self.content.append(x.get("content"))
            self.includedInSummary.append(x.get("includedInSummary"))
            self.isHidden.append(x.get("isHidden"))
            self.messageId.append(x.get("messageId"))
            self.chatBubbleId.append(x.get("chatBubbleId"))
            self.clientRefId.append(x.get("clientRefId"))
            self.chatId.append(x.get("threadId"))
            self.messageType.append(x.get("messageType"))
            self.createdTime.append(x.get("createdTime"))
            self.chatBubbleVersion.append(x.get("chatBubbleVersion"))
            self.type.append(x.get("type"))
            self.mediaValue.append(x.get("mediaValue"))
            self.mediaType.append(x.get("mediaType"))

            # extensions
            self.extensions.append(x.get("extensions"))
            self.originalStickerId.append(self.extensions[n].get("originalStickerId"))
            self.mentionUserIds.append([m.get("uid") for m in self.extensions[n].get("mentionedArray", [])])
            self.videoExtensions.append(self.extensions[n].get("videoExtensions"))
            self.videoDuration.append(self.extensions[n].get("videoExtensions") or {}.get("duration"))
            self.videoHeight.append(self.extensions[n].get("videoExtensions") or {}.get("height"))
            self.videoWidth.append(self.extensions[n].get("videoExtensions") or {}.get("width"))
            self.videoCoverImage.append(self.extensions[n].get("videoExtensions") or {}.get("coverImage"))
            self.tippingCoins.append(self.extensions[n].get("tippingCoins"))

        return self

class GetMessages:
    def __init__(self, data):
        self.json = data

        self.messageList = []
        self.nextPageToken = None
        self.prevPageToken = None

    @property
    def GetMessages(self):
        paging = self.json.get("paging") or {}

        self.nextPageToken = paging.get("nextPageToken")
        self.prevPageToken = paging.get("prevPageToken")
        self.messageList = self.json.get("messageList")

        return MessageList(self.messageList, self.nextPageToken, self.prevPageToken).MessageList

class CommunityStickerCollection:
    def __init__(self, data):
        self.json = data

        self.sticker: StickerCollectionList = StickerCollectionList(data.get("stickerCollectionList")).StickerCollectionList

        self.stickerCollectionCount = data.get("stickerCollectionCount")

    @property
    def CommunityStickerCollection(self):

        return self

class NotificationList:
    def __init__(self, data):
        _author = [x.get("author") for x in data]

        self.json = data

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.contextComId = []
        self.objectText = []
        self.objectType = []
        self.contextValue = []
        self.comId = []
        self.notificationId = []
        self.objectSubtype = []
        self.parentType = []
        self.createdTime = []
        self.parentId = []
        self.type = []
        self.contextText = []
        self.objectId = []
        self.parentText = []

    @property
    def NotificationList(self):
        for x in self.json:
            self.parentText.append(x.get("parentText"))
            self.objectId.append(x.get("objectId"))
            self.contextText.append(x.get("contextText"))
            self.type.append(x.get("type"))
            self.parentId.append(x.get("parentId"))
            self.createdTime.append(x.get("createdTime"))
            self.parentType.append(x.get("parentType"))
            self.objectSubtype.append(x.get("objectSubtype"))
            self.comId.append(x.get("ndcId"))
            self.notificationId.append(x.get("notificationId"))
            self.objectText.append(x.get("objectText"))
            self.contextValue.append(x.get("contextValue"))
            self.contextComId.append(x.get("contextNdcId"))
            self.objectType.append(x.get("objectType"))

        return self

class AdminLogList:
    def __init__(self, data):
        _author = [x.get("author") for x in data]

        self.json = data

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.createdTime = []
        self.objectType = []
        self.operationName = []
        self.comId = []
        self.referTicketId = []
        self.extData = []
        self.operationDetail = []
        self.operationLevel = []
        self.moderationLevel = []
        self.operation = []
        self.objectId = []
        self.logId = []
        self.objectUrl = []
        self.content = []
        self.value = []

    @property
    def AdminLogList(self):
        for x in self.json:
            extData = x.get("extData") or {}

            self.createdTime.append(x.get("createdTime"))
            self.objectType.append(x.get("objectType"))
            self.operationName.append(x.get("operationName"))
            self.comId.append(x.get("ndcId"))
            self.referTicketId.append(x.get("referTicketId"))
            self.extData.append(extData)
            self.content.append(extData.get("note"))
            self.value.append(extData.get("value"))
            self.operationDetail.append(x.get("operationDetail"))
            self.operationLevel.append(x.get("operationLevel"))
            self.moderationLevel.append(x.get("moderationLevel"))
            self.operation.append(x.get("operation"))
            self.objectId.append(x.get("objectId"))
            self.logId.append(x.get("logId"))
            self.objectUrl.append(x.get("objectUrl"))

        return self

class LotteryLog:
    def __init__(self, data):
        self.json = data

        self.awardValue = data.get("awardValue")
        self.parentId = data.get("parentId")
        self.parentType = data.get("parentType")
        self.objectId = data.get("objectId")
        self.objectType = data.get("objectType")
        self.createdTime = data.get("createdTime")
        self.awardType = data.get("awardType")
        self.refObject = data.get("refObject")

    @property
    def LotteryLog(self):
        return self

class VcReputation:
    def __init__(self, data):
        self.json = data

        self.availableReputation = data.get("availableReputation")
        self.maxReputation = data.get("maxReputation")
        self.reputation = data.get("reputation")
        self.participantCount = data.get("participantCount")
        self.totalReputation = data.get("totalReputation")
        self.duration = data.get("duration")

    @property
    def VcReputation(self):
        return self

class FanClubList:
    __slots__ = (
        "json", "profile", "targetUserProfile", "userId", "lastThankedTime",
        "expiredTime", "createdTime", "status", "targetUserId"
    )

    def __init__(self, data):
        if data is None:
            for attr in self.__slots__:
                setattr(self, attr, None)

            return

        self.json = data

        profile_data = []
        targetUserProfile_data = []
        userId_data = []
        lastThankedTime_data = []
        expiredTime_data = []
        createdTime_data = []
        status_data = []
        targetUserId_data = []

        for x in data:
            profile_data.append(x.get("fansUserProfile"))
            targetUserProfile_data.append(x.get("targetUserProfile"))
            userId_data.append(x.get("uid"))
            lastThankedTime_data.append(x.get("lastThankedTime"))
            expiredTime_data.append(x.get("expiredTime"))
            createdTime_data.append(x.get("createdTime"))
            status_data.append(x.get("fansStatus"))
            targetUserId_data.append(x.get("targetUid"))

        self.profile = UserProfileList(tuple(profile_data)).UserProfileList
        self.targetUserProfile = UserProfileList(tuple(targetUserProfile_data)).UserProfileList
        self.userId = tuple(userId_data)
        self.lastThankedTime = tuple(lastThankedTime_data)
        self.expiredTime = tuple(expiredTime_data)
        self.createdTime = tuple(createdTime_data)
        self.status = tuple(status_data)
        self.targetUserId = tuple(targetUserId_data)

    @property
    def FanClubList(self):
        return self

class InfluencerFans:
    def __init__(self, data):
        self.json = data

        self.influencerProfile: UserProfile = UserProfile(data.get("influencerUserProfile", [])).UserProfile
        self.fanClubList: FanClubList = FanClubList(data.get("fanClubList", [])).FanClubList


        self.myFanClub = data.get("myFanClub")

    @property
    def InfluencerFans(self):
        return self

class QuizQuestionList:
    __slots__ = (
        'json', 'status', 'parentType', 'title', 'createdTime',
        'questionId', 'parentId', 'mediaList', 'extensions', 'style',
        'backgroundImage', 'backgroundColor', 'answerExplanation',
        'answersList'
    )
    def __init__(self, data):
        if data is None:
            for attr in self.__slots__:
                setattr(self, attr, None)

            return

        _answersList = []

        self.json = data

        for y in data:
            try: _answersList.append(QuizAnswers(y["extensions"]["quizQuestionOptList"]).QuizAnswers)
            except (KeyError, TypeError): _answersList.append(None)

        self.status = []
        self.parentType = []
        self.title = []
        self.createdTime = []
        self.questionId = []
        self.parentId = []
        self.mediaList: Optional[List[MediaObject]] = []
        self.extensions = []
        self.style = []
        self.backgroundImage = []
        self.backgroundColor = []
        self.answerExplanation = []
        self.answersList = _answersList

    @property
    def QuizQuestionList(self):
        for x in self.json:
            extensions = x.get("extensions") or {}
            style = extensions.get("style") or {}
            backgroundMediaList: Optional[MediaObject] = style.get("backgroundMediaList", [None, None])

            self.status.append(x.get("status"))
            self.parentType.append(x.get("parentType"))
            self.title.append(x.get("title"))
            self.createdTime.append(x.get("createdTime"))
            self.questionId.append(x.get("quizQuestionId"))
            self.parentId.append(x.get("parentId"))
            self.mediaList.append(x.get("mediaList"))
            self.extensions.append(extensions)
            self.style.append(style)
            self.backgroundImage.append(backgroundMediaList[1])
            self.backgroundColor.append(style.get("backgroundColor"))
            self.answerExplanation.append(extensions.get("quizAnswerExplanation"))

        return self

class QuizAnswers:
    def __init__(self, data):
        self.json = data
        self.answerId = []
        self.isCorrect = []
        self.mediaList: List[Optional[MediaObject]] = []
        self.title = []
        self.qhash = []

    @property
    def QuizAnswers(self):
        for x in self.json:
            self.answerId.append(x.get("optId"))
            self.qhash.append(x.get("qhash"))
            self.isCorrect.append(x.get("isCorrect"))
            self.mediaList.append(x.get("mediaList"))
            self.title.append(x.get("title"))

        return self

class QuizRankings:
    def __init__(self, data):
        _rankingList = []

        self.json = data

        for y in data:
            _rankingList.append(QuizRanking(y.get("quizResultRankingList")).QuizRanking)

        self.rankingList = _rankingList
        self.quizPlayedTimes = data.get("quizPlayedTimes")
        self.quizInBestQuizzes = data.get("quizInBestQuizzes")
        self.profile: QuizRanking = data.get("quizResultOfCurrentUser")

    @property
    def QuizRankings(self):

        return self

class QuizRanking:
    def __init__(self, data):
        self.json = data

        self.highestMode = data.get("highestMode")
        self.modifiedTime = data.get("modifiedTime")
        self.isFinished = data.get("isFinished")
        self.hellIsFinished = data.get("hellIsFinished")
        self.highestScore = data.get("highestScore")
        self.beatRate = data.get("beatRate")
        self.lastBeatRate = data.get("lastBeatRate")
        self.totalTimes = data.get("totalTimes")
        self.latestScore = data.get("latestScore")
        self.latestMode = data.get("latestMode")
        self.createdTime = data.get("createdTime")

    @property
    def QuizRanking(self):

        return self

class QuizRankingList:
    def __init__(self, data):
        _author = [x.get("author") for x in data]

        self.json = data

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.highestMode = []
        self.modifiedTime = []
        self.isFinished = []
        self.hellIsFinished = []
        self.highestScore = []
        self.beatRate = []
        self.lastBeatRate = []
        self.totalTimes = []
        self.latestScore = []
        self.latestMode = []
        self.createdTime = []

    @property
    def QuizRankingList(self):
        for x in self.json:
            self.highestMode.append(x.get("highestMode"))
            self.modifiedTime.append(x.get("modifiedTime"))
            self.isFinished.append(x.get("isFinished"))
            self.hellIsFinished.append(x.get("hellIsFinished"))
            self.highestScore.append(x.get("highestScore"))
            self.beatRate.append(x.get("beatRate"))
            self.lastBeatRate.append(x.get("lastBeatRate"))
            self.totalTimes.append(x.get("totalTimes"))
            self.latestScore.append(x.get("latestScore"))
            self.latestMode.append(x.get("latestMode"))
            self.createdTime.append(x.get("createdTime"))

        return self

class SharedFolderFile:
    def __init__(self, data):
        self.json = data

        self.author: UserProfile = UserProfile(data.get("author")).UserProfile

        self.votesCount = self.json.get("votesCount")
        self.createdTime = self.json.get("createdTime")
        self.modifiedTime = self.json.get("modifiedTime")
        self.extensions = self.json.get("extensions")
        self.width = self.json.get("width_hq")
        self.height = self.json.get("height_hq")
        self.title = self.json.get("title")
        self.media: Optional[MediaObject] = self.json.get("media", [None, None])
        self.mediaType = self.media[0]
        self.fileUrl = self.media[1]
        self.commentsCount = self.json.get("commentsCount")
        self.fileType = self.json.get("fileType")
        self.votedValue = self.json.get("votedValue")
        self.fileId = self.json.get("fileId")
        self.comId = self.json.get("ndcId")
        self.status = self.json.get("status")

    @property
    def SharedFolderFile(self):
        return self

class SharedFolderFileList:
    def __init__(self, data):
        _author = [x.get("author") for x in data]

        self.json = data

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.votesCount = []
        self.createdTime = []
        self.modifiedTime = []
        self.extensions = []
        self.title = []
        self.media: Optional[MediaObject] = []
        self.width = []
        self.height = []
        self.commentsCount = []
        self.fileType = []
        self.votedValue = []
        self.fileId = []
        self.comId = []
        self.status = []
        self.fileUrl = []
        self.mediaType = []

    @property
    def SharedFolderFileList(self):
        for x in self.json:
            media = x.get("media", [None, None])

            self.votesCount.append(x.get("votesCount"))
            self.createdTime.append(x.get("createdTime"))
            self.modifiedTime.append(x.get("modifiedTime"))
            self.extensions.append(x.get("extensions"))
            self.width.append(x.get("width_hq"))
            self.height.append(x.get("height_hq"))
            self.title.append(x.get("title"))
            self.media.append(x.get("media"))
            self.mediaType.append(media[0])
            self.fileUrl.append(media[1])
            self.commentsCount.append(x.get("commentsCount"))
            self.fileType.append(x.get("fileType"))
            self.votedValue.append(x.get("votedValue"))
            self.fileId.append(x.get("fileId"))
            self.comId.append(x.get("ndcId"))
            self.status.append(x.get("status"))


        return self

class Event:
    __sloots__ = (
        "json", "comId", "alertOption", "membershipStatus",
        "actions", "target", "params", "threadType", "duration",
        "id", "message"
    )

    def __init__(self, data):
        self.json = data
        params = self.json.get("params") or {}

        self.comId = self.json.get("ndcId")
        self.alertOption = self.json.get("alertOption")
        self.membershipStatus = self.json.get("membershipStatus")
        self.actions = self.json.get("actions")
        self.target = self.json.get("target")
        self.params = params
        self.threadType = params.get("threadType")
        self.duration = params.get("duration")
        self.id = self.json.get("id")

        self.message: Message = Message(data.get("chatMessage")).Message

    @property
    def Event(self):

        return self

class JoinRequest:
    def __init__(self, data):
        _author = tuple(x for x in data["communityMembershipRequestList"])

        self.json = data

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.communityMembershipRequestCount = self.json.get("communityMembershipRequestCount")

    @property
    def JoinRequest(self):
        return self

class CommunityStats:
    def __init__(self, data):
        self.json = data

        self.dailyActiveMembers = self.json.get("dailyActiveMembers")
        self.monthlyActiveMembers = self.json.get("monthlyActiveMembers")
        self.totalTimeSpent = self.json.get("totalTimeSpent")
        self.totalPostsCreated = self.json.get("totalPostsCreated")
        self.newMembersToday = self.json.get("newMembersToday")
        self.totalMembers = self.json.get("totalMembers")

    @property
    def CommunityStats(self):
        return self


class InviteCode:
    def __init__(self, data):
        self.json = data

        self.author: UserProfile = UserProfile(data.get("author", [])).UserProfile

        self.status = self.json.get("status")
        self.duration = self.json.get("duration")
        self.invitationId = self.json.get("invitationId")
        self.link = self.json.get("link")
        self.modifiedTime = self.json.get("modifiedTime")
        self.comId = self.json.get("ndcId")
        self.createdTime = self.json.get("createdTime")
        self.inviteCode = self.json.get("inviteCode")

    @property
    def InviteCode(self):
        return self


class InviteCodeList:
    def __init__(self, data):
        _author = [x.get("author") for x in data]

        self.json = data

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.status = []
        self.duration = []
        self.invitationId = []
        self.link = []
        self.modifiedTime = []
        self.comId = []
        self.createdTime = []
        self.inviteCode = []

    @property
    def InviteCodeList(self):
        for x in self.json:
            self.status.append(x.get("status"))
            self.duration.append(x.get("duration"))
            self.invitationId.append(x.get("invitationId"))
            self.link.append(x.get("link"))
            self.modifiedTime.append(x.get("modifiedTime"))
            self.comId.append(x.get("ndcId"))
            self.createdTime.append(x.get("createdTime"))
            self.inviteCode.append(x.get("inviteCode"))

        return self

class WikiRequestList:
    def __init__(self, data):
        _author, _wiki, _originalWiki = [], [], []

        self.json = data

        for y in data:
            _author.append(y.get("operator"))
            _wiki.append(y.get("item"))
            _originalWiki.append(y.get("originalItem"))

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.wiki: WikiList = WikiList(_wiki).WikiList
        self.originalWiki: WikiList = WikiList(_originalWiki).WikiList

        self.authorId = []
        self.status = []
        self.modifiedTime = []
        self.message = []
        self.wikiId = []
        self.requestId = []
        self.destinationItemId = []
        self.createdTime = []
        self.responseMessage = []

    @property
    def WikiRequestList(self):
        for x in self.json:
            self.authorId.append(x.get("uid"))
            self.status.append(x.get("status"))
            self.modifiedTime.append(x.get("modifiedTime"))
            self.message.append(x.get("message"))
            self.wikiId.append(x.get("itemId"))
            self.requestId.append(x.get("requestId"))
            self.destinationItemId.append(x.get("destinationItemId"))
            self.createdTime.append(x.get("createdTime"))
            self.responseMessage.append(x.get("responseMessage"))


        return self

class NoticeList:
    def __init__(self, data):
        _author, _targetUser = [], []

        self.json = data

        for y in data:
            _author.append(y.get("operator"))
            _targetUser.append(y.get("targetUser"))

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.targetUser: UserProfileList = UserProfileList(_targetUser).UserProfileList

        self.title = []
        self.icon = []
        self.noticeId = []
        self.status = []
        self.comId = []
        self.modifiedTime = []
        self.createdTime = []
        self.extensions = []
        self.content = []
        self.community = []
        self.type = []
        self.notificationId = []
        self.authorId = []
        self.style = []
        self.backgroundColor = []
        self.config = []
        self.showCommunity = []
        self.showAuthor = []
        self.allowQuickOperation = []
        self.operationList = []

    @property
    def NoticeList(self):
        for x in self.json:
            extensions = x.get("extensions") or {}
            config = extensions.get("config") or {}
            style = extensions.get("style") or {}

            self.title.append(x.get("title"))
            self.icon.append(x.get("icon"))
            self.noticeId.append(x.get("noticeId"))
            self.status.append(x.get("status"))
            self.comId.append(x.get("ndcId"))
            self.modifiedTime.append(x.get("modifiedTime"))
            self.createdTime.append(x.get("createdTime"))
            self.extensions.append(extensions)
            self.authorId.append(extensions.get("operatorUid"))
            self.config.append(config)
            self.showCommunity.append(config.get("showCommunity"))
            self.showAuthor.append(config.get("showOperator"))
            self.allowQuickOperation.append(config.get("allowQuickOperation"))
            self.operationList.append(config.get("operationList"))
            self.style.append(style)
            self.backgroundColor.append(style.get("backgroundColor"))
            self.content.append(x.get("content"))
            self.community.append(x.get("community"))
            self.type.append(x.get("type"))
            self.notificationId.append(x.get("notificationId"))

        return self


class LiveLayer:
    def __init__(self, data):
        self.json = data

        self.userProfileCount = []
        self.topic = []
        self.userProfileList = []
        self.mediaList = []

    @property
    def LiveLayer(self):
        for x in self.json:
            self.userProfileCount.append(x.get("userProfileCount"))
            self.topic.append(x.get("topic"))
            self.userProfileList.append(UserProfileList(x.get("userProfileList", [])).UserProfileList)
            self.mediaList.append(x.get("mediaList"))


        return self


class AvatarFrameList:
    def __init__(self, data):
        _author = tuple(x.get("operator") for x in data)
        _targetUser = tuple(x.get("targetUser") for x in data)

        self.json = data

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.targetUser: UserProfileList = UserProfileList(_targetUser).UserProfileList

        self.isGloballyAvailable = []
        self.extensions = []
        self.frameType = []
        self.resourceUrl = []
        self.md5 = []
        self.icon = []
        self.createdTime = []
        self.config = []
        self.moodColor = []
        self.configName = []
        self.configVersion = []
        self.userIconBorderColor = []
        self.avatarFramePath = []
        self.avatarId = []
        self.ownershipStatus = []
        self.frameUrl = []
        self.additionalBenefits = []
        self.firstMonthFreeAminoPlusMembership = []
        self.restrictionInfo = []
        self.ownerType = []
        self.restrictType = []
        self.restrictValue = []
        self.availableDuration = []
        self.discountValue = []
        self.discountStatus = []
        self.ownerId = []
        self.ownershipInfo = []
        self.isAutoRenew = []
        self.modifiedTime = []
        self.name = []
        self.frameId = []
        self.version = []
        self.isNew = []
        self.availableComIds = []
        self.status = []

    @property
    def AvatarFrameList(self):
        for x in self.json:
            config = x.get("config") or {}
            restrictionInfo = x.get("restrictionInfo") or {}
            ownershipInfo = x.get("ownershipInfo") or {}
            additionalBenefits = x.get("additionalBenefits") or {}

            self.isGloballyAvailable.append(x.get("isGloballyAvailable"))
            self.extensions.append(x.get("extensions"))
            self.frameType.append(x.get("frameType"))
            self.resourceUrl.append(x.get("resourceUrl"))
            self.md5.append(x.get("md5"))
            self.icon.append(x.get("icon"))
            self.createdTime.append(x.get("createdTime"))
            self.config.append(config)
            self.moodColor.append(config.get("moodColor"))
            self.configName.append(config.get("name"))
            self.configVersion.append(config.get("version"))
            self.userIconBorderColor.append(config.get("userIconBorderColor"))
            self.avatarFramePath.append(config.get("avatarFramePath"))
            self.avatarId.append(config.get("id"))
            self.ownershipStatus.append(x.get("ownershipStatus"))
            self.frameUrl.append(x.get("frameUrl"))
            self.additionalBenefits.append(additionalBenefits)
            self.firstMonthFreeAminoPlusMembership.append(additionalBenefits.get("firstMonthFreeAminoPlusMembership"))
            self.restrictionInfo.append(restrictionInfo)
            self.ownerType.append(restrictionInfo.get("ownerType"))
            self.restrictType.append(restrictionInfo.get("restrictType"))
            self.restrictValue.append(restrictionInfo.get("restrictValue"))
            self.availableDuration.append(restrictionInfo.get("availableDuration"))
            self.discountValue.append(restrictionInfo.get("discountValue"))
            self.discountStatus.append(restrictionInfo.get("discountStatus"))
            self.ownerId.append(restrictionInfo.get("ownerUid"))
            self.ownershipInfo.append(ownershipInfo)
            self.isAutoRenew.append(ownershipInfo.get("isAutoRenew"))
            self.name.append(x.get("name"))
            self.modifiedTime.append(x.get("modifiedTime"))
            self.frameId.append(x.get("frameId"))
            self.version.append(x.get("version"))
            self.isNew.append(x.get("isNew"))
            self.status.append(x.get("status"))
            self.availableComIds.append(x.get("availableNdcIds"))

        return self


class BubbleConfig:
    def __init__(self, data):
        self.json = data

        self.status = self.json.get("status")
        self.allowedSlots = self.json.get("allowedSlots")
        self.name = self.json.get("name")
        self.vertexInset = self.json.get("vertexInset")
        self.zoomPoint = self.json.get("zoomPoint")
        self.coverImage = self.json.get("coverImage")
        self.bubbleType = self.json.get("bubbleType")
        self.contentInsets = self.json.get("contentInsets")
        self.version = self.json.get("version")
        self.linkColor = self.json.get("linkColor")
        self.backgroundPath = self.json.get("backgroundPath")
        self.id = self.json.get("id")
        self.previewBackgroundUrl = self.json.get("previewBackgroundUrl")

    @property
    def BubbleConfig(self):
        return self


class Bubble:
    def __init__(self, data):
        self.config: BubbleConfig = BubbleConfig(data.get("config", [])).BubbleConfig

        self.json = data
        self.uid = data.get("uid")
        self.isActivated = data.get("isActivated")
        self.isNew = data.get("isNew")
        self.bubbleId = data.get("bubbleId")
        self.resourceUrl = data.get("resourceUrl")
        self.backgroundImage = data.get("backgroundImage")
        self.status = data.get("status")
        self.modifiedTime = data.get("modifiedTime")

        ownershipInfo = data.get("ownershipInfo") or {}
        self.ownershipInfo = ownershipInfo
        self.expiredTime = ownershipInfo.get("expiredTime")
        self.isAutoRenew = ownershipInfo.get("isAutoRenew")

        self.ownershipStatus = data.get("ownershipStatus")
        self.bannerImage = data.get("bannerImage")
        self.md5 = data.get("md5")
        self.name = data.get("name")
        self.coverImage = data.get("coverImage")
        self.bubbleType = data.get("bubbleType")
        self.extensions = data.get("extensions")
        self.templateId = data.get("templateId")
        self.createdTime = data.get("createdTime")
        self.deletable = data.get("deletable")
        self.backgroundMedia = data.get("backgroundMedia")
        self.description = data.get("description")
        self.materialUrl = data.get("materialUrl")
        self.comId = data.get("ndcId")

        restrictionInfo = data.get("restrictionInfo") or {}
        self.restrictionInfo = restrictionInfo
        self.discountStatus = restrictionInfo.get("discountStatus")
        self.discountValue = restrictionInfo.get("discountValue")
        self.ownerId = restrictionInfo.get("ownerUid")
        self.ownerType = restrictionInfo.get("ownerType")
        self.restrictType = restrictionInfo.get("restrictType")
        self.restrictValue = restrictionInfo.get("restrictValue")
        self.availableDuration = restrictionInfo.get("availableDuration")

    @property
    def Bubble(self):
        return self


class BubbleConfigList:
    def __init__(self, data):
        self.json = data

        self.status = []
        self.allowedSlots = []
        self.name = []
        self.vertexInset = []
        self.zoomPoint = []
        self.coverImage = []
        self.bubbleType = []
        self.contentInsets = []
        self.version = []
        self.linkColor = []
        self.backgroundPath = []
        self.id = []
        self.previewBackgroundUrl = []

    @property
    def BubbleConfigList(self):
        for x in self.json:
            self.status.append(x.get("status"))
            self.allowedSlots.append(x.get("allowedSlots"))
            self.name.append(x.get("name"))
            self.vertexInset.append(x.get("vertexInset"))
            self.zoomPoint.append(x.get("zoomPoint"))
            self.coverImage.append(x.get("coverImage"))
            self.bubbleType.append(x.get("bubbleType"))
            self.contentInsets.append(x.get("contentInsets"))
            self.version.append(x.get("version"))
            self.linkColor.append(x.get("linkColor"))
            self.backgroundPath.append(x.get("backgroundPath"))
            self.id.append(x.get("id"))
            self.previewBackgroundUrl.append(x.get("previewBackgroundUrl"))

        return self

class BubbleList:
    def __init__(self, data):
        _config = tuple(x.get("config") for x in data)

        self.json = data

        self.config: BubbleConfigList = BubbleConfigList(_config).BubbleConfigList
        self.uid = []
        self.isActivated = []
        self.isNew = []
        self.bubbleId = []
        self.resourceUrl = []
        self.version = []
        self.backgroundImage = []
        self.status = []
        self.modifiedTime = []
        self.ownershipInfo = []
        self.expiredTime = []
        self.isAutoRenew = []
        self.ownershipStatus = []
        self.bannerImage = []
        self.md5 = []
        self.name = []
        self.coverImage = []
        self.bubbleType = []
        self.extensions = []
        self.templateId = []
        self.createdTime = []
        self.deletable = []
        self.backgroundMedia: List[Optional[MediaObject]] = []
        self.description = []
        self.materialUrl = []
        self.comId = []
        self.restrictionInfo = []
        self.discountValue = []
        self.discountStatus = []
        self.ownerId = []
        self.ownerType = []
        self.restrictType = []
        self.restrictValue = []
        self.availableDuration = []

    @property
    def BubbleList(self):
        for x in self.json:
            ownershipInfo = x.get("ownershipInfo") or {}
            restrictionInfo = x.get("restrictionInfo") or {}

            self.uid.append(x.get("uid"))
            self.isActivated.append(x.get("isActivated"))
            self.isNew.append(x.get("isNew"))
            self.bubbleId.append(x.get("bubbleId"))
            self.resourceUrl.append(x.get("resourceUrl"))
            self.backgroundImage.append(x.get("backgroundImage"))
            self.status.append(x.get("status"))
            self.modifiedTime.append(x.get("modifiedTime"))
            self.ownershipInfo.append(ownershipInfo)
            self.expiredTime.append(ownershipInfo.get("expiredTime"))
            self.isAutoRenew.append(ownershipInfo.get("isAutoRenew"))
            self.ownershipStatus.append(x.get("ownershipStatus"))
            self.bannerImage.append(x.get("bannerImage"))
            self.md5.append(x.get("md5"))
            self.name.append(x.get("name"))
            self.coverImage.append(x.get("coverImage"))
            self.bubbleType.append(x.get("bubbleType"))
            self.extensions.append(x.get("extensions"))
            self.templateId.append(x.get("templateId"))
            self.createdTime.append(x.get("createdTime"))
            self.deletable.append(x.get("deletable"))
            self.backgroundMedia.append(x.get("backgroundMedia"))
            self.description.append(x.get("description"))
            self.materialUrl.append(x.get("materialUrl"))
            self.comId.append(x.get("ndcId"))
            self.restrictionInfo.append(restrictionInfo)
            self.discountStatus.append(restrictionInfo.get("discountStatus"))
            self.discountValue.append(restrictionInfo.get("discountValue"))
            self.ownerId.append(restrictionInfo.get("ownerUid"))
            self.ownerType.append(restrictionInfo.get("ownerType"))
            self.restrictType.append(restrictionInfo.get("restrictType"))
            self.restrictValue.append(restrictionInfo.get("restrictValue"))
            self.availableDuration.append(restrictionInfo.get("availableDuration"))

        return self


class AvatarFrame:
    def __init__(self, data):
        self.json = data

        self.name = []
        self.id = []
        self.resourceUrl = []
        self.icon = []
        self.frameUrl = []
        self.value = []

    @property
    def AvatarFrame(self):
        for x in self.json:
            refObject = x.get("refObject") or {}
            config = refObject.get("config") or {}
            restrictionInfo = refObject.get("restrictionInfo") or {}

            self.name.append(config.get("name"))
            self.id.append(config.get("id"))
            self.resourceUrl.append(refObject.get("resourceUrl"))
            self.icon.append(refObject.get("icon"))
            self.frameUrl.append(refObject.get("frameUrl"))
            self.value.append(restrictionInfo.get("restrictValue"))

        return self


class ChatBubble:
    def __init__(self, data):
        self.json = data

        self.name = []
        self.bubbleId = []
        self.bannerImage = []
        self.backgroundImage = []
        self.resourceUrl = []
        self.value = []

    @property
    def ChatBubble(self):
        for x in self.json:
            itemBasicInfo = x.get("itemBasicInfo") or {}
            refObject = x.get("refObject") or {}
            restrictionInfo = refObject.get("restrictionInfo") or {}

            self.name.append(itemBasicInfo.get("name"))
            self.bubbleId.append(refObject.get("bubbleId"))
            self.bannerImage.append(refObject.get("bannerImage"))
            self.backgroundImage.append(refObject.get("backgroundImage"))
            self.resourceUrl.append(refObject.get("resourceUrl"))
            self.value.append(restrictionInfo.get("restrictValue"))

        return self

class StoreStickers:
    def __init__(self, data):
        self.json = data

        self.id = []
        self.name = []
        self.icon = []
        self.value = []
        self.smallIcon = []

    @property
    def StoreStickers(self):
        for x in self.json:
            refObject = x.get("refObject") or {}
            itemBasicInfo = x.get("itemBasicInfo") or {}
            restrictionInfo = refObject.get("restrictionInfo") or {}

            self.id.append(refObject.get("collectionId"))
            self.name.append(itemBasicInfo.get("name"))
            self.icon.append(itemBasicInfo.get("icon"))
            self.value.append(restrictionInfo.get("restrictValue"))
            self.smallIcon.append(refObject.get("smallIcon"))

        return self

class MediaObject(List[List[TypeVar('T')]]):
    pass

def set_attributes(instance, _ListObjects):
    if _ListObjects:
        attributes = tuple(attr for attr in dir(_ListObjects[0]) if not attr.startswith('__') and not callable(getattr(_ListObjects[0], attr)) and attr != _ListObjects[0].__class__.__name__)
        for attr in attributes:
            setattr(instance, attr, tuple(getattr(user, attr, None) for user in _ListObjects))
