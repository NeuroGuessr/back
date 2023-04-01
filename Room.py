from fastapi import WebSocket

class Room:
    def __init__(self, id: int, configuration: str):
        self.id = id
        self.configuration = configuration
        self.websocket = None
    
    def get_id(self):
        return self.id
    
    def get_configuration(self):
        return self.configuration
    
    def set_configuration(self, configuration: str):
        self.configuration = configuration
        
    def get_websocket(self):
        return self.websocket
    
    def set_websocket(self, websocket: WebSocket):
        self.websocket = websocket
    