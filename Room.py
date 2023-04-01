from ConnectionManager import ConnectionManager
import asyncio

class Room:
    def __init__(self, id: int, configuration: str):
        self.id = id
        self.configuration = configuration
        self.queue = asyncio.Queue()
        self.connection_manager = ConnectionManager(self.queue)
    
    def get_id(self):
        return self.id
    
    def get_configuration(self):
        return self.configuration
    
    def set_configuration(self, configuration: str):
        self.configuration = configuration
        
    def get_connection_manager(self):
        return self.connection_manager
    
    async def engine(self):
        print("ENGINE START")
        while True:
            data = await self.queue.get()
            print('Q', data)
            