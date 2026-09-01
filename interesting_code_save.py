import llm_sdk
import json


def main() -> None:
    model = llm_sdk.Small_LLM_Model()
    with open("data/input/function_calling_tests.json") as file:
        rough_prompt_dict: list[dict[str]] = json.load(file)
        file.close()
    with open("data/input/functions_definition.json") as file:
        function_dict: list[dict[str]] = json.load(file)
        file.close()

    print("INPUT DICT =", type(rough_prompt_dict))
    prompt_list: list[str] = list()
    for x in range(len(rough_prompt_dict)):
        print(type(rough_prompt_dict[x]))
        for y in rough_prompt_dict[x].values():
            prompt_list.append(y)
    # clean useable list
    print(prompt_list)
    print("\n", function_dict)

    empty_list: list[int] = list()
    msg_area: str = ("<|im_start|>system"
                     "You are an AI assistant. You are efficient and not verbose."
                     "Give me the name of the best function to solve the prompt."
                     "Give me the argument needed by the function to solve it."
                     " Here is the list of functions and their descriptions:"
                     f" {function_dict}."
                     "<|im_end|>"
                     "<|im_start|>user "
                     f"{prompt_list[0]}."
                     "<|im_end|>"
                     "<think></think>")
    result: list[int] = model.encode(msg_area)[0].tolist()
    for x in range(25):
        y: list[float] = model.get_logits_from_input_ids(result)
        z = 0

        while y[z] != max(y):
            z += 1
        result.append(z)
        empty_list.append(z)
        if z == 151643:
            break
        if z == 4710 and x != 0:
            result.pop()
            empty_list.pop()
            break
    print("result =", model.decode(empty_list))
    for c in range(len(empty_list)):
        print(model.decode(empty_list[c]), "=", empty_list[c])
    print("codded =", empty_list)


if __name__ == "__main__":
    main()


# L original qui marche assez bien
"""
        msg_area: str = ("You are an AI assistant. You only give short answers, "
                         "no verbosity. Here is a task that need to be solved,"
                         f" but not by you: {input_dict[a]}. You have to give me "
                         "the most adapted function in this list to "
                         f"solve this task: {function_dict}. <think> </think> function:")
"""

# Quasi fonctionnel
"""
        msg_area: str = ("You are a function selector."
                         "Give me the adapted function in this list or 'fn_none' if there isn't any."
                         "Function list:"
                         f"{function_dict}."
                         "Task to solve:"
                         f"{input_dict[a]}."
                         "<think> </think> Answer: fn_")
"""
#proposed by gpt
"""
        msg_area: str = ("<|im_start|>system\nYou are a function-calling assistant. Your task is to select the best function from the provided function definitions and provide the arguments required to call it."
                         " Avaiable functions:")
        for b in function_dict:
            msg_area = msg_area + (f'\n-{b["name"]}: {b["description"]}')
        msg_area += ("\nDo not answer the user's request."
                     "\nDo not explain your choice."
                     "\n<|im_end|>")
        msg_area = msg_area + ("\n<|im_start|>user"
                               f"\n{input_list[a]}"
                               "\n<|im_end|>"
                               "\n<|im_start|>assistant"
                               "\nFunction name: fn_")
"""
