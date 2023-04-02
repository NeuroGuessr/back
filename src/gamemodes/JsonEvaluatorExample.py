from gamemodes.json_evaluator import JsonEvaluator


# 1. Zdefiniuj funkcje

def f(x):
    x = int(x)
    return x**2

# 2. Utwórz evaluator z listą funkcji jako jedynym argumentem

jsonEvaluator = JsonEvaluator([f])

# 3. Aby wykonać użyj jsonEvaluator.evaluate_from_string("string z jsona") (zawsze zwraca string)

print(jsonEvaluator.evaluate_from_string("f(5)"))

# 4. Zmienne może zdefiniować w jsonie albo w jsonEvaluator.variable_dictionary["zmienna"] = wartość
#    ^ Te zmienne wykorzystuje sie w funkcjach z symbolem & na poczatku

jsonEvaluator.variable_dictionary["answer"] = 6
print(jsonEvaluator.evaluate_from_string("&answer"))


# Docelowe wykorzystanie:
# Użytkownik (być może przez UI) definuje zasady gry używając istniejących funkcji jako "klocków" w jsonie.
# Jeśli potrzebne są nowe funkcje pythonowe można po ich napisaniu dodać ich
# nazwy do listy evaluatora, aby ich funkcjonalność byłą dostępna w jsonie.
# W przyszłości dodam wrappery w stylu evaluator.gameEnded() żeby
# zminimalizować wykorzystanie evaluate_from_string

