from fastapi import WebSocket

class Player:
    def __init__(self, name: str, websocket: WebSocket):
        self.name = name
        self.websocket = websocket
        self.total_score = 0
        self.game_score = 0
        self.finished_level = False

    def add_score(self, new_points: int) -> None:
        self.scores.append(new_points)
    
    def get_socket(self) -> WebSocket:
        return self.websocket
    
    def get_name(self) -> str:
        return self.name
    
    def get_info(self) -> dict:
        return {
            'name': self.name,
            'total_score': self.total_score,
            'game_score': self.game_score,
        }
    
    def finish_game(self) -> None:
        self.total_score += self.game_score
        self.game_score = 0
    
    def start_level(self) -> None:
        self.finished_level = False

    def did_finish_level(self) -> bool:
        return self.finished_level