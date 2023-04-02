import json

from gamemodes.JsonEvaluator import JsonEvaluator
from gamemodes.ModularFunctionsManager import ModularFunctionsManager


class JsonEvaluatorManager:
    def __init__(self):
        self.modular_functions_manager = None
        self.json_evaluator = None
        self.level_json = None

    def load_configuration(self, json_path, room):
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

    def get_scores(self):
        return int(self.json_evaluator.evaluate_from_string(self.level_json['rules']['score_function']))

    def get_stages(self):
        return int(self.get_variable_value('stages'))

    def get_stage_size(self):
        return int(self.get_variable_value('stage_size'))

    def get_level_time(self):
        return int(self.get_variable_value('level_time'))

    def get_variable_value(self, var_name):
        return self.json_evaluator.get_variable_value(var_name)

    def evaluate(self, string):
        return self.json_evaluator.evaluate_from_string(string)

    def check_finish_level(self):
        return self.string_to_bool(self.evaluate(self.level_json['rules']['end_condition']))

    def string_to_bool(self, bool_as_string):
        if bool_as_string == "True":
            return True
        if bool_as_string == "False":
            return False
        raise ValueError("Trying to parse " + str(bool_as_string) + " as bool.")
