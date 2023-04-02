from gamemodes.json_evaluator import JsonEvaluator


def a(x, y):
    return int(x) + int(y)


def b(x):
    return int(x) - 10


def c():
    return 1


def d():
    return 2


def x(b):
    if b == "True":
        return False
    else:
        return True


def y():
    return True


def z(a, b, c):
    return bool(a) and bool(b) and bool(c)


jsonEvaluator = JsonEvaluator([a, b, c, d, x, y, z])

assert jsonEvaluator.evaluate_from_string("a( d(), b(c()) )") == str(-7)
assert jsonEvaluator.evaluate_from_string("z( 1<2, 1==1, x(y())==False )") == "True"
assert jsonEvaluator.evaluate_from_string("x(False) and y()") == "True"

jsonEvaluator.variable_dictionary["VAR"] = 21

assert jsonEvaluator.evaluate_from_string("&VAR") == str(21)
assert jsonEvaluator.evaluate_from_string("b(&VAR)") == str(11)
assert jsonEvaluator.evaluate_from_string("a(&VAR, &VAR)") == str(42)
