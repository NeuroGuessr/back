from ConnectionManager import ConnectionManager
from PlayerManager import PlayerManager
import asyncio

# ========================================================
LEVEL = {
    "type": "level",
    "images": ["1.jpg", "2.jpg", "3.jpg", "4.jpg"],
            "labels": [
                "Aaaaaa", "Bbbbb", "Ccccccccc", "Ddddd"
    ]
}
CORRECT_LEVEL = {"1.jpg": "Aaaaaa", "2.jpg": "Bbbbb",
                 "3.jpg": "Ccccccccc", "4.jpg": "Ddddd"}
# ========================================================


class Room:
    def __init__(self, room_id: int, configuration: str):
        self.id = room_id
        self.configuration = configuration
        self.queue = asyncio.Queue()
        self.player_manager = PlayerManager()
        self.connection_manager = ConnectionManager(self.player_manager, self.queue, room_id)

    def get_id(self) -> int:
        return self.id

    def get_configuration(self) -> object:
        return self.configuration

    def set_configuration(self, configuration: str) -> None:
        self.configuration = configuration

    def get_connection_manager(self) -> ConnectionManager:
        return self.connection_manager
    
    def get_player_manager(self) -> PlayerManager:
        return self.player_manager

    async def engine(self) -> None:
        print('ENGINE START')

        while True:
            data = await self.queue.get()
            print('Q:', data)

            await self.handle_message(data)

    async def handle_message(self, data) -> None:
        name, message = data
        message_type = message['type']

        if message_type == 'start_game':
            await self.handle_start_game()  
        elif message_type == 'choice':
            self.handle_choice(name, message['choices'])

    async def handle_start_game(self) -> None:
        await self.connection_manager.broadcast(LEVEL)

    def handle_choice(self, name: str, choices: dir) -> None:
        points = self.count_points(choices, CORRECT_LEVEL)
        self.player_manager.add_score(name, points)

    def count_points(self, name: str, choices: dir, correct: dir) -> int:
        points = 0
        for image, label in CORRECT_LEVEL.items():
            if label == choices.get(image, None):
                points += 1

        return max(points-1, 0)
