import parsing


def func_name_list(dataset: parsing.DataSet) -> list[str]:
    model = dataset.model
    prompt_list = dataset.prompt_list
    function_json = dataset.function_json
    func_names = dataset.func_names

    functions_answers: list[list[int]] = list()
    empty_list: list[int] = list()

    for a in range(len(prompt_list)):  # (#) temp: 3 - def: len(prompt_list)
        msg_area: str = ("You are a function selector. You only give function"
                         " names, no verbosity. Here is a task that need to"
                         " be solved, but not by you: "
                         f"{prompt_list[a]}."
                         " You have to give me the function in this list that"
                         " is the most adapted to solve the task: "
                         f"{function_json}."
                         " Do not invent, stop once you gave the function"
                         " name.<think> </no_think> function: ")
        result: list[int] = model.encode(msg_area)[0].tolist()
        for _ in range(10):
            loggit_list: list[float] = model.get_logits_from_input_ids(result)

            # If the tokken is not in the list of functions set it to -inf.
            for b in range(len(loggit_list)):
                if (all(model.decode(b) not in name for name in func_names)
                   or b >= 151644):
                    loggit_list[b] = float('-inf')

            # Add the highest to the list.
            z = 0
            max_loggit_list = max(loggit_list)
            while loggit_list[z] != max_loggit_list:
                z += 1

            result.append(z)
            empty_list.append(z)
            if any(model.decode(empty_list) == name for name in func_names):
                print("name found")  # (@)
                break
            # Kill the loop if EOS is reached.
            if z == 151643:
                print("EOS REACHED")
                break
        functions_answers.append(empty_list.copy())
        empty_list.clear()

    returner: list[list[str]] = list()
    for d in range(len(functions_answers)):
        returner.append(model.decode(functions_answers[d]))

    for e in range(len(returner)):
        if any(returner[e] == name for name in func_names):
            continue
        else:
            raise ValueError("Invalid function detected"
                             f" for {prompt_list[e]}.")

    return (returner)


def arg_finder(dataset: parsing.DataSet) -> None:  # @@@@ Return something?

    model = dataset.model

    functions_answers: list[list[int]] = list()
    empty_list: list[int] = list()

    for a in range(8, len(dataset.func_answers)):  # (#) temp: 3 - def: len(dataset.func_answers)
        for x in dataset.function_json:
            if x["name"] == dataset.func_answers[a]:
                in_use_function = x

        msg_area: str = ("You are an argument finder. "
                         "Given a prompt and the function used to solve it. "
                         "You must understand, interpret and give the arguments needed. "
                         "No verbosity, no repetitions, don't give the source"
                         ", only the arguments. "
                         f"\n- Function:{in_use_function}"
                         f"\n- Prompt:{dataset.prompt_list[a]}"
                         "\n- Argument: {")
        result: list[int] = model.encode(msg_area)[0].tolist()

        ########################################################## !!!!

        for _ in range(40):
            loggit_list: list[float] = model.get_logits_from_input_ids(result)

            # Add the highest to the list.
            z = 0
            max_loggit_list = max(loggit_list)
            while loggit_list[z] != max_loggit_list:
                z += 1

            result.append(z)
            empty_list.append(z)
            print("result = .", model.decode(empty_list), ".", sep="")
            if any(model.decode(empty_list) == name for name in dataset.func_names):
                print("name found")  # (@)
                break
            # Kill the loop if EOS is reached.
            if z == 151643:
                print("EOS REACHED")
                break

            if "}" in model.decode(empty_list):
                break

        functions_answers.append(empty_list.copy())
        functions_answers[-1] = model.decode(functions_answers[-1])
        functions_answers.append(len(empty_list))
        empty_list.clear()
    print("FINAL RESULT =")
    for res in functions_answers:
        print("------------------\n#", res, "#", sep="")

#This one is almost perfect
"""
        msg_area: str = ("You are an argument finder. "
                         "Given a prompt and the function used to solve it you must give the arguments needed. "
                         "No verbosity, no source, only the arguments. "
                         f"\n-Function:{in_use_function}"
                         f"\n-Prompt:{dataset.prompt_list[a]}"
                         "\n-Argument: {")
"""
"""
def arg_finder(dataset: parsing.DataSet) -> None:  # @@@@ Return something?

    model = dataset.model

    functions_answers: list[list[int]] = list()
    empty_list: list[int] = list()

    for a in range(len(dataset.func_answers)):  # (#) temp: 3 - def: len(dataset.func_answers)
        for x in dataset.function_json:
            if x["name"] == dataset.func_answers[a]:
                in_use_function = x

        msg_area: str = ("You are an argument finder. "
                         "Given a prompt and the function used to solve it you must give the arguments needed. "
                         "No verbosity, only the arguments. "
                         f"\n-Function:{in_use_function}"
                         f"\n-Prompt:{dataset.prompt_list[a]}"
                         "\n-Argument: {")
        result: list[int] = model.encode(msg_area)[0].tolist()

        ########################################################## !!!!

        for _ in range(40):
            loggit_list: list[float] = model.get_logits_from_input_ids(result)

            # Add the highest to the list.
            z = 0
            max_loggit_list = max(loggit_list)
            while loggit_list[z] != max_loggit_list:
                z += 1

            result.append(z)
            empty_list.append(z)
            print("result = .", model.decode(empty_list), ".", sep="")
            if any(model.decode(empty_list) == name for name in dataset.func_names):
                print("name found")  # (@)
                break
            # Kill the loop if EOS is reached.
            if z == 151643:
                print("EOS REACHED")
                break

            if "}" in model.decode(empty_list):
                break

        functions_answers.append(empty_list.copy())
        functions_answers[-1] = model.decode(functions_answers[-1])
        functions_answers.append(len(empty_list))
        empty_list.clear()
    print("FINAL RESULT =")
    for res in functions_answers:
        print("------------------\n#", res, "#", sep="")
"""