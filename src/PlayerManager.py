from fastapi import WebSocket
from Player import Player
import asyncio

class PlayerManager:
    def __init__(self):
        self.players = {}
        self.lock = asyncio.Lock()

    async def add_player(self, name: str, websocket: WebSocket) -> bool:
        await self.lock.acquire()
        try:
            if name in self.players.keys():
                return False

            self.players[name] = Player(name, websocket)
            return True
        
        finally:
            self.lock.release()

    def remove_player(self, name: str) -> None:
        self.players.pop(name, None)

    def get_socket(self, name: str) -> WebSocket:
        player = self.players.get(name, None)
        if player:
            return self.get_socket()

    def add_score(self, name: str, new_points: int) -> None:
        player = self.players.get(name, None)
        if player:
            player.add_score(new_points)
    
    def start_level_for_all_players(self) -> None:
        for player in self.players.values():
            player.start_level()

    def finish_game_for_all_players(self) -> None:
        for player in self.players.values():
            player.finish_game()
    
    def get_player_infos(self) -> dict:
        return {name: player.get_info() for name, player in self.players.items()}

    def get_players_list(self) -> list:
        return list(self.players.values())

    def is_empty(self) -> bool:
        return not self.players
        