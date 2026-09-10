import re
from . import parsing
from typing import Any


def organiser(dataset: parsing.DataSet) -> list[list[str]]:
    """Clean the parameters list and make it useable.

    Cut and clean the list of parameters given by the AI.
    Fuse it with elements from the function JSON file.
    """
    triage: list[list[str]] = list()
    param_list: list[list[str]] = list()
    buffer: list[str] = list()
    # **** data loss
    for clean in range(len(dataset.prompt_answers)):
        dataset.prompt_answers[clean] = dataset.prompt_answers[clean].strip()
        triage.append(re.split(r": |, ", dataset.prompt_answers[clean]))
        for x in range(len(triage[-1])):
            triage[-1][x] = triage[-1][x].strip(" '\"{}")
    # **** error trigger
    for x in range(len(triage)):
        copy = triage[x]
        while len(copy) > 0:
            buffer.append(copy.pop())
            if len(copy) > 0:
                copy.pop()
        param_list.append(buffer.copy())
        buffer.clear()
    for x in range(len(param_list)):
        for y in range(len(param_list[x])):
            if param_list[x][y] == ("a|e|i|o|u"):
                param_list[x][y] = ("a|e|i|o|u|y|A|E|I|O|U|Y")
        param_list[x].reverse()

    return param_list


def param_formating(param_list: list[str],
                    dataset: parsing.DataSet, x: int) -> str:
    """Reorganise and fuse the argument list in the corect form."""
    param_dict: dict[str, Any] = dict()

    for a in dataset.function_json:
        if a["name"] == dataset.func_answers[x]:
            param_dict = a["parameters"]
            break

    keys: list[str] = list()
    keys_buffer = param_dict.keys()
    for c in keys_buffer:
        keys.append(c)
    clean: list[Any] = list()
    a_max = len(param_dict)
    b_max = len(keys)
    long = a_max
    if b_max < a_max:
        long = b_max
    for b in range(long):  # len(param_dict)
        buffer = keys[b]
        if param_dict[buffer]["type"] == "number":
            clean.append(keys[b])
            try:
                clean.append(float(param_list[b]))
            except Exception:
                clean.append(float(0.00))
            continue
        if param_dict[buffer]["type"] == "integer":
            clean.append(keys[b])
            try:
                clean.append(int(param_list[b]))
            except Exception:
                clean.append(int(0))
            continue
        clean.append(keys[b])
        clean.append(param_list[b])
    returner: str = "{"
    d = 0
    while d < len(clean):
        returner += f"\"{clean[d]}\": "
        if type(clean[d + 1]) is float or type(clean[d + 1]) is int:
            returner += f"{clean[d + 1]}, "
        else:
            returner += f"\"{clean[d + 1]}\", "
        d += 2
    returner = returner[:-2]
    returner += "}"
    return (returner)


def outputter(dataset: parsing.DataSet) -> str:
    """Take, organise, order then return the clean JSON in an str."""
    param_list: list[list[str]] = organiser(dataset)

    final: str = "[\n"
    for x in range(len(dataset.func_answers)):
        param_final: str = param_formating(param_list[x], dataset, x)
        final += ("    {\n"
                  f"        \"prompt\": \"{dataset.prompt_list[x]}\",\n"
                  f"        \"name\": \"{dataset.func_answers[x]}\",\n"
                  f"        \"parameters\": {param_final}\n"
                  "    },\n")

    final = final[:-2]
    final += "\n]"
    return (final)
