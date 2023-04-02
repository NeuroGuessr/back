from fastapi import FastAPI, WebSocket, HTTPException
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

@app.websocket("/ws/room/1")
async def endpoint(websocket: WebSocket):
    await websocket_room(websocket, "new", "abc")

@app.websocket("/ws/room/{room_id}/player/{name}")
async def websocket_room(websocket: WebSocket, room_id, name: str):
    try:
        if room_id == 'new':
            room_id = room_manager.create_room()

        connection_manager = room_manager.get_room(room_id).get_connection_manager()
        print(name)
        await connection_manager.connect(websocket, name)
    except RuntimeError as e:
        await websocket.send_json({
            'type': 'error',
            'message': str(e),
        })
    
