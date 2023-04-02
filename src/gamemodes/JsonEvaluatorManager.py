import json

from gamemodes.JsonEvaluator import JsonEvaluator
from gamemodes.ModularFunctionsManager import ModularFunctionsManager
import os
from os import path


class JsonEvaluatorManager:
    def __init__(self, json_path, room):
        self.modular_functions_manager = ModularFunctionsManager(room.player_manager, room)
        self.json_evaluator = JsonEvaluator(
            self.modular_functions_manager.get_modular_functions()
        )
        print("Listing", os.listdir("gamemodes"))
        print("EXISTS:", os.path.exists("gamemodes/basic_pairs.json"))
        with open(json_path, 'r') as f:
            self.level_json = json.load(f)

    def evalaute(self, string):
        return self.json_evaluator.evaluate_from_string(string)

    def check_finish_level(self):
        return self.evalaute(self.level_json['rules']['end_condition'])
