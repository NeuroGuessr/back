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
            print('Q:', data)

            await self.handle_message(data)

    async def handle_message(self, data):
        name, message = data
        if message["type"] == "start_game":
            await self.connection_manager.broadcast(self.create_level())

            if message['type'] == 'choice':
                pass


    def create_level(self):
        return {
            "type": "level",
            "images": [
                "1.jpg", "2.jpg", "3.jpg", "4.jpg"
            ],
            "labels": [
                "Aaaaaa", "Bbbbb", "Ccccccccc", "Ddddd"
            ]
        }