from fastapi import WebSocket, WebSocketDisconnect
import json

class ConnectionManager:
    def __init__(self):
        self.sockets = {} #player nickname -> websocket
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        connection_message = await websocket.receive_text()
        json_object = json.loads(json.loads(connection_message))
        name = json_object["name"]
        #TODO: sprawdzenie nicku
        #TODO: blokowanie zasobu
        self.sockets[name] = websocket
        
        await self.handle_client(websocket)
        # while True:
        #     data = await websocket.receive_text()
        #     await websocket.send_text(f"Message text was: {data}")
        
    async def broadcast(self, message: dict):
        for player in self.sockets.keys():
            await self.sockets[player].send_text(json.dumps(message))
            
    def get_sockets(self):
        return self.sockets

    async def handle_client(self, websocket: WebSocket):
        while True:
            data = await websocket.receive_text()
            print(data)
            await websocket.send_text(f"Message text was: {data}")