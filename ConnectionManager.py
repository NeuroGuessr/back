from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio

class ConnectionManager:
    def __init__(self, queue : asyncio.Queue):
        self.sockets = {} #player nickname -> websocket
        self.queue = queue
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        # connection_message = await websocket.receive_text()

        json_object = await self.safely_receive_message(websocket)
        print("NEW USER: ", json_object)
        
        name = json_object["name"]
        #TODO: sprawdzenie nicku
        #TODO: blokowanie zasobu
        self.sockets[name] = websocket
        await self.receive_messages_from(name)
        
    async def broadcast(self, message: dict):
        for player in self.sockets.keys():
            await self.sockets[player].send_text(json.dumps(message))
            
    def get_sockets(self):
        return self.sockets

    async def receive_messages_from(self, name: str):
        socket = self.sockets[name]
        while True:
            data = await self.safely_receive_message(socket)
            await self.queue.put(data)

    async def safely_receive_message(self, websocket : WebSocket):
        message = await websocket.receive_json()
        return message
        # result = json.loads(message)
        # if type(result) != dict:
        #     result = json.loads(message)
        # return result
    