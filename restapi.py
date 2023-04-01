from fastapi import FastAPI, WebSocket
from enum import Enum
from pydantic import BaseModel
from RoomManager import RoomManager
from Room import Room
from uuid import uuid4
from ConnectionManager import ConnectionManager

app = FastAPI()

room_manager = RoomManager()

room_manager.add_room(Room(1, "", ConnectionManager))

@app.get("/")
async def root():
    return "Up and running"

@app.get("/room")
async def list_rooms():
    rooms = room_manager.get_rooms()
    return "rooms"

@app.post("/room")
async def add_room():
    room_id = uuid4()
    room = Room(room_id, "", ConnectionManager())
    room_manager.add_room(room)
    return str(room_id)

@app.get("/room/{room_id}")
async def join_room(room_id: int):
    return "join room: " + str(room_id)

@app.websocket("/ws/room/{room_id}")
async def websocket_endpoint(room_id: int, websocket: WebSocket):
    room_manager.get_rooms()[room_id].get_connection_manager.connect(websocket)
    