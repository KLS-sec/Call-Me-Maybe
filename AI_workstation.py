import llm_sdk
import parsing


def func_name_list() -> list[list[str]]:
    model = llm_sdk.Small_LLM_Model()
    prompt_list = parsing.get_test_prompts()
    function_dict = parsing.get_func_descr()
    func_names = parsing.get_func_names(function_dict)
    print(func_names)
    for _ in function_dict:
        print(_)

    functions_answers: list[list[int]] = list()
    empty_list: list[int] = list()

    for a in range(len(prompt_list)):
        msg_area: str = ("You are a function selector. You only give function"
                         " names, no verbosity. Here is a task that need to"
                         " be solved, but not by you: "
                         f"{prompt_list[a]}."
                         " You have to give me the function in this list that"
                         " is the most adapted to solve the task: "
                         f"{function_dict}."
                         " Do not invent, stop once you gave the function"
                         " name.<think> </no_think> function: ")
        result: list[int] = model.encode(msg_area)[0].tolist()
        for _ in range(10):
            loggit_list: list[float] = model.get_logits_from_input_ids(result)

            # If the tokken cannot be found in the list of functions set it to -inf
            for b in range(len(loggit_list)):
                if (all(model.decode(b) not in name for name in func_names)
                   or b >= 151644):
                    loggit_list[b] = float('-inf')

            # recupere le plus haut et l ajoute
            z = 0
            max_loggit_list = max(loggit_list)
            while loggit_list[z] != max_loggit_list:
                z += 1

            result.append(z)
            empty_list.append(z)
            print("result =", model.decode(empty_list[-1]), "=", z)
            print(".", model.decode(empty_list), ".", sep="")
            if any(model.decode(empty_list) == name for name in func_names):
                print("name found")
                break
            # Kill the loop if EOS is reached.
            if z == 151643:
                print("EOS REACHED")
                break
        functions_answers.append(empty_list.copy())
        empty_list.clear()

    for c in functions_answers:
        print("result =", model.decode(c))
        print("codded =", c)

    returner: list[list[str]] = list()
    for d in range(len(functions_answers)):
        returner.append(model.decode(functions_answers[d]))

    for e in range(len(returner)):
        if any(returner[e] == name for name in func_names):
            print(prompt_list[e])
            print("ok")
        else:
            raise ValueError("Invalid function detected"
                             f" for {prompt_list[e]}.")

    return (returner)
