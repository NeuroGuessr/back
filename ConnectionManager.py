from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio

class ConnectionManager:
    def __init__(self, queue : asyncio.Queue):
        self.sockets = {} #player nickname -> websocket
        self.queue = queue
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        json_object = await websocket.receive_json()
        print("NEW USER: ", json_object)
        
        name = json_object["name"]

        #TODO: sprawdzenie nicku
        #TODO: blokowanie zasobu
        self.sockets[name] = websocket
        await self.receive_messages_from(name)
        
    async def broadcast(self, message: dict):
        for player in self.sockets.keys():
            await self.sockets[player].send_json(message)
            
    def get_sockets(self):
        return self.sockets

    async def receive_messages_from(self, name: str):
        socket = self.sockets[name]
        while True:
            message = await socket.receive_json()
            print("RECEIVE:", message)
            await self.queue.put(message)