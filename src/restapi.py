from fastapi import FastAPI, WebSocket
from RoomManager import RoomManager
from fastapi.staticfiles import StaticFiles
import json
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")

room_manager = RoomManager()
room_manager.create_room()

@app.get("/")
async def root():
    return room_manager.get_rooms()

@app.get("/room")
async def list_rooms():
    rooms = room_manager.get_rooms()
    return "rooms"

@app.get("/room/{room_id}/player")
def list_players(room_id: int):
    sockets = room_manager.get_rooms()[room_id].get_connection_manager().get_sockets()
    return json.dumps(list(sockets.keys()))

@app.websocket("/ws/room")
async def websocket_create_room(websocket: WebSocket):
    room_id = room_manager.create_room()
    await websocket_join_room(websocket, room_id)
                             
@app.websocket("/ws/room/{room_id}")
async def websocket_join_room(websocket: WebSocket, room_id: int):
    connection_manager = room_manager.get_room(room_id).get_connection_manager()
    await connection_manager.connect(websocket)