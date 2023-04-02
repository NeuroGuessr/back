from ConnectionManager import ConnectionManager
from PlayerManager import PlayerManager
import asyncio
from Timer import Timer
from uuid import uuid4

# ========================================================
LEVEL0 = {
    "type": "level",
    "images": ["1.jpg", "2.jpg", "3.jpg", "4.jpg"],
            "labels": [
                "Aaaaaa", "Bbbbb", "Ccccccccc", "Ddddd"
    ]
}
LEVEL1 = {
    "type": "level",
    "images": ["5.jpg", "6.jpg", "7.jpg", "12.jpg"],
            "labels": [
                "Aaaaaa", "Bbbbb", "Ccccccccc", "Ddddd"
    ]
}
LEVEL2 = {
    "type": "level",
    "images": ["13.jpg", "14.jpg", "15.jpg", "1.jpg"],
            "labels": [
                "Aaaaaa", "Bbbbb", "Ccccccccc", "Ddddd"
    ]
}
CORRECT_LEVEL = {"1.jpg": "Aaaaaa", "2.jpg": "Bbbbb",
                 "3.jpg": "Ccccccccc", "4.jpg": "Ddddd"}

GAME = [LEVEL0, LEVEL1, LEVEL2]
# ========================================================


class Room:
    FINISH_LEVEL_POLLING_TIME = 1
    LEVEL_TIME = 5

    def __init__(self, room_id: int, configuration: str):
        self.id = room_id
        self.configuration = configuration
        self.queue = asyncio.Queue()
        self.player_manager = PlayerManager()
        self.connection_manager = ConnectionManager(self.player_manager, self.queue, room_id)
        self.timer = Timer(self.queue)

        self.level_number = 0
        self.game_id = None
        self.level_time_elapsed = False

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

        if message_type == 'start_game' and self.game_id is None:
            await self.handle_start_game()
        elif message_type == 'choice' and self.game_id is not None:
            self.handle_choice(name, message)
        elif message_type == 'check_finish_level' and self.game_id is not None:
            await self.handle_check_finish_level(message)
        elif message_type == 'level_time_elapsed' and self.game_id is not None:
            await self.handle_level_time_elapsed(message)

    # EVENT HANDLERS
    async def handle_start_game(self) -> None:
        self.game_id = uuid4()
        self.level_number = 0
        await self.start_level()

    def handle_choice(self, message) -> None:
        if message['level_number'] == self.level_number:
            points = self.count_points(message['choices'], CORRECT_LEVEL)
            self.player_manager.add_score(message['name'], points)

    async def handle_check_finish_level(self, message) -> None:
        if self.is_level_finished() or self.level_time_elapsed:
            await self.finish_level()
        else:
            self.timer.remind(Room.FINISH_LEVEL_POLLING_TIME, {'type': 'check_finish_level'})

    async def handle_level_time_elapsed(self, message) -> None:
        if message['level_number'] == self.level_number and message['game_id'] == self.game_id:
            self.level_time_elapsed = True

    # STATE TRANSITION FUNCTIONS
    async def start_level(self) -> None:
        print("START LEVEL:", self.level_number)

        self.player_manager.start_level_for_all_players()
        await self.connection_manager.broadcast(self.get_current_level())

        self.level_time_elapsed = False
        self.timer.remind(Room.FINISH_LEVEL_POLLING_TIME, {'type': 'check_finish_level'})
        self.timer.remind(Room.LEVEL_TIME, {'type': 'level_time_elapsed', 'level_number': self.level_number, 'game_id': self.game_id})

    async def finish_level(self) -> None:
        print("FINISH LEVEL:", self.level_number)

        await self.connection_manager.update_room()

        self.level_number += 1
        if self.level_number < len(GAME):
            await self.start_level()
        else:
            await self.finish_game()

    async def finish_game(self):
        print("FINISH GAME")

        self.game_id = None
        self.player_manager.finish_game_for_all_players()
        await self.connection_manager.broadcast({'type': 'game_finished'})

    #================================================================
    def is_level_finished(self) -> bool:
        players = self.player_manager.get_players_list()
        return all(player.did_finish_level() for player in players)

    def count_points(self, choices: dir) -> int:
        points = 0
        for image, label in CORRECT_LEVEL.items():
            if label == choices.get(image, None):
                points += 1

        return max(points-1, 0)

    def get_current_level(self):
        level = GAME[self.level_number]
        level['time'] = Room.LEVEL_TIME
        level['level_number'] = self.level_number
        return level
    
    def get_levels_number(self):
        len(GAME)