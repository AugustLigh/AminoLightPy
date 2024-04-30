class Typing():
    def __init__(self, context, chatId: str, comId: int = None) -> None:
        self.chatId = chatId
        self.context = context
        self.comId = 0 if not comId else comId

    def __enter__(self):
        self.context.typing_request(self.comId, self.chatId, False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.typing_request(self.comId, self.chatId, True)    

class Recording():
    def __init__(self, context, chatId: str, comId: int = None) -> None:
        self.chatId = chatId
        self.context = context
        self.comId = 0 if not comId else comId

    def __enter__(self):
        self.context.recording_reqest(self.comId, self.chatId, False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.recording_reqest(self.comId, self.chatId, True) 