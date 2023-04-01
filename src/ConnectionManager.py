from fastapi import WebSocket, WebSocketDisconnect
from PlayerManager import PlayerManager
import asyncio


class ConnectionManager:
    def __init__(self, player_manager: PlayerManager, queue: asyncio.Queue):
        self.player_manager = player_manager
        self.queue = queue

    async def connect(self, websocket: WebSocket):
        try:
            await websocket.accept()
            
            accepted = False
            while not accepted:
                json_object = await websocket.receive_json()
                name = json_object["name"]
                if self.player_manager.add_player(name, websocket):
                    accepted = True
                else:
                    await self.send_duplicate_name_error(websocket, name)

            print("CONNECTED: ", name)

            await self.receive_messages(websocket, name)

        except WebSocketDisconnect:
            await self.disconnect_player(name)

    async def send_duplicate_name_error(self, websocket: WebSocket, name: str):
        websocket.send_json({
            'type': 'error', 
            'error_message': f'User {name} exists in this room.'
        })

    async def broadcast(self, message: dict):
        for player in self.players.values():
            await player['socket'].send_json(message)

    def get_players(self):
        return self.players

    async def receive_messages(self, websocket: WebSocket, name: str):
        while True:
            message = await websocket.receive_json()
            print("RECEIVE:", message)
            await self.queue.put((name, message))

    async def disconnect_player(self, player: str):
        print("DISCONNECTED:", player)
        self.player_manager.remove_player(player)
        await self.update_players_list()

    async def update_players_list(self):
        message = {
            "type": "players_list",
            "players": self.player_manager.get_players_list()
        }
        await self.broadcast(message)
        print('BROADCAST:', message)
