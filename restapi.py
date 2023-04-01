from fastapi import FastAPI, WebSocket
from enum import Enum
from pydantic import BaseModel
from RoomManager import RoomManager
from Room import Room
from uuid import uuid4
from ConnectionManager import ConnectionManager
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

room_manager = RoomManager()
room = Room(1, "")
room_manager.add_room(room)

@app.get("/")
async def root():
    await room.engine()
    return "Up and running"

@app.get("/room")
async def list_rooms():
    rooms = room_manager.get_rooms()
    return "rooms"

@app.post("/room")
async def add_room():
    room_id = uuid4()
    room = Room(room_id, "")
    room_manager.add_room(room)
    room.engine()
    return str(room_id)

@app.get("/room/{room_id}")
async def join_room(room_id: int):
    return "join room: " + str(room_id)

@app.get("/room/{room_id}/player")
def list_players(room_id: int):
    sockets = room_manager.get_rooms()[room_id].get_connection_manager().get_sockets()

    return json.dumps(list(sockets.keys()))

@app.websocket("/ws/room/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    manager = room_manager.get_rooms()[room_id].get_connection_manager()
    await manager.connect(websocket)