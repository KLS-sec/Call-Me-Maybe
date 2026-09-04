import json
import argparse
import llm_sdk
from dataclasses import dataclass
from typing import Any


# **** !!!! creer une finction qui le creer et retourne l objet.
# A integrer avec le systeme de flag qui sont demande (necessite de modifier le reste des parsers)
@dataclass
class DataSet:
    """The data to use."""
    model: Any
    prompt_list: list[str]
    function_json: list[dict]
    func_names: list[str]
    args: argparse.Namespace
    func_answers: list[str]


def create_dataset() -> DataSet:
    args: argparse.Namespace = arg_parser()
    model = llm_sdk.Small_LLM_Model()
    prompt_list: list[str] = get_test_prompts(args.input)
    function_json: list[dict] = get_func_json(args.functions_definition)
    func_names: list[str] = get_func_names(function_json)

    obj = DataSet(model=model,
                  prompt_list=prompt_list,
                  function_json=function_json,
                  func_names=func_names,
                  args=args,
                  func_answers=["E"])
    return (obj)


# Use arge with args.function_definition ou les 2 autres
def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--functions_definition",
                        default="data/input/functions_definition.json",
                        help="Input a JSON file with function definitions.")
    parser.add_argument("--input",
                        default="data/input/function_calling_tests.json",
                        help="Input a JSON file with prompts.")
    parser.add_argument("--output",
                        default="data/output/function_calling_results.json",
                        help="Output print path.")
    args = parser.parse_args()
    return args
######################################################################


def get_test_prompts(path: str) -> list[str]:
    """Return the list of prompts."""
    prompt_list: list[str] = list()
    with open(path) as file:
        buffer = json.load(file)
        file.close()
    for x in buffer:
        prompt_list.append(x["prompt"])
    return prompt_list


def get_func_json(path: str) -> list[dict]:
    """Return the JSON of the functions."""
    function_json: list[dict] = list()
    with open(path) as file:
        function_json = json.load(file)
        file.close()
    return function_json


def get_func_names(function_dict) -> list[str]:
    """Return a list with only the functions names."""
    func_names: list[str] = list()
    for a in range(len(function_dict)):
        func_names.append(function_dict[a]["name"])
    return func_names


# Useless? @@@@
def func_dict_cleaner(function_dict) -> list[dict[str]]:
    """Return a list of dict with the functions's names and descriptions."""
    returner: list[dict[str]] = list()
    y: dict[str] = dict()
    for x in function_dict:
        y["name"] = x["name"]
        y["description"] = x["description"]
        returner.append(y.copy())
    return returner
