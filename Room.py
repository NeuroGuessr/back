class Room:
    def __init__(self, id: int):
        self.id = id
        self.configuration = None
    
    def get_id(self):
        return self.id
    
    def get_configuration(self):
        return self.configuration
    
    def set_configuration(self, configuration: str):
        self.configuration = configuration