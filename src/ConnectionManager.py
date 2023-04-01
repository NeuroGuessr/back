from fastapi import WebSocket, WebSocketDisconnect
from PlayerManager import PlayerManager
import asyncio


class ConnectionManager:
    def __init__(self, player_manager: PlayerManager, queue: asyncio.Queue, room_id: int):
        self.player_manager = player_manager
        self.queue = queue
        self.room_id = room_id

    async def connect(self, websocket: WebSocket):
        try:
            await websocket.accept()
            
            accepted = False
            while not accepted:
                json_object = await websocket.receive_json()
                name = json_object["name"]
                print(name)
                if await self.player_manager.add_player(name, websocket):
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
        for player in self.player_manager.get_players_list():
            try:
                websocket = player.get_socket()
                await websocket.send_json(message)
            except Exception as e:
                print("COULD NOT SEND TO:", player.get_name())

    def get_players(self):
        return self.players

    async def receive_messages(self, websocket: WebSocket, name: str):
        while True:
            message = await websocket.receive_json()
            print("RECEIVED:", message)
            await self.queue.put((name, message))

    async def disconnect_player(self, player: str):
        print("DISCONNECTED:", player)
        self.player_manager.remove_player(player)
        await self.update_players_list()

    async def update_room(self):
        message = {
            "type": "room",
            "room_id": self.room_id,
            "players": self.player_manager.get_players_list()
        }
        await self.broadcast(message)
        print('BROADCAST:', message)
