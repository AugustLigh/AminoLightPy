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

class SocketHandler:
    def __init__(self, client, debug=False):
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

    def on_message(self, ws, data):
        self.client.handle_socket_message(data)

    def is_connected(self):
        return self.socket and self.socket.sock and self.socket.sock.connected

    def safe_reconnect(self):
        """Safely reconnects the socket with retry logic"""
        with self._socket_lock:
            if self._is_connecting:
                self.debug_print("[socket][reconnect] Connection already in progress")
                return False
                
            if self.reconnect_attempts >= self.max_reconnect_attempts:
                self.debug_print("[socket][reconnect] Max reconnection attempts reached")
                self.reconnect_attempts = 0
                return False

            try:
                self._is_connecting = True
                self.debug_print(f"[socket][reconnect] Attempt {self.reconnect_attempts + 1}")
                
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
        self.debug_print(f"[socket][send] Sending Data : {data}")
        
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
                self.debug_print(f"[socket][send] Error: {str(e)}")
                retry_count += 1
                sleep(1)
                
        self.debug_print("[socket][send] Failed to send message after retries")
        return False

    def on_close(self, ws, data, status):
        self.debug_print("[socket][reconnect_handler] Reconnecting Socket")
        self.starting_process()

    def on_error(self, ws, error):
        traceback.print_exc()
        print("On error: ", error)

    def on_open(self, ws):
        self.debug_print("[socket][start] Socket Started")
        self.thread_event.set()

    def on_ping(self, ws, somesing):
        self.debug_print("[socket][Ping] Servier send ping")
        self.send(dumps({"t": 116, "o": {"threadChannelUserInfoList": []}}))

    def on_pong(self, ws, somesing):
        self.debug_print("server send pong")

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

    def debug_print(self, message):
        if self.debug:
            print(message)

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
        print(data)
        self.client.send(data)

class Callbacks:
    def __init__(self):
        self.handlers = {}

        self.methods = {
            304: self._resolve_chat_action_start,
            306: self._resolve_chat_action_end,
            1000: self._resolve_chat_message
        }

        self.chat_methods = {
            "0:0": self.on_text_message,
            "0:100": self.on_image_message,
            "0:103": self.on_youtube_message,
            "1:0": self.on_strike_message,
            "2:110": self.on_voice_message,
            "3:113": self.on_sticker_message,
            "52:0": self.on_voice_chat_not_answered,
            "53:0": self.on_voice_chat_not_cancelled,
            "54:0": self.on_voice_chat_not_declined,
            "55:0": self.on_video_chat_not_answered,
            "56:0": self.on_video_chat_not_cancelled,
            "57:0": self.on_video_chat_not_declined,
            "100:0": self.on_delete_message,
            "101:0": self.on_group_member_join,
            "102:0": self.on_group_member_leave,
            "103:0": self.on_chat_invite,
            "104:0": self.on_chat_background_changed,
            "105:0": self.on_chat_title_changed,
            "106:0": self.on_chat_icon_changed,
            "107:0": self.on_voice_chat_start,
            "108:0": self.on_video_chat_start,
            "110:0": self.on_voice_chat_end,
            "111:0": self.on_video_chat_end,
            "113:0": self.on_chat_content_changed,
            "114:0": self.on_screen_room_start,
            "115:0": self.on_screen_room_end,
            "116:0": self.on_chat_host_transfered,
            "117:0": self.on_text_message_force_removed,
            "118:0": self.on_chat_removed_message,
            "119:0": self.on_text_message_removed_by_admin,
            "120:0": self.on_chat_tip,
            "121:0": self.on_chat_pin_announcement,
            "122:0": self.on_voice_chat_permission_open_to_everyone,
            "123:0": self.on_voice_chat_permission_invited_and_requested,
            "124:0": self.on_voice_chat_permission_invite_only,
            "125:0": self.on_chat_view_only_enabled,
            "126:0": self.on_chat_view_only_disabled,
            "127:0": self.on_chat_unpin_announcement,
            "128:0": self.on_chat_tipping_enabled,
            "129:0": self.on_chat_tipping_disabled,
            "65281:0": self.on_timestamp_message,
            "65282:0": self.on_welcome_message,
            "65283:0": self.on_invite_message
        }

        self.chat_actions_start = {
            "Typing": self.on_user_typing_start,
        }

        self.chat_actions_end = {
            "Typing": self.on_user_typing_end,
        }

    def _resolve_chat_message(self, data):
        key = f"{data['o']['chatMessage']['type']}:{data['o']['chatMessage'].get('mediaType', 0)}"
        return self.chat_methods.get(key, self.default)(data)

    def _resolve_chat_action_start(self, data):
        key = data['o'].get('actions', 0)
        return self.chat_actions_start.get(key, self.default)(data)

    def _resolve_chat_action_end(self, data):
        key = data['o'].get('actions', 0)
        return self.chat_actions_end.get(key, self.default)(data)

    def resolve(self, data):
        data = loads(data)
        return self.methods.get(data["t"], self.default)(data)

    def call(self, type, data):
        if type in self.handlers:
            for handler in self.handlers[type]:
                handler(data)

    def event(self, type):
        def registerHandler(handler):
            if type in self.handlers:
                self.handlers[type].append(handler)
            else:
                self.handlers[type] = [handler]
            return handler

        return registerHandler

    def event_handler_decorator(func):
        def wrapper(self, data):
            event = Event(data["o"]).Event
            self.call(func.__name__, event)
            self.call("all", event)
        return wrapper

    @event_handler_decorator
    def on_text_message(self, data): pass
    @event_handler_decorator
    def on_image_message(self, data): pass
    @event_handler_decorator
    def on_youtube_message(self, data): pass
    @event_handler_decorator
    def on_strike_message(self, data): pass
    @event_handler_decorator
    def on_voice_message(self, data): pass
    @event_handler_decorator
    def on_sticker_message(self, data): pass
    @event_handler_decorator
    def on_voice_chat_not_answered(self, data): pass
    @event_handler_decorator
    def on_voice_chat_not_cancelled(self, data): pass
    @event_handler_decorator
    def on_voice_chat_not_declined(self, data): pass
    @event_handler_decorator
    def on_video_chat_not_answered(self, data): pass
    @event_handler_decorator
    def on_video_chat_not_cancelled(self, data): pass
    @event_handler_decorator
    def on_video_chat_not_declined(self, data): pass
    @event_handler_decorator
    def on_delete_message(self, data): pass
    @event_handler_decorator
    def on_group_member_join(self, data): pass
    @event_handler_decorator
    def on_group_member_leave(self, data): pass
    @event_handler_decorator
    def on_chat_invite(self, data): pass
    @event_handler_decorator
    def on_chat_background_changed(self, data): pass
    @event_handler_decorator
    def on_chat_title_changed(self, data): pass
    @event_handler_decorator
    def on_chat_icon_changed(self, data): pass
    @event_handler_decorator
    def on_voice_chat_start(self, data): pass
    @event_handler_decorator
    def on_video_chat_start(self, data): pass
    @event_handler_decorator
    def on_voice_chat_end(self, data): pass
    @event_handler_decorator
    def on_video_chat_end(self, data): pass
    @event_handler_decorator
    def on_chat_content_changed(self, data): pass
    @event_handler_decorator
    def on_screen_room_start(self, data): pass
    @event_handler_decorator
    def on_screen_room_end(self, data): pass
    @event_handler_decorator
    def on_chat_host_transfered(self, data): pass
    @event_handler_decorator
    def on_text_message_force_removed(self, data): pass
    @event_handler_decorator
    def on_chat_removed_message(self, data): pass
    @event_handler_decorator
    def on_text_message_removed_by_admin(self, data): pass
    @event_handler_decorator
    def on_chat_tip(self, data): pass
    @event_handler_decorator
    def on_chat_pin_announcement(self, data): pass
    @event_handler_decorator
    def on_voice_chat_permission_open_to_everyone(self, data): pass
    @event_handler_decorator
    def on_voice_chat_permission_invited_and_requested(self, data): pass
    @event_handler_decorator
    def on_voice_chat_permission_invite_only(self, data): pass
    @event_handler_decorator
    def on_chat_view_only_enabled(self, data): pass
    @event_handler_decorator
    def on_chat_view_only_disabled(self, data): pass
    @event_handler_decorator
    def on_chat_unpin_announcement(self, data): pass
    @event_handler_decorator
    def on_chat_tipping_enabled(self, data): pass
    @event_handler_decorator
    def on_chat_tipping_disabled(self, data): pass
    @event_handler_decorator
    def on_timestamp_message(self, data): pass
    @event_handler_decorator
    def on_welcome_message(self, data): pass
    @event_handler_decorator
    def on_invite_message(self, data): pass
    
    @event_handler_decorator
    def on_user_typing_start(self, data): pass
    @event_handler_decorator
    def on_user_typing_end(self, data): pass

    def default(self, data): self.call("default", data)

    @event_handler_decorator
    def all(self, data): pass