import llm_sdk
import parsing


def main() -> None:
    model = llm_sdk.Small_LLM_Model()

    input_dict = parsing.get_test_prompts()
    function_dict = parsing.get_func_descr()
    func_names = parsing.get_func_names(function_dict)
    none_dict = {
                "name": "None",
                "description": "To use if no other function matches the request.",
                }
    func_names.append("None")
    function_dict.append(none_dict)
    print(input_dict[2])
    print("\n", func_names)
    print(function_dict)

    word_buffer: list[int] = list()
    answers: list[list[int]] = list()
    #######################################################
    # Main core
    for a in range(3):  # len(input_dict)
        # HERE **** !!!! rework liste des fonctions pour la rendre plus digeste
        msg_area: str = ("You are a function selector."
                         "Give me the adapted function in this list or 'none' if there isn't any."
                         "Function list:"
                         f"{function_dict}."
                         "Task to solve:"
                         f"{input_dict[a]}.")
        msg_area.append("<think> </think> Answer: ")
        result: list[int] = model.encode(msg_area)[0].tolist()

        for x in range(3):
            # loggit: list[float] => c est une liste des float, leurs POSITION decide quel token est concerne
            loggit_list: list[float] = model.get_logits_from_input_ids(result)

            z = 0
            test_max_loggit_list = max(loggit_list)
            while loggit_list[z] != test_max_loggit_list:
                z += 1

            # If the tokken cannot be found in the list of functions set it to -inf
            for g in range(len(loggit_list)):
                if all(model.decode(g) not in tokken for tokken in func_names):
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


if __name__ == "__main__":
    main()

"""
for _ in range(self.max_tokens):
    logits = self.model.get_logits_from_input_ids(context)
    slef.validate_steps(prompt, context, generated)

        for i in range(len(logits)):
        if i not in self.authorized and len(self.authorized) != 0:
            logits[i] = float('-inf')
"""
