class Room:
    def __init__(self, id: int, configuration: str, websocket: WebSocket):
        self.id = id
        self.configuration = configuration
        self.websocket = websocket
    
    def get_id(self):
        return self.id
    
    def get_configuration(self):
        return self.configuration
    
    def set_configuration(self, configuration: str):
        self.configuration = configuration
        
    def get_websocket(self):
        return self.websocket
    