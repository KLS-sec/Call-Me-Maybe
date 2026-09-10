from . import parsing
from typing import Any


def func_name_list(dataset: parsing.DataSet) -> list[list[str]]:
    """Obtain the name of the functions to use in order.

    Feed the prompts to the AI, get the name of the most adapted function to
    solve it and return the list of the name in order to treat the prompt.
    Use a precise prompt and constrained decoding to ensure the fiability.
    """
    model = dataset.model
    prompt_list = dataset.prompt_list
    function_json = dataset.function_json
    func_names = dataset.func_names

    functions_answers: list[list[int]] = list()
    empty_list: list[int] = list()

    # Main loop, treat every prompt.
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

        # Send the prompt a to the ai, add the next tokken at every loop.
        for _ in range(10):
            loggit_list: list[float] = model.get_logits_from_input_ids(result)

            # If the tokken is not in the list of functions set it to -inf.
            for b in range(len(loggit_list)):
                if (all(model.decode(b) not in name for name in func_names)
                   or b >= 151644):
                    loggit_list[b] = float('-inf')

            # Add the tokken withe the highest probability to the list.
            z = 0
            max_loggit_list = max(loggit_list)
            while loggit_list[z] != max_loggit_list:
                z += 1

            result.append(z)
            empty_list.append(z)
            if any(model.decode(empty_list) == name for name in func_names):
                break
            # Kill the loop if EOS is reached.
            if z == 151643:
                break
        functions_answers.append(empty_list.copy())
        empty_list.clear()

    returner: list[list[str]] = list()
    # Convert the tokken into readable text.
    for d in range(len(functions_answers)):
        returner.append(model.decode(functions_answers[d]))
    return (returner)


def arg_finder(dataset: parsing.DataSet) -> list[list[Any]]:
    """Get the parameters for the JSON from the AI.

    Same functionment as func_name_list."""
    model = dataset.model
    functions_answers: list[list[int]] = list()
    empty_list: list[int] = list()

    for a in range(len(dataset.func_answers)):
        for x in dataset.function_json:
            if x["name"] == dataset.func_answers[a]:
                in_use_function = x

        msg_area: str = ("You are an argument finder. "
                         "Given a prompt and the function used to solve it. "
                         "You must understand the function and give the"
                         " parameters needed. "
                         "No verbosity, no repetitions, don't give the source"
                         ", only the arguments. "
                         f"\n- Function:{in_use_function}"
                         f"\n- Prompt:{dataset.prompt_list[a]}"
                         "\n- Argument: {")
        result: list[int] = model.encode(msg_area)[0].tolist()

        for _ in range(40):
            loggit_list: list[float] = model.get_logits_from_input_ids(result)

            # Prioritise EOS if the output is now correct.
            if "}" in model.decode(empty_list):
                for b in range(len(loggit_list)):
                    if b != 151643:
                        loggit_list[b] = float('-inf')

            # Add the highest to the list.
            z = 0
            max_loggit_list = max(loggit_list)
            while loggit_list[z] != max_loggit_list:
                z += 1

            result.append(z)
            empty_list.append(z)

            # Kill the loop if EOS is reached.
            if z == 151643:
                break

        functions_answers.append(empty_list.copy())
        functions_answers[-1] = model.decode(functions_answers[-1])
        empty_list.clear()
    return (functions_answers)
