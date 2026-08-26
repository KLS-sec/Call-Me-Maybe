import llm_sdk
import json


def main() -> None:
    model = llm_sdk.Small_LLM_Model()
    with open("data/input/function_calling_tests.json") as file:
        input_dict = json.load(file)
        file.close()
    with open("data/input/functions_definition.json") as file:
        function_dict = json.load(file)
        file.close()

    empty_list: list[int] = list()
    result: list[int] = model.encode(f"You are an AI assistant. Among theses functions: {function_dict}. which one is the most adapted to answer to this question: {input_dict[1]}.")[0].tolist()
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
    print("ok")


if __name__ == "__main__":
    main()
