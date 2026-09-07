import re  # (#)
from . import parsing


def organiser(dataset: parsing.DataSet) -> list[list[str]]:
    triage: list[list[str]] = list()
    param_list: list[list[str]] = list()
    buffer: list[str] = list()
    print("FINAL RESULT =")  # (@)
    for res in range(len(dataset.prompt_answers)):  # (@)
        print("---------\n#", dataset.prompt_answers[res], "#", sep="")
    print("cleaned result =")  # (@)
    for clean in range(len(dataset.prompt_answers)):
        dataset.prompt_answers[clean] = dataset.prompt_answers[clean].strip()
        # print(dataset.prompt_answers[clean])  # (@)
        triage.append(re.split(r": |, ", dataset.prompt_answers[clean]))
        for x in range(len(triage[-1])):
            triage[-1][x] = triage[-1][x].strip(" '\"{}")
            # print("x =", triage[-1][x])  # (@)

    for x in range(len(triage)):
        copy = triage[x]
        while len(copy) > 0:
            buffer.append(copy.pop())
            if len(copy) > 0:
                copy.pop()
        param_list.append(buffer.copy())
        buffer.clear()
    print("proper result =")
    for x in range(len(param_list)):
        for y in range(len(param_list[x])):
            if param_list[x][y] == ("a|e|i|o|u"):
                param_list[x][y] = ("a|e|i|o|u|y|A|E|I|O|U|Y")
        param_list[x].reverse()  # (@) ou je garde le .pop() ?
        print(param_list[x])

    return param_list


def param_formating(param_list: list[list[str]], dataset: parsing.DataSet, x: int) -> str:
    param_dict: dict = dict()
    print("Marker 01")  # (@)
    print("funcname", dataset.func_answers[x], "x =", x)
    print("param list", param_list)

    for a in dataset.function_json:
        print("a Name", a["name"], dataset.func_answers[x])
        if a["name"] == dataset.func_answers[x]:
            param_dict = a["parameters"]
            break
    print("Marker 02")  # (@)

    keys: list[str] = list()
    keys_buffer = param_dict.keys()
    for c in keys_buffer:
        keys.append(c)
    clean: list[str] = list()
    for b in range(len(param_dict)):
        print("keys =", type(keys))
        buffer = keys[b]
        print(buffer)
        print("HERE", param_dict[buffer])  # (@)
        print("PARAM LIST", param_list)
        if param_dict[buffer]["type"] == "number":
            clean.append(keys[b])
            clean.append(float(param_list[b]))
            continue
        clean.append(keys[b])
        clean.append(param_list[b])
    print("Marker 03")  # (@)
    returner: str = "{"
    d = 0
    while d < len(clean):
        returner += f"\"{clean[d]}\": "
        if type(clean[d + 1]) is float:
            returner += f"{clean[d + 1]}, "
        else:
            returner += f"\"{clean[d + 1]}\", "
        d += 2
    returner = returner[:-2]
    returner += "}"
    print("Marker 04")  # (@)
    return (returner)


def outputter(dataset: parsing.DataSet) -> str:
    # !!!!##########################
    param_list: list[list[str]] = organiser(dataset)
    for x in dataset.function_json:  # (@)
        print(len(x["parameters"]))

    final: str = "[\n"
    for x in range(len(dataset.func_answers)):
        print("Marker 0")  # (@)
        param_final: str = param_formating(param_list[x], dataset, x)
        print("Marker 1")  # (@)
        final += ("    {\n"
                  f"        \"prompt\": \"{dataset.prompt_list[x]}\",\n"
                  f"        \"name\": \"{dataset.func_answers[x]}\",\n"
                  f"        \"parameters\": {param_final}\n"
                  "    },\n")
        print(final)
        print("Marker 2")  # (@)

    final = final[:-2]
    final += "\n]"
    print(final)
    return (final)

# Old
"""
def param_formating(param_list: list[list[str]], dataset: parsing.DataSet, x: int) -> str:
    param_dict: dict = dict()
    for a in dataset.function_json:
        if a["name"] == dataset.func_names[x]:
            param_dict = a["parameters"].copy()
    keys = param_dict.keys()
    clean: list[str] = list()
    for b in range(len(param_dict)):
        clean.append(keys[b], param_list[b])


def outputter(dataset: parsing.DataSet) -> None:
    # !!!!##########################
    param_list: list[list[str]] = organiser(parsing.dataset)
    prompts: list[str] = parsing.dataset.prompt_list
    func_names: list[str] = parsing.dataset.func_answers
    for x in parsing.dataset.function_json:
        print(len(x["parameters"]))
    final: str = "[\n"
    for x in range(len(func_names)):
        param_final = param_formating(param_list, parsing.dataset, x)
        final += ("    {\n"
                  f"        \"prompt\": \"{prompts[x]}\",\n"
                  f"        \"name\": \"{func_names[x]}\"\n"
                  f"        \"parameters\": {param_final}")
"""