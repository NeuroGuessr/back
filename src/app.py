from fastapi import FastAPI, WebSocket
from RoomManager import RoomManager
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")

room_manager = RoomManager()
room_manager.create_room()

@app.get("/")
async def root():
    return "Up and running"

@app.get("/room")
async def list_rooms():
    rooms = [room.get_id() for room in room_manager.get_rooms().values()]
    return json.dumps(rooms)

@app.get("/room/{room_id}/player")
def list_players(room_id: int):
    player_manager = room_manager.get_room(room_id).get_player_manager()
    player_infos = player_manager.get_player_infos()
    return json.dumps(player_infos)

@app.websocket("/ws/room")
async def websocket_create_room(websocket: WebSocket):
    room_id = room_manager.create_room()
    await websocket_join_room(websocket, room_id)
                             
@app.websocket("/ws/room/{room_id}")
async def websocket_join_room(websocket: WebSocket, room_id: int):
    connection_manager = room_manager.get_room(room_id).get_connection_manager()
    await connection_manager.connect(websocket)