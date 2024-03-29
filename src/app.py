from fastapi import FastAPI, WebSocket, HTTPException
from RoomManager import RoomManager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import json
from LevelManager import LevelManager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="../static"), name="static")

room_manager = RoomManager()

@app.get("/")
async def root():
    return "Up and running"

@app.get("/room")
async def list_rooms():
    # await level_manager.fetch_all(2, 2)
    rooms = [room.get_id() for room in room_manager.get_rooms().values()]
    return json.dumps(rooms)

@app.get("/room/{room_id}/player")
def list_players(room_id: int):
    player_manager = room_manager.get_room(room_id).get_player_manager()
    player_infos = player_manager.get_player_infos()
    return json.dumps(player_infos)

@app.post("/room")
async def create_room():
    # await level_manager.fetch_all(
    #     2,
    #     2
    # )
    room_id = room_manager.create_room()
    return JSONResponse({'room_id': room_id})

@app.websocket("/ws/room/{room_id}/player/{name}")
async def websocket_room(websocket: WebSocket, room_id: int, name: str):
    try:
        connection_manager = room_manager.get_room(room_id).get_connection_manager()
        await connection_manager.connect(websocket, name)
    except RuntimeError as e:
        await websocket.send_json({
            'type': 'error',
            'message': str(e),
        })
    
