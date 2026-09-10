import json
import argparse
from llm_sdk.llm_sdk import Small_LLM_Model
from typing import Any
from pydantic import BaseModel, ValidationError


class DataSet(BaseModel):
    """Compile the needed datas.

    Correction of pydantic inability to deal with the argparse.
    """
    model_config = {"arbitrary_types_allowed": True}
    model: Any
    prompt_list: list[str]
    function_json: list[Any]
    func_names: list[Any]
    args: argparse.Namespace
    func_answers: list[Any]
    prompt_answers: list[Any]


def create_dataset() -> DataSet:
    """Create the DataSet object."""
    args: argparse.Namespace = arg_parser()
    model = Small_LLM_Model()
    prompt_list: list[str] = get_test_prompts(args.input)
    function_json: list[Any] = get_func_json(args.functions_definition)
    func_names: list[Any] = get_func_names(function_json)
    try:
        obj = DataSet(model=model,
                      prompt_list=prompt_list,
                      function_json=function_json,
                      func_names=func_names,
                      args=args,
                      func_answers=["E"],
                      prompt_answers=["E"])
    except ValidationError as err:
        print("Invalid DataSet: ", err)
        exit()

    return (obj)


def arg_parser() -> argparse.Namespace:
    """Return the args ready to use with default values."""
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


def get_test_prompts(path: str) -> list[str]:
    """Return the list of prompts and secure the JSON formating."""
    prompt_list: list[str] = list()
    try:
        with open(path) as file:
            buffer = json.load(file)
            file.close()
        for x in buffer:
            if type(x["prompt"]) is not str:
                raise ValueError("Invalid prompt, not a string.")
            if not x["prompt"]:
                raise ValueError("Invalid prompt, empty prompt.")
            prompt_list.append(x["prompt"])
    except KeyError as err:
        print("Invalid prompt key, correct key:", err)
        exit()
    except ValueError as err:
        print("JSON formating anomaly:", err)
        exit()
    except Exception as err:
        print("Invalid JSON file:", err)
        exit()
    for y in range(len(prompt_list)):
        if type(prompt_list[y]) is str:
            prompt_list[y] = prompt_list[y].replace('\\', '\\\\')
            prompt_list[y] = prompt_list[y].replace('"', '\\"')
    return prompt_list


def json_security(function_json: list[Any]) -> None:
    """Security against invalid function definition JSON."""
    trashcan: list[Any] = list()
    try:
        for x in function_json:
            trashcan.append(x["name"])
            if not x["name"]:
                raise ValueError("Empty function name.")
            if type(x["name"]) is not str:
                raise ValueError("Function name is not a string.")

        for x in function_json:
            trashcan.append(x["description"])
            if not x["description"]:
                raise ValueError("Empty function description in.", x["name"])
            if type(x["description"]) is not str:
                raise ValueError("Function description is not a string in.",
                                 x["name"])

        for x in function_json:
            trashcan.append(x["parameters"])
            if not x["parameters"]:
                raise ValueError("Empty function parameter in.", x["name"])
            if type(x["parameters"]) is not dict:
                raise ValueError("Function parameter  is not a dict.",
                                 x["name"])
        for x in function_json:
            for y in x["parameters"]:
                if not x["parameters"][y]["type"]:
                    raise ValueError("Empty function parameter type.",
                                     x["name"])
                if type(x["parameters"][y]["type"]) is not str:
                    raise ValueError("Function parameter type is not a dict.",
                                     x["name"])

    except KeyError as err:
        print("Invalid prompt key, correct key:", err)
        exit()
    except ValueError as err:
        print("JSON formating anomaly:", err)
        exit()
    except Exception as err:
        print("Invalid JSON file:", err)
        exit()


def get_func_json(path: str) -> list[Any]:
    """Return the JSON of the functions."""
    function_json: list[Any] = list()
    try:
        with open(path) as file:
            function_json = json.load(file)
            file.close()
    except Exception as err:
        print(err, "Invalid JSON file.")
        exit()
    json_security(function_json)
    return function_json


def get_func_names(function_dict: list[Any]) -> list[str]:
    """Return a list with only the functions names."""
    func_names: list[Any] = list()
    for a in range(len(function_dict)):
        func_names.append(function_dict[a]["name"])
    return func_names
