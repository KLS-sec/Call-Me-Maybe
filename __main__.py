import llm_sdk
import json
import parsing


def main() -> None:
    model = llm_sdk.Small_LLM_Model()

    input_dict = parsing.get_test_prompts()
    function_dict = parsing.get_func_descr()
    func_names = parsing.get_func_names(function_dict)
    print(input_dict[2])
    print("\n", func_names)

    empty_list: list[int] = list()
    msg_area: str = ("You are an AI assistant. You only give short answers, "
                     "no verbosity. Here is a task that need to be solved,"
                     f" but not by you: {input_dict[2]}. You have to give me "
                     "the function in this list that is the most adapted to "
                     f"solve the task: {function_dict}<think> </no_think> function:")
    result: list[int] = model.encode(msg_area)[0].tolist()

    for x in range(40):
        # loggit: list[float] => c est une liste des float, leurs POSITION decide quel token est concerne
        loggit_list: list[float] = model.get_logits_from_input_ids(result)

        # HERE **** !!!!
        for f in func_names:
            for g in range(len(loggit_list)):
                if model.decode(g) not in f:
                    loggit_list[g] = float('-inf')

        # recupere le plus haut et l ajoute
        z = 0
        max_loggit_list = max(loggit_list)
        while loggit_list[z] != max_loggit_list:
            z += 1
        result.append(z)
        empty_list.append(z)
        print("result =", model.decode(empty_list[-1]), "=", z)

        # Kill the loop when EOS is reached.
        if z == 151643:
            break

    print("result =", model.decode(empty_list))
    print("codded =", empty_list)


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
