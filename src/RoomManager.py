from Room import Room
from uuid import uuid4
import asyncio

class RoomManager:
    def __init__(self):
        self.rooms = {}
        
    def create_room(self):
        # room_id = uuid4()
        room_id = 1 # TODO: change to uuid

        new_room = Room(room_id, '')
        self.rooms[room_id] = new_room

        print('CREATE ROOM:', room_id)

        asyncio.create_task(new_room.engine())
        return room_id
        
    def remove_room(self, room_id: int):
        del self.rooms[room_id]
        
    def get_room(self, room_id: int):
        return self.rooms[room_id]

    def get_rooms(self):
        return self.rooms