import json

class JsonEvaluator:
    def __init__(self, functions, json_path):
        self.function_dict = {}
        for function in functions:
            self.function_dict[function.__name__] = function
        self.variable_dictionary = {}
        self.import_variables(json_path)

    def import_variables(self, json_path):
        with open(json_path, 'r') as f:
            json_dict = json.load(f)
            for var_name in json_dict['variables']:
                self.variable_dictionary[var_name] = json_dict['variables'][var_name]
        return self.variable_dictionary

    def get_variable_value(self, var_name):
        if var_name not in self.variable_dictionary:
            raise AttributeError("Variable "+var_name+" reference without import from json")
        return self.variable_dictionary[var_name]

    def find_end_parenthesis(self, string, parenthesis_ind):
        open_counter = 0
        for i in range(parenthesis_ind, len(string)):
            if string[i] == '(':
                open_counter += 1
            if string[i] == ')':
                open_counter -= 1
            if open_counter == 0:
                return i
        raise AttributeError("Could not find closing parenthesis in string: "+string)


    def find_start_of_function_name(self, string, parenthesis_ind):
        for i in range(parenthesis_ind, -1, -1):
            if string[i] in [' ', ',', '(', '<', '>', '=']:
                return i + 1
        return 0


    def contains_unparsed_functions(self, string):
        for c in string:
            if c in ['(']:
                return True
        return False


    def contains_arithmetic_or_logic_operators(self, string):
        for sub in ['<', '>', '=', 'and', 'or']:
            if sub in string:
                return True
        return False


    def find_end_of_variable_name(self, string, start_ind):
        for i in range(start_ind, len(string)):
            if string[i] in ['<', '>', '=', ' ', ',', ')']:
                return i
        return len(string)


    def replace_variables_with_values(self, string):
        while '&' in string:
            amper_ind = string.find('&')
            end_ind = self.find_end_of_variable_name(string, string.find('&'))
            var_name = string[amper_ind + 1:end_ind]
            if var_name not in self.variable_dictionary:
                raise AttributeError("Variable not defined: "+var_name)
            string = string.replace('&' + var_name, str(self.variable_dictionary[var_name]))
        return string


    def evaluate_from_string(self, string):
        string = self.replace_variables_with_values(string)

        # Find instances of functions
        parenthesis_ind = 1
        while parenthesis_ind != -1:
            # Find start of argument list
            parenthesis_ind = string.find('(')
            if parenthesis_ind != -1:
                # Function instance found.
                # Find end of argument list
                end_parenthesis_ind = self.find_end_parenthesis(string, parenthesis_ind)
                # Check has nested functions as arguments
                if self.contains_unparsed_functions(string[parenthesis_ind + 1:end_parenthesis_ind]):
                    # Evaluate arguments inside that function
                    not_substituted = string[parenthesis_ind + 1: end_parenthesis_ind]
                    substituted = self.evaluate_from_string(string[parenthesis_ind + 1:end_parenthesis_ind])
                    string = string.replace(not_substituted, substituted)
                # At this point there are no functions in the string (except base function).
                # There might be commas and logic/arithmetic operators.
                # Evaluate arithmetic and logic operators
                elif self.contains_arithmetic_or_logic_operators(string[parenthesis_ind + 1:end_parenthesis_ind]):
                    not_substituted_args = string[parenthesis_ind + 1: end_parenthesis_ind].split(',')
                    for arg in not_substituted_args:
                        if self.contains_arithmetic_or_logic_operators(arg):
                            string = string.replace(arg, str(eval(arg)))
                # Function has no arguments or all arguments are parsed.
                else:
                    # Evaluate entire function
                    name_start_ind = self.find_start_of_function_name(string, parenthesis_ind - 1)
                    not_substituted = string[name_start_ind: end_parenthesis_ind + 1]

                    # Import function from dictionary
                    name = string[name_start_ind:parenthesis_ind]
                    if name not in self.function_dict:
                        raise AttributeError("Function not found: "+name)
                    function = self.function_dict[name]
                    # Get arguments
                    args = string[parenthesis_ind+1:end_parenthesis_ind].split(',')
                    # If any arguments present then execute the function with them
                    if not (len(args) == 1 and args[0] == ''):
                        substituted = function(*args)
                        string = string.replace(not_substituted, str(substituted))
                    else:
                        substituted = function()
                        string = string.replace(not_substituted, str(substituted))
        # If baseline string after evaluation contains arithmetic or logic then evaluate it.
        if ',' not in string:  # Check if baseline
            if self.contains_arithmetic_or_logic_operators(string):
                string = str(eval(string))
        return string

