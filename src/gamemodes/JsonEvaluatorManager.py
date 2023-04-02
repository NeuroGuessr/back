import json

from gamemodes.JsonEvaluator import JsonEvaluator
from gamemodes.ModularFunctionsManager import ModularFunctionsManager
import os
from os import path


class JsonEvaluatorManager:
    def __init__(self, json_path, room):
        self.modular_functions_manager = ModularFunctionsManager(room.player_manager, room)
        self.json_evaluator = JsonEvaluator(
            self.modular_functions_manager.get_modular_functions(),
            json_path
        )
        self.level_json = self.load_level_json(json_path)

    def load_level_json(self, json_path):
        try:
            with open(json_path, 'r') as f:
                return json.load(f)
        except:
            raise Exception("Could not open or parse " + json_path)

    def get_level_time(self):
        return self.get_variable_value('level_time')

    def get_variable_value(self, var_name):
        return self.json_evaluator.get_variable_value(var_name)

    def evalaute(self, string):
        return self.json_evaluator.evaluate_from_string(string)

    def check_finish_level(self):
        return self.string_to_bool(self.evalaute(self.level_json['rules']['end_condition']))

    def string_to_bool(self, bool_as_string):
        if bool_as_string == "True":
            return True
        if bool_as_string == "False":
            return False
        raise ValueError("Trying to parse " + str(bool_as_string) + " as bool.")
