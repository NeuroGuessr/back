from ConnectionManager import ConnectionManager

class Room:
    def __init__(self, id: int, configuration: str, connection_manager: ConnectionManager):
        self.id = id
        self.configuration = configuration
        self.connection_manager = connection_manager
    
    def get_id(self):
        return self.id
    
    def get_configuration(self):
        return self.configuration
    
    def set_configuration(self, configuration: str):
        self.configuration = configuration
        
    def get_connection_manager(self):
        return self.connection_manager
    