import json

class Response():
    def __init__(self, status, message, data) -> None:
        self.status = status
        self.message = message
        self.data = data
          
    def GetMessage(self):
        return json.dumps({
            'meta' : {
                'status' : self.status,
                'message' : self.message,
            },
            'data' : self.data
        })