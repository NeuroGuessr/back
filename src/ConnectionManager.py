from fastapi import WebSocket, WebSocketDisconnect
from PlayerManager import PlayerManager
import asyncio


class ConnectionManager:
    def __init__(self, player_manager: PlayerManager, queue: asyncio.Queue, room_id: int):
        self.player_manager = player_manager
        self.queue = queue
        self.room_id = room_id

    async def connect(self, websocket: WebSocket) -> None:
        name = None
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

            await self.update_room()
            await self.receive_messages(websocket, name)

        except WebSocketDisconnect:
            await self.disconnect(name)

    async def send_duplicate_name_error(self, websocket: WebSocket, name: str) -> None:
        websocket.send_json({
            'type': 'error', 
            'error_message': f'User {name} exists in this room.'
        })

    async def broadcast(self, message: dict) -> None:
        print('BROADCAST:', message)
        for player in self.player_manager.get_players_list():
            try:
                websocket = player.get_socket()
                await websocket.send_json(message)
            except Exception as e:
                print("COULD NOT SEND TO:", player.get_name())
    
    async def receive_messages(self, websocket: WebSocket, name: str) -> None:
        while True:
            message = await websocket.receive_json()
            print("RECEIVED:", message)
            await self.queue.put((name, message))

    async def disconnect(self, player: str) -> None:
        print("DISCONNECTED:", player)
        self.player_manager.remove_player(player)
        await self.update_room()

    async def update_room(self) -> None:
        player_infos = self.player_manager.get_player_infos()

        message = {
            "type": "room",
            "room_id": self.room_id,
            "players": player_infos
        }

        await self.broadcast(message)
