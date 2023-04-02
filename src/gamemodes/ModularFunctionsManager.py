class ModularFunctionsManager:

    def __init__(self, player_manager, room):
        self.player_manager = player_manager
        self.room = room

    def get_modular_functions(self):
        return [
            self.all_players_finished,
            self.level_time_elapsed,
            self.test
        ]

    def all_players_finished(self):
        players = self.player_manager.get_players_list()
        return all(player.did_finish_level() for player in players)

    def level_time_elapsed(self):
        return self.room.level_time_elapsed

    def test(self):
        print("Hello")
        return True
