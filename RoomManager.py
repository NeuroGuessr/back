class RoomManager:
    def __init__(self):
        self.rooms = {}
        
    def add_room(self, Room):
        self.rooms[Room.get_id()] = Room
        
    def remove_room(self, room_id: int):
        del self.rooms[room_id]
        
    def get_rooms(self):
        return self.rooms