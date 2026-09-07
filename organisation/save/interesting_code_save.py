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
    msg_area: str = ("You are an AI assistant. You only give short answers, "
                     "no verbosity. Here is a task that need to be solved,"
                     f" but not by you: {prompt_list[0]}. You have to give me "
                     "the most adapted function in this list to "
                     f"solve this task: {function_dict}. <think> </think> function:")
    result: list[int] = model.encode(msg_area)[0].tolist()
    for x in range(25):
        y: list[float] = model.get_logits_from_input_ids(result)
        z = 0
        y_max = max(y)
        while y[z] != y_max:
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


"""
for _ in range(self.max_tokens):
    logits = self.model.get_logits_from_input_ids(context)
    slef.validate_steps(prompt, context, generated)
        for i in range(len(logits)):
        if i not in self.authorized and len(self.authorized) != 0:
            logits[i] = float('-inf')
"""
"""
for _ in range(self.max_tokens):
    logits = self.model.get_logits_from_input_ids(context)
    slef.validate_steps(prompt, context, generated)
        for i in range(len(logits)):
        if i not in self.authorized and len(self.authorized) != 0:
            logits[i] = float('-inf')
"""

"""import llm_sdk
import parsing


def main() -> None:
    model = llm_sdk.Small_LLM_Model()

    input_list = parsing.get_test_prompts()
    function_dict = parsing.get_func_descr()
    func_names = parsing.get_func_names(function_dict)
    # none_dict = {
                # "name": "fn_none",
             #    "description": "Use this if no function matches the request.",
            #     }
    func_names.append("fn_none")
    # function_dict.insert(0, none_dict)
    func_dict_clean = parsing.func_dict_cleaner(function_dict)
    print(input_list[2])
    print("\n")
    for func in func_names:
        print(func)
    print(function_dict)
    for funcc in function_dict:
        print(funcc)
    for funccc in func_dict_clean:
        print("clean func=", funccc)

    word_buffer: list[int] = list()
    answers: list[list[int]] = list()
    #######################################################
    # Main core
    for a in range(4):  # len(input_list)
        # HERE **** !!!!
        # Rework liste des fonctions pour la rendre plus digeste
        # Rework le prompt
        """
#        msg_area: str = ("You are a function selector. Given a user request, respond with ONLY the function name, nothing else. If no function matches, answer with fn_none."
#                         "\nAvaiable functions:")
"""
        msg_area: str = ("You are a function checker. You have to tell me if any function in the list can solve the user input. Answer ONLY yes or no, nothing else"
                         "\nAvaiable functions:")
        for b in function_dict:
            msg_area = msg_area + (f'\n -{b["name"]}: {b["description"]}')
        msg_area = msg_area + ("\nUser request: "
                               f"{input_list[a]}"
                               "\nyes or no:")
        print(msg_area)
        result: list[int] = model.encode(msg_area)[0].tolist()

        for x in range(1):
            # loggit: list[float] => c est une liste des float, leurs POSITION decide quel token est concerne
            loggit_list: list[float] = model.get_logits_from_input_ids(result)

            z = 0
            test_max_loggit_list = max(loggit_list)
            while loggit_list[z] != test_max_loggit_list:
                z += 1

            # If the tokken cannot be found in the list of functions set it to -inf
            for g in range(len(loggit_list)):
                """"""
                if all(model.decode(g) not in tokken for tokken in func_names):
                    loggit_list[g] = float('-inf')""""""
                if model.decode(g) != "yes" and model.decode(g) != "no":
                    loggit_list[g] = float('-inf')
                if g >= 151644:
                    loggit_list[g] = float('-inf')

            for h in range(151644):
                if loggit_list[h] != float('-inf'):
                    print(h, "=", model.decode(h), "=", loggit_list[h])

            # Recupere le plus probable et l ajoute
            z = 0
            max_loggit_list = max(loggit_list)
            while loggit_list[z] != max_loggit_list:
                z += 1
            result.append(z)
            word_buffer.append(z)
            print("result =", model.decode(word_buffer[-1]), "=", z)

            # Kill the loop when EOS is reached.
            if z == 151645:
                print("EOS REACHED")
                break
        answers.append(word_buffer.copy())
        word_buffer.clear()
    #######################################################

    for d in range(len(answers)):
        print("\n", "result =", model.decode(answers[d]), "=", answers[d])
        print("codded =", answers[d])

"""

"""
for _ in range(self.max_tokens):
    logits = self.model.get_logits_from_input_ids(context)
    slef.validate_steps(prompt, context, generated)

        for i in range(len(logits)):
        if i not in self.authorized and len(self.authorized) != 0:
            logits[i] = float('-inf')
"""
