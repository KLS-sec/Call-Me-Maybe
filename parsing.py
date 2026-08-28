import json


def get_test_prompts() -> list[dict]:
    """Return the JSON of the test prompts."""
    input_dict: list[dict] = list()
    with open("data/input/function_calling_tests.json") as file:
        input_dict = json.load(file)
        file.close()
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
