class PhotoResp:
    def __init__(self, payload: dict):
        self._payload = payload
        self.ok = payload['ok']
        self.result = Res(self._payload['result'])

class Res:
    def __init__(self, payload: dict):
        self.file_id: str = payload['file_id']
        self.file_unique_id: str = payload['file_unique_id']
        self.file_size: str = payload['file_size']
        self.file_path: str = payload['file_path']