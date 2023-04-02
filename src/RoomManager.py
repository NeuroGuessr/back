from Room import Room
import asyncio

class RoomManager:
    def __init__(self):
        self.rooms = {}
        self.unique_id = 0
        
    def create_room(self) -> int:
        room_id = self.unique_id
        self.unique_id += 1

        new_room = Room(room_id, '')
        self.rooms[room_id] = new_room

        print('CREATE ROOM:', room_id)

        asyncio.create_task(new_room.engine())
        return room_id
        
    def remove_room(self, room_id: int) -> None:
        del self.rooms[room_id]
        
    def get_room(self, room_id: int) -> Room:
        if room_id not in self.rooms:
            raise RuntimeError(f"Room {room_id} doesn't exists")
        return self.rooms[room_id]

    def get_rooms(self) -> dict:
        return self.rooms