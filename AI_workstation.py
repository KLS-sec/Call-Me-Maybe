import parsing


def func_name_list(dataset: parsing.DataSet) -> list[list[str]]:
    model = dataset.model
    prompt_list = dataset.prompt_list
    function_json = dataset.function_json
    func_names = dataset.func_names

    functions_answers: list[list[int]] = list()
    empty_list: list[int] = list()

    for a in range(len(prompt_list)):
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
                print("name found")
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
