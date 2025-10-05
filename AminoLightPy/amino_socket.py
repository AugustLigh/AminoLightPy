# pylint: disable=invalid-name
# pylint: disable=no-member
import ssl
import traceback
import threading

from json import loads, dumps
from time import time, sleep
from websocket import WebSocketApp

from .lib import Event
from .lib import gen_deviceId, signature
from .lib.util.objects import ChatEvent

class Callbacks:
    def __init__(self):
        self.handlers = {}
        self.methods = {
            304: self._resolve_chat_action_start,
            306: self._resolve_chat_action_end,
            1000: self._resolve_chat_message
        }
        self.chat_methods = {
            "0:0": ChatEvent.TEXT_MESSAGE,
            "0:100": ChatEvent.IMAGE_MESSAGE,
            "0:103": ChatEvent.YOUTUBE_MESSAGE,
            "1:0": ChatEvent.STRIKE_MESSAGE,
            "2:110": ChatEvent.VOICE_MESSAGE,
            "3:113": ChatEvent.STICKER_MESSAGE,
            "52:0": ChatEvent.VOICE_CHAT_MISSED,
            "53:0": ChatEvent.VOICE_CHAT_CANCELLED,
            "54:0": ChatEvent.VOICE_CHAT_DECLINED,
            "55:0": ChatEvent.VIDEO_CHAT_MISSED,
            "56:0": ChatEvent.VIDEO_CHAT_CANCELLED,
            "57:0": ChatEvent.VIDEO_CHAT_DECLINED,
            "100:0": ChatEvent.MESSAGE_DELETED,
            "101:0": ChatEvent.USER_JOINED,
            "102:0": ChatEvent.USER_LEFT,
            "103:0": ChatEvent.CHAT_INVITE,
            "104:0": ChatEvent.BACKGROUND_CHANGED,
            "105:0": ChatEvent.TITLE_CHANGED,
            "106:0": ChatEvent.ICON_CHANGED,
            "107:0": ChatEvent.VOICE_CHAT_STARTED,
            "108:0": ChatEvent.VIDEO_CHAT_STARTED,
            "110:0": ChatEvent.VOICE_CHAT_ENDED,
            "111:0": ChatEvent.VIDEO_CHAT_ENDED,
            "113:0": ChatEvent.CHAT_CONTENT_CHANGED,
            "114:0": ChatEvent.SCREEN_ROOM_STARTED,
            "115:0": ChatEvent.SCREEN_ROOM_ENDED,
            "116:0": ChatEvent.HOST_TRANSFERRED,
            "117:0": ChatEvent.MESSAGE_FORCE_DELETED,
            "118:0": ChatEvent.CHAT_MESSAGE_REMOVED,
            "119:0": ChatEvent.MESSAGE_REMOVED_BY_ADMIN,
            "120:0": ChatEvent.CHAT_TIP,
            "121:0": ChatEvent.ANNOUNCEMENT_PINNED,
            "122:0": ChatEvent.VOICE_CHAT_OPEN_PERMISSION,
            "123:0": ChatEvent.VOICE_CHAT_REQUEST_PERMISSION,
            "124:0": ChatEvent.VOICE_CHAT_INVITE_PERMISSION,
            "125:0": ChatEvent.CHAT_VIEW_ONLY_ENABLED,
            "126:0": ChatEvent.CHAT_VIEW_ONLY_DISABLED,
            "127:0": ChatEvent.ANNOUNCEMENT_UNPINNED,
            "128:0": ChatEvent.CHAT_TIPPING_ENABLED,
            "129:0": ChatEvent.CHAT_TIPPING_DISABLED,
            "65281:0": ChatEvent.TIMESTAMP_MESSAGE,
            "65282:0": ChatEvent.WELCOME_MESSAGE,
            "65283:0": ChatEvent.INVITE_MESSAGE
        }
        self.chat_actions_start = {"Typing": "on_user_typing_start"}
        self.chat_actions_end = {"Typing": "on_user_typing_end"}

    def _resolve_chat_message(self, data):
        key = f"{data['o']['chatMessage']['type']}:{data['o']['chatMessage'].get('mediaType', 0)}"
        self._trigger_event(self.chat_methods.get(key, "default"), data)

    def _resolve_chat_action_start(self, data):
        self._trigger_event(self.chat_actions_start.get(data['o'].get('actions', 0), "default"), data)

    def _resolve_chat_action_end(self, data):
        self._trigger_event(self.chat_actions_end.get(data['o'].get('actions', 0), "default"), data)

    def _trigger_event(self, event_name, data):
        event = Event(data["o"]).Event
        self.call(event_name, event)
        self.call("all", event)

    def resolve(self, data):
        data = loads(data)
        method = self.methods.get(data["t"], self.default)
        return method(data)

    def call(self, type, data):
        for handler in self.handlers.get(type, []):
            handler(data)

    def event(self, type):
        def registerHandler(handler):
            self.handlers.setdefault(type, []).append(handler)
            return handler
        return registerHandler

    def default(self, data): 
        self.call("default", data)



class SocketHandler(Callbacks):
    def __init__(self, client, debug=False):
        super().__init__()
        self.socket_url = "ws://ws1.aminoapps.com"
        self.client = client
        self.debug = debug
        self.socket = None
        self.thread_event = threading.Event()
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 5
        self._socket_lock = threading.Lock()
        self._is_connecting = False
        self._debug_print = lambda msg: print(msg) if self.debug else None

    def on_message(self, ws, data):
        self.resolve(data)

    def is_connected(self):
        return self.socket and self.socket.sock and self.socket.sock.connected

    def safe_reconnect(self):
        """Safely reconnects the socket with retry logic"""
        with self._socket_lock:
            if self._is_connecting:
                self._debug_print("[socket][reconnect] Connection already in progress")
                return False
                
            if self.reconnect_attempts >= self.max_reconnect_attempts:
                self._debug_print("[socket][reconnect] Max reconnection attempts reached")
                self.reconnect_attempts = 0
                return False

            try:
                self._is_connecting = True
                self._debug_print(f"[socket][reconnect] Attempt {self.reconnect_attempts + 1}")
                
                if self.socket:
                    try:
                        self.socket.close()
                    except:
                        pass
                    self.socket = None
                    
                self.run_amino_socket()
                sleep(self.reconnect_delay)
                
                if self.is_connected():
                    self.reconnect_attempts = 0
                    return True
                    
                self.reconnect_attempts += 1
                return False
            except:
                self.reconnect_attempts += 1
                sleep(self.reconnect_delay)
                return False
            finally:
                self._is_connecting = False

    def send(self, data):
        self._debug_print(f"[socket][send] Sending Data : {data}")
        
        retry_count = 0
        while retry_count < 3:
            if not self.is_connected():
                if not self.safe_reconnect():
                    retry_count += 1
                    continue
                    
            try:
                self.socket.send(data)
                return True
            except Exception as e:
                self._debug_print(f"[socket][send] Error: {str(e)}")
                retry_count += 1
                sleep(1)
                
        self._debug_print("[socket][send] Failed to send message after retries")
        return False

    def on_close(self, ws, data, status):
        self._debug_print("[socket][reconnect_handler] Reconnecting Socket")
        self.safe_reconnect()

    def on_error(self, ws, error):
        traceback.print_exc()
        print("On error: ", error)

    def on_open(self, ws):
        self._debug_print("[socket][start] Socket Started")
        self.thread_event.set()

    def on_ping(self, ws, somesing):
        self._debug_print("[socket][Ping] Servier send ping")
        self.send(dumps({"t": 116, "o": {"threadChannelUserInfoList": []}}))

    def on_pong(self, ws, somesing):
        self._debug_print("server send pong")

    def starting_process(self):
        deviceId = gen_deviceId()

        final = f"{deviceId}|{int(time() * 1000)}"

        headers = {
            "NDCDEVICEID": deviceId,
            "NDCAUTH": f"sid={self.client.sid}",
            "NDC-MSG-SIG": signature(final)
        }

        self.socket = WebSocketApp(
            f"{self.socket_url}/?signbody={final.replace('|', '%7C')}",
            on_open=self.on_open,
            on_error=self.on_error,
            on_ping=self.on_ping,
            on_pong=self.on_pong,
            on_message=self.on_message,
            on_close=self.on_close,
            header=headers,
        )

        threading.Thread(target=self.socket.run_forever, kwargs={
            "sslopt": {"cert_reqs": ssl.CERT_NONE},
            "skip_utf8_validation": True,
            "ping_interval": 60*5,
            "ping_payload": dumps({"t": 116, "o": {"threadChannelUserInfoList": []}})
        }).start()

    def run_amino_socket(self):
        if self.client.sid is None:
            return

        threading.Thread(target=self.starting_process).start()
        self.thread_event.wait()

class SocketRequests:
    def __init__(self, client) -> None:
        self.client = client
        self.active_live_chats = set()

    def join_voice_chat(self, comId: int, chatId: str, joinType: int = 1):
        """
        Joins a Voice Chat
        **Parameters**
            - **comId** : ID of the Community
            - **chatId** : ID of the Chat
        """

        # Made by Light, Ley and Phoenix

        data = {
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "joinRole": joinType,
            },
            "t": 112
        }
        data = dumps(data)
        self.client.send(data)

    def join_video_chat(self, comId: int, chatId: str, joinType: int = 1):
        """
        Joins a Video Chat
        **Parameters**
            - **comId** : ID of the Community
            - **chatId** : ID of the Chat
        """

        # Made by Light, Ley and Phoenix

        data = {
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "joinRole": joinType,
                "channelType": 5,
            },
            "t": 108
        }
        data = dumps(data)
        self.client.send(data)

 
    def run_vc(self, comId: int, chatId: str, joinType: str):
        while chatId in self.active_live_chats:
            try:
                self.join_voice_chat(
                    comId=comId,
                    chatId=chatId,
                    joinType=joinType
                )
                sleep(60)

            except Exception as e:
                print(e)

    def start_vc(self, comId: int, chatId: str, joinType: int = 1):
        self.join_voice_chat(
            comId=comId,
            chatId=chatId,
            joinType=joinType
        )
        data = {
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "jointype": joinType,
                "channelType": 1,
            },
            "t": 108
        }
        data = dumps(data)
        self.client.send(data)
        self.active_live_chats.add(chatId)
        threading.Thread(target=self.run_vc, args=(comId, chatId, joinType)).start()

    def end_vc(self, comId: int, chatId: str, joinType: int = 2):
        self.active_live_chats.discard(chatId)
        self.join_voice_chat(
            comId=comId,
            chatId=chatId,
            joinType=joinType
        )
        

    def start_video_chat(self, comId: str, chatId: str, joinType: int = 1):
        self.join_voice_chat(
            comId=comId,
            chatId=chatId,
            joinType=joinType
        )

        data = {
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "joinRole": joinType,
                "channelType": 4,
            },
            "t": 108
        }
        data = dumps(data)
        self.client.send(data)

    def Browsing(self, comId: int, blogId: str = None, blogType: int = 0):
        """
        Send Browsing Action

        **Paramaters**
            - **blogId**: 2 For Public 1 & 0 For Private (str)
            - **blogType**: Type Of the Blog *poll & blog & wiki* (int)

        **Return**
            - None
        """
        if blogId and blogType:
            target = f"ndc://x{comId}/blog/"
        else:
            target = f"ndc://x{comId}/featured"

        data = {
            "o": {
                "actions": ["Browsing"],
                "target": target,
                "ndcId": int(comId),
                "params": {"blogType": blogType},
            },
            "t": 306
        }
        data = dumps(data)
        self.client.send(data)

    def Chatting(self, comId: int, chatId: str, threadType: int = 2):
        """
        Send Chatting Action

        **Paramaters**
            - **threadType**: 2 For Public 1 & 0 For Private (int)

        **Return**
            - None
        """
        data = {
            "o": {
                "actions": ["Chatting"],
                "target": f"ndc://x{comId}/chat-thread/{chatId}",
                "ndcId": int(comId),
                "params": {
                    "duration": 12800,
                    "membershipStatus": 1,
                    "threadType": threadType
                },
            },
            "t": 306
        }
        data = dumps(data)
        self.client.send(data)

    def PublicChats(self, comId: int,):
        """
        Send PublicChats Action

        **Return**
            - None
        """
        data = {
            "o": {
                "actions": ["Browsing"],
                "target": f"ndc://x{comId}/public-chats",
                "ndcId": int(comId),
                "params": {"duration": 859},
            },
            "t": 306
        }
        data = dumps(data)
        self.client.send(data)

    def LeaderBoards(self, comId: int,):
        """
        Send LeaderBoard Action

        **Return**
            - None
        """
        data = {
            "o": {
                "actions": ["Browsing"],
                "target": f"ndc://x{comId}/leaderboards",
                "ndcId": int(comId),
                "params": {"duration": 859},
            },
            "t": 306
        }
        data = dumps(data)
        self.client.send(data)

    def typing_request(self, comId: int, chatId: str, stop: bool):
        data = {
            "o": {
                "actions": ["Typing"],
                "target": f"ndc://x{comId}/chat-thread/{chatId}",
                "ndcId": comId,
            },
            "t": 306 if stop else 304
        }
        data = dumps(data)
        self.client.send(data)

    def recording_request(self, comId: int, chatId: str, stop: bool):
        data = {
            "o": {
                "actions": ["Recording"],
                "target": f"ndc://x{comId}/chat-thread/{chatId}",
                "ndcId": comId,
            },
            "t": 306 if stop else 304
        }
        data = dumps(data)
        self.client.send(data)

