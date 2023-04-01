from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio

class ConnectionManager:
    def __init__(self, queue : asyncio.Queue):
        self.sockets = {} #player nickname -> websocket
        self.queue = queue
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        connection_message = await websocket.receive_text()
        # json_object = json.loads(json.loads(connection_message))
        json_object = json.loads(connection_message)
        print(json_object)
        name = json_object["name"]
        #TODO: sprawdzenie nicku
        #TODO: blokowanie zasobu
        self.sockets[name] = websocket

        await self.receive_messages(websocket)
        
    async def broadcast(self, message: dict):
        for player in self.sockets.keys():
            await self.sockets[player].send_text(json.dumps(message))
            
    def get_sockets(self):
        return self.sockets

    async def receive_messages(self, websocket: WebSocket):
        while True:
            data = await websocket.receive_text()
            print(data)
            await self.queue.put(data)

    def safely_parse_message(message):
        result = json.loads(message)
        if type(result) != dict:
            result = json.loads(message)
        return result
