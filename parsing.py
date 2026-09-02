import json


def get_test_prompts() -> list[str]:
    """Return the list of prompts."""
    input_dict: list[str] = list()
    with open("data/input/function_calling_tests.json") as file:
        buffer = json.load(file)
        file.close()
    for x in buffer:
        input_dict.append(x["prompt"])
    return input_dict


def get_func_descr() -> list[dict]:
    """Return the JSON of the functions and their descriptions."""
    input_dict: list[dict] = list()
    with open("data/input/functions_definition.json") as file:
        input_dict = json.load(file)
        file.close()
    return input_dict


def get_func_names(function_dict) -> list[str]:
    """Return a list with only the functions names."""
    func_names: list[str] = list()
    for a in range(len(function_dict)):
        func_names.append(function_dict[a]["name"])
    return func_names


def func_dict_cleaner(function_dict) -> list[dict[str]]:
    """Return a list of dict with the functions's names and descriptions."""
    returner: list[dict[str]] = list()
    y: dict[str] = dict()
    for x in function_dict:
        y["name"] = x["name"]
        y["description"] = x["description"]
        returner.append(y.copy())
    return returner
