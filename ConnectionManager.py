from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio

class ConnectionManager:
    def __init__(self, queue : asyncio.Queue):
        self.players = {} #player nickname -> {}
        self.queue = queue
        
    async def connect(self, websocket: WebSocket):
        try:
            await websocket.accept()

            json_object = await websocket.receive_json()
            print("CONNECTED: ", json_object)
            
            name = json_object["name"]

            #TODO: sprawdzenie nicku
            #TODO: blokowanie zasobu
            self.players[name] = {
                'socket': websocket,
                'score': 0
            }
            await self.receive_messages(websocket, name)
        except WebSocketDisconnect:
            print("DISCONNECTED:", name)
            self.players.pop(name)
        
    async def broadcast(self, message: dict):
        for player in self.players.values():
            await player['socket'].send_json(message)
            
    def get_players(self):
        return self.players

    async def receive_messages(self, socket: WebSocket, name: str):
        while True:
            message = await socket.receive_json()
            print("RECEIVE:", message)
            await self.queue.put((name, message))

