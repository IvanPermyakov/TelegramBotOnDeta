from .enums import dispatches, try_enum
from .message import Message

def dispatch(data: dict) -> dispatches:
    if dispatches.message.value in data:
        return dispatches.message
    elif dispatches.edited_message.value in data:
        return dispatches.edited_message
    elif dispatches.channel_post.value in data:
        return dispatches.channel_post
    elif dispatches.edited_channel_post.value in data:
        return dispatches.edited_channel_post
    else:
        return dispatches.unknown

class Context:
    def __init__(self, payload: dict):
        self._payload = payload
        self.type = dispatch(payload)
        self._data = payload.get(self.type.value)
        self.id = payload['update_id']
    @property
    def message(self) -> Message:
        if self.type is not dispatches.unknown:
            return Message(self._data)
            