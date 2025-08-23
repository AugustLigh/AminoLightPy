# pylint: disable=too-many-lines
from json import loads, JSONDecodeError

class AminoBaseException(Exception):
    """Base class for all custom exceptions in library."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UnsupportedService(AminoBaseException):
    """
    - **API Code** : 100
    - **API Message** : Unsupported service. Your client may be out of date. Please update it to the latest version.
    - **API String** : ``Unknown String``
    """

class FileTooLarge(AminoBaseException):
    """
    - **API Code** : 102
    - **API Message** : ``Unknown Message``
    - **API String** : API_STD_ERR_ENTITY_TOO_LARGE_RAW
    """

class InvalidRequest(AminoBaseException):
    """
    - **API Code** : 103, 104
    - **API Message** : Invalid Request. Please update to the latest version. If the problem continues, please contact us.
    - **API String** : ``Unknown String``
    """

class InvalidSession(AminoBaseException):
    """
    - **API Code** : 105
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class AccessDenied(AminoBaseException):
    """
    - **API Code** : 106
    - **API Message** : Access denied.
    - **API String** : ``Unknown String``
    """

class UnexistentData(AminoBaseException):
    """
    - **API Code** : 107
    - **API Message** : The requested data does not exist.
    - **API String** : ``Unknown String``
    """

class ActionNotAllowed(AminoBaseException):
    """
    - **API Code** : 110
    - **API Message** : Action not allowed.
    - **API String** : ``Unknown String``
    """

class ServiceUnderMaintenance(AminoBaseException):
    """
    - **API Code** : 111
    - **API Message** : Sorry, this service is under maintenance. Please check back later.
    - **API String** : ``Unknown String``
    """

class MessageNeeded(AminoBaseException):
    """
    - **API Code** : 113
    - **API Message** : Be more specific, please.
    - **API String** : ``Unknown String``
    """

class InvalidAccountOrPassword(AminoBaseException):
    """
    - **API Code** : 200
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class AccountDisabled(AminoBaseException):
    """
    - **API Code** : 210
    - **API Message** : This account is disabled.
    - **API String** : AUTH_DISABLED_ACCOUNT
    """

class InvalidEmail(AminoBaseException):
    """
    - **API Code** : 213
    - **API Message** : Invalid email address.
    - **API String** : API_ERR_EMAIL
    """

class InvalidPassword(AminoBaseException):
    """
    - **API Code** : 214
    - **API Message** : Invalid password. Password must be 6 characters or more and contain no spaces.
    - **API String** : API_ERR_PASSWORD
    """

class EmailAlreadyTaken(AminoBaseException):
    """
    - **API Code** : 215
    - **API Message** : Hey this email ``X`` has been registered already. You can try to log in with the email or edit the email.
    - **API String** : API_ERR_EMAIL_TAKEN
    """

class UnsupportedEmail(AminoBaseException):
    """
    - **API Code** : 215
    - **API Message** : This email address is not supported.
    - **API String** : API_ERR_EMAIL_TAKEN
    """

class AccountDoesntExist(AminoBaseException):
    """
    - **API Code** : 216
    - **API Message** : ``Unknown Message``
    - **API String** : AUTH_ACCOUNT_NOT_EXISTS
    """

class InvalidDevice(AminoBaseException):
    """
    - **API Code** : 218
    - **API Message** : Error! Your device is currently not supported, or the app is out of date. Please update to the latest version.
    - **API String** : ``Unknown String``
    """

class AccountLimitReached(AminoBaseException):
    """
    - **API Code** : 219
    - **API Message** : A maximum of 3 accounts can be created from this device. If you forget your password, please reset it.
    - **API String** : ``Unknown String``
    """

class TooManyRequests(AminoBaseException):
    """
    - **API Code** : 219
    - **API Message** : Too many requests. Try again later.
    - **API String** : ``Unknown String``
    """

class CantFollowYourself(AminoBaseException):
    """
    - **API Code** : 221
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class UserUnavailable(AminoBaseException):
    """
    - **API Code** : 225
    - **API Message** : This user is unavailable.
    - **API String** : ``Unknown String``
    """

class YouAreBanned(AminoBaseException):
    """
    - **API Code** : 229
    - **API Message** : You are banned.
    - **API String** : ``Unknown String``
    """

class UserNotMemberOfCommunity(AminoBaseException):
    """
    - **API Code** : 230
    - **API Message** : You have to join this Community first.
    - **API String** : API_ERR_USER_NOT_IN_COMMUNITY
    """

class RequestRejected(AminoBaseException):
    """
    - **API Code** : 235
    - **API Message** : Request rejected. You have been temporarily muted (read only mode) because you have received a strike. To learn more, please check the Help Center.
    - **API String** : ``Unknown String``
    """

class ActivateAccount(AminoBaseException):
    """
    - **API Code** : 238
    - **API Message** : Please activate your account first. Check your email, including your spam folder.
    - **API String** : ``Unknown String``
    """

class CantLeaveCommunity(AminoBaseException):
    """
    - **API Code** : 239
    - **API Message** : Sorry, you can not do this before transferring your Agent status to another member.
    - **API String** : ``Unknown String``
    """
    

class ReachedTitleLength(AminoBaseException):
    """
    - **API Code** : 240
    - **API Message** : Sorry, the max length of member's title is limited to 20.
    - **API String** : ``Unknown String``
    """

class AccountDeleted(AminoBaseException):
    """
    - **API Code** : 246
    - **API Message** : ``Unknown Message``
    - **API String** : AUTH_RECOVERABLE_DELETED_ACCOUNT
    """

class API_ERR_EMAIL_NO_PASSWORD(AminoBaseException):
    """
    - **API Code** : 251
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_EMAIL_NO_PASSWORD
    """

class API_ERR_COMMUNITY_USER_CREATED_COMMUNITIES_VERIFY(AminoBaseException):
    """
    - **API Code** : 257
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_COMMUNITY_USER_CREATED_COMMUNITIES_VERIFY
    """

class ReachedMaxTitles(AminoBaseException):
    """
    - **API Code** : 262
    - **API Message** : You can only add up to 20 Titles. Please choose the most relevant ones.
    - **API String** : ``Unknown String``
    """

class VerificationRequired(AminoBaseException):
    """
    - **API Code** : 270
    - **API Message** : Verification Required.
    - **API String** : API_ERR_NEED_TWO_FACTOR_AUTHENTICATION
    """

class API_ERR_INVALID_AUTH_NEW_DEVICE_LINK(AminoBaseException):
    """
    - **API Code** : 271
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_INVALID_AUTH_NEW_DEVICE_LINK
    """

class CommandCooldown(AminoBaseException):
    """
    - **API Code** : 291
    - **API Message** : Whoa there! You've done too much too quickly. Take a break and try again later.
    - **API String** : ``Unknown String``
    """

class UserBannedByTeamAmino(AminoBaseException):
    """
    - **API Code** : 293
    - **API Message** : Sorry, this user has been banned by Team Amino.
    - **API String** : ``Unknown String``
    """

class BadImage(AminoBaseException):
    """
    - **API Code** : 300
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class InvalidThemepack(AminoBaseException):
    """
    - **API Code** : 313
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class InvalidVoiceNote(AminoBaseException):
    """
    - **API Code** : 314
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class RequestedNoLongerExists(AminoBaseException):
    """
    - **API Code** : 500, 700, 1600
    - **API Message** : Sorry, the requested data no longer exists. Try refreshing the view.
    - **API String** : ``Unknown String``
    """

class PageRepostedTooRecently(AminoBaseException):
    """
    - **API Code** : 503
    - **API Message** : Sorry, you have reported this page too recently.
    - **API String** : ``Unknown String``
    """

class InsufficientLevel(AminoBaseException):
    """
    - **API Code** : 551
    - **API Message** : This post type is restricted to members with a level ``X`` ranking.
    - **API String** : ``Unknown String``
    """

class WallCommentingDisabled(AminoBaseException):
    """
    - **API Code** : 702
    - **API Message** : This member has disabled commenting on their wall.
    - **API String** : ``Unknown String``
    """

class CommunityNoLongerExists(AminoBaseException):
    """
    - **API Code** : 801
    - **API Message** : This Community no longer exists.
    - **API String** : ``Unknown String``
    """

class InvalidCodeOrLink(AminoBaseException):
    """
    - **API Code** : 802
    - **API Message** : Sorry, this code or link is invalid.
    - **API String** : ``Unknown String``
    """

class CommunityNameAlreadyTaken(AminoBaseException):
    """
    - **API Code** : 805
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class CommunityCreateLimitReached(AminoBaseException):
    """
    - **API Code** : 806
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_COMMUNITY_USER_CREATED_COMMUNITIES_EXCEED_QUOTA
    """

class CommunityDisabled(AminoBaseException):
    """
    - **API Code** : 814
    - **API Message** : This Community is disabled.
    - **API String** : ``Unknown String``
    """

class CommunityDeleted(AminoBaseException):
    """
    - **API Code** : 833
    - **API Message** : This Community has been deleted.
    - **API String** : ``Unknown String``
    """

class DuplicatePollOption(AminoBaseException):
    """
    - **API Code** : 1501
    - **API Message** : Sorry, you have duplicate poll options.
    - **API String** : ``Unknown String``
    """

class ReachedMaxPollOptions(AminoBaseException):
    """
    - **API Code** : 1507
    - **API Message** : Sorry, you can only join or add up to 5 of your items per poll.
    - **API String** : ``Unknown String``
    """

class TooManyChats(AminoBaseException):
    """
    - **API Code** : 1602
    - **API Message** : Sorry, you can only have up to 1000 chat sessions.
    - **API String** : ``Unknown String``
    """

class ChatFull(AminoBaseException):
    """
    - **API Code** : 1605
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class TooManyInviteUsers(AminoBaseException):
    """
    - **API Code** : 1606
    - **API Message** : Sorry, you can only invite up to 999 people.
    - **API String** : ``Unknown String``
    """

class ChatInvitesDisabled(AminoBaseException):
    """
    - **API Code** : 1611
    - **API Message** : This user has disabled chat invite requests.
    - **API String** : ``Unknown String``
    """

class RemovedFromChat(AminoBaseException):
    """
    - **API Code** : 1612
    - **API Message** : You've been removed from this chatroom.
    - **API String** : ``Unknown String``
    """

class UserNotJoined(AminoBaseException):
    """
    - **API Code** : 1613
    - **API Message** : Sorry, this user has not joined.
    - **API String** : ``Unknown String``
    """

class API_ERR_CHAT_VVCHAT_NO_MORE_REPUTATIONS(AminoBaseException):
    """
    - **API Code** : 1627
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_CHAT_VVCHAT_NO_MORE_REPUTATIONS
    """

class MemberKickedByOrganizer(AminoBaseException):
    """
    - **API Code** : 1637
    - **API Message** : This member was previously kicked by the organizer and cannot be reinvited.
    - **API String** : ``Unknown String``
    """

class LevelFiveRequiredToEnableProps(AminoBaseException):
    """
    - **API Code** : 1661
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class ChatViewOnly(AminoBaseException):
    """
    - **API Code** : 1663
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class ChatMessageTooBig(AminoBaseException):
    """
    - **API Code** : 1664
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_CHAT_MESSAGE_CONTENT_TOO_LONG
    """

class InviteCodeNotFound(AminoBaseException):
    """
    - **API Code** : 1900
    - **API Message** : Sorry, the requested data no longer exists. Try refreshing the view.
    - **API String** : ``Unknown String``
    """

class AlreadyRequestedJoinCommunity(AminoBaseException):
    """
    - **API Code** : 2001
    - **API Message** : Sorry, you have already submitted a membership request.
    - **API String** : ``Unknown String``
    """

class API_ERR_PUSH_SERVER_LIMITATION_APART(AminoBaseException):
    """
    - **API Code** : 2501
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_PUSH_SERVER_LIMITATION_APART
    """

class API_ERR_PUSH_SERVER_LIMITATION_COUNT(AminoBaseException):
    """
    - **API Code** : 2502
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_PUSH_SERVER_LIMITATION_COUNT
    """

class API_ERR_PUSH_SERVER_LINK_NOT_IN_COMMUNITY(AminoBaseException):
    """
    - **API Code** : 2503
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_PUSH_SERVER_LINK_NOT_IN_COMMUNITY
    """

class API_ERR_PUSH_SERVER_LIMITATION_TIME(AminoBaseException):
    """
    - **API Code** : 2504
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_PUSH_SERVER_LIMITATION_TIME
    """

class AlreadyCheckedIn(AminoBaseException):
    """
    - **API Code** : 2601
    - **API Message** : Sorry, you can't check in any more.
    - **API String** : ``Unknown String``
    """

class AlreadyUsedMonthlyRepair(AminoBaseException):
    """
    - **API Code** : 2611
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class AccountAlreadyRestored(AminoBaseException):
    """
    - **API Code** : 2800
    - **API Message** : Account already restored.
    - **API String** : ``Unknown String``
    """

class IncorrectVerificationCode(AminoBaseException):
    """
    - **API Code** : 3102
    - **API Message** : Incorrect verification code.
    - **API String** : ``Unknown String``
    """

class NotOwnerOfChatBubble(AminoBaseException):
    """
    - **API Code** : 3905
    - **API Message** : You are not the owner of this chat bubble.
    - **API String** : ``Unknown String``
    """

class NotEnoughCoins(AminoBaseException):
    """
    - **API Code** : 4300
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class AlreadyPlayedLottery(AminoBaseException):
    """
    - **API Code** : 4400
    - **API Message** : You have played the maximum number of lucky draws.
    - **API String** : ``Unknown String``
    """

class CannotSendCoins(AminoBaseException):
    """
    - **API Code** : 4500, 4501
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """

class AminoIDAlreadyChanged(AminoBaseException):
    """
    - **API Code** : 6001
    - **API Message** : Amino ID cannot be changed after you set it.
    - **API String** : ``Unknown String``
    """

class InvalidAminoID(AminoBaseException):
    """
    - **API Code** : 6002
    - **API Message** : Invalid Amino ID
    - **API String** : ``Unknown String``
    """

class InvalidName(AminoBaseException):
    """
    - **API Code** : 99001
    - **API Message** : Sorry, the name is invalid.
    - **API String** : ``Unknown String``
    """

class SpecifyType(AminoBaseException):
    """
    Raised when you need to specify the output of the command.
    """
    

class WrongType(AminoBaseException):
    """
    Raised when you attribute the function the wrong type.
    """

class UnknownResponse(AminoBaseException):
    """
    Raised when an error occurs but the reason is unknown.
    """

class NotLoggedIn(AminoBaseException):
    """
    Raised when you try to make an action but you aren't logged in.
    """

class NoCommunity(AminoBaseException):
    """
    Raised when you try to make an action but no community was selected.
    """

class CommunityNotFound(AminoBaseException):
    """
    Raised when you search for a community but nothing is found.
    """

class NoChatThread(AminoBaseException):
    """
    Raised when you try to make an action but no chat was selected.
    """

class ChatRequestsBlocked(AminoBaseException):
    """
    Raised when you try to make an action but the end user has chat requests blocked.
    """

class NoImageSource(AminoBaseException):
    """
    Raised when you try to make an action but no image source was selected.
    """

class CannotFetchImage(AminoBaseException):
    """
    Raised when an image cannot be fetched.
    """

class FailedLogin(AminoBaseException):
    """
    Raised when you try to login but it fails.
    """

class AgeTooLow(AminoBaseException):
    """
    Raised when you try to configure an account but the age is too low. Minimum is 13.
    """

class UnsupportedLanguage(AminoBaseException):
    """
    Raised when you try to use a language that isn't supported or exists.
    """

class CommunityNeeded(AminoBaseException):
    """
    Raised when you try to execute an command but a Community needs to be specified.
    """

class FlagTypeNeeded(AminoBaseException):
    """
    Raised when you try to flag a community, blog or user but a Flag Type needs to be specified.
    """

class ReasonNeeded(AminoBaseException):
    """
    Raised when you try to execute an command but a Reason needs to be specified.
    """

class TransferRequestNeeded(AminoBaseException):
    """
    Raised when you need to transfer host to complete the action.
    """

class LibraryUpdateAvailable(AminoBaseException):
    """
    Raised when a new library update is available.
    """

class UserHasBeenDeleted(AminoBaseException):
    """
    - **API Code** : 245
    - **API Message** : Sorry, this user has been deleted.
    - **API String** : ``Unknown String``
    """

class IpTemporaryBan(AminoBaseException):
    """
    - **API Code** : 403
    - **API Message** : 403 Forbidden.
    - **API String** : ``Unknown String``
    """

class FailedSubscribeFanClub(AminoBaseException):
    """
    - **API Code** : 4805
    - **API Message** : Failed to subscribe to this fan club.
    - **API String** : ``Unknown String``
    """

class UnknownError(AminoBaseException):
    pass

def CheckException(data):
    try:
        data = loads(data)
        try:
            api_code = data["api:statuscode"]
        except KeyError as e:
            raise UnknownError(data) from e
    except JSONDecodeError:
        api_code = 403

    exception_map = {
        100: UnsupportedService,
        102: FileTooLarge,
        103: InvalidRequest,
        104: InvalidRequest,
        105: InvalidSession,
        106: AccessDenied,
        107: UnexistentData,
        110: ActionNotAllowed,
        111: ServiceUnderMaintenance,
        113: MessageNeeded,
        200: InvalidAccountOrPassword,
        201: AccountDisabled,
        213: InvalidEmail,
        214: InvalidPassword,
        215: EmailAlreadyTaken,
        216: AccountDoesntExist,
        218: InvalidDevice,
        219: AccountLimitReached,
        221: CantFollowYourself,
        225: UserUnavailable,
        229: YouAreBanned,
        230: UserNotMemberOfCommunity,
        235: RequestRejected,
        238: ActivateAccount,
        239: CantLeaveCommunity,
        240: ReachedTitleLength,
        245: UserHasBeenDeleted,
        246: AccountDeleted,
        251: API_ERR_EMAIL_NO_PASSWORD,
        257: API_ERR_COMMUNITY_USER_CREATED_COMMUNITIES_VERIFY,
        262: ReachedMaxTitles,
        270: VerificationRequired,
        271: API_ERR_INVALID_AUTH_NEW_DEVICE_LINK,
        291: CommandCooldown,
        293: UserBannedByTeamAmino,
        300: BadImage,
        313: InvalidThemepack,
        314: InvalidVoiceNote,
        403: IpTemporaryBan,
        500: RequestedNoLongerExists,
        700: RequestedNoLongerExists,
        1600: RequestedNoLongerExists,
        503: PageRepostedTooRecently,
        551: InsufficientLevel,
        702: WallCommentingDisabled,
        801: CommunityNoLongerExists,
        802: InvalidCodeOrLink,
        805: CommunityNameAlreadyTaken,
        806: CommunityCreateLimitReached,
        814: CommunityDisabled,
        833: CommunityDeleted,
        1501: DuplicatePollOption,
        1507: ReachedMaxPollOptions,
        1602: TooManyChats,
        1605: ChatFull,
        1606: TooManyInviteUsers,
        1611: ChatInvitesDisabled,
        1612: RemovedFromChat,
        1613: UserNotJoined,
        1627: API_ERR_CHAT_VVCHAT_NO_MORE_REPUTATIONS,
        1637: MemberKickedByOrganizer,
        1661: LevelFiveRequiredToEnableProps,
        1663: ChatViewOnly,
        1664: ChatMessageTooBig,
        1900: InviteCodeNotFound,
        2001: AlreadyRequestedJoinCommunity,
        2501: API_ERR_PUSH_SERVER_LIMITATION_APART,
        2502: API_ERR_PUSH_SERVER_LIMITATION_COUNT,
        2503: API_ERR_PUSH_SERVER_LINK_NOT_IN_COMMUNITY,
        2504: API_ERR_PUSH_SERVER_LIMITATION_TIME,
        2601: AlreadyCheckedIn,
        2611: AlreadyUsedMonthlyRepair,
        2800: AccountAlreadyRestored,
        3102: IncorrectVerificationCode,
        3905: NotOwnerOfChatBubble,
        4300: NotEnoughCoins,
        4400: AlreadyPlayedLottery,
        4500: CannotSendCoins,
        4501: CannotSendCoins,
        4805: FailedSubscribeFanClub,
        6001: AminoIDAlreadyChanged,
        6002: InvalidAminoID,
        9901: InvalidName,
    }

    if api_code in exception_map:
        raise exception_map[api_code](data)
    else:
        raise UnknownError(data)