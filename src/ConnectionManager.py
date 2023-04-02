from fastapi import WebSocket, WebSocketDisconnect
from PlayerManager import PlayerManager
import asyncio

class ConnectionManager:
    def __init__(self, player_manager: PlayerManager, queue: asyncio.Queue, room):
        self.player_manager = player_manager
        self.queue = queue
        self.room = room

    async def connect(self, websocket: WebSocket, name: str) -> None:

        if self.room.is_game_running():
            raise RuntimeError("Game is running in this room.")
        
        try:
            await websocket.accept()
            self.player_manager.add_player(name, websocket)

            print("CONNECTED: ", name)

            await self.update_room()
            await self.receive_messages(websocket, name)

        except WebSocketDisconnect:
            await self.disconnect(name)

    async def broadcast(self, message: dict) -> None:
        print('BROADCAST:', message)
        for player in self.player_manager.get_players_list():
            message['your_name'] = player.get_name()
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
            "room_id": self.room.get_id(),
            "players": player_infos
        }

        await self.broadcast(message)
