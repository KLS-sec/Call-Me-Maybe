import ai_workstation
import outputter
import sys
import parsing


def main() -> None:
    # try:  # (+)
        # Dataset with every info in it
        dataset = parsing.create_dataset()
        dataset.func_answers.clear()

        ######################################################################
        # (#) test area
        """x = dataset.function_json[0]["parameters"]
        print(len(x))
        exit()"""
        ######################################################################
        """dataset.func_answers = ['fn_add_numbers',  # (#)
                                'fn_add_numbers',
                                'fn_greet',
                                'fn_greet',
                                'fn_reverse_string',
                                'fn_reverse_string',
                                'fn_get_square_root',
                                'fn_get_square_root',
                                'fn_substitute_string_with_regex',
                                'fn_substitute_string_with_regex',
                                'fn_substitute_string_with_regex',]"""
        # Get the list of function names in order
        dataset.func_answers = ai_workstation.func_name_list(dataset)  # (+)

        print("\nFinal result:")  # (@)
        for a in dataset.func_answers:  # (@)
            print(a)

        dataset.prompt_answers.clear()
        """dataset.prompt_answers = ["'a': 2, 'b': 3 }",  # (#)
                                  "'a': 265, 'b': 345 }",
                                  "name: 'shrek'}",
                                  '"name": "john" }',
                                  "'s': 'hello' }",
                                  "'s': 'world' }",
                                  "'a': 16 }",
                                  "144}",
                                  '"source_string": "Hello 34 I\'m 233 years old", "regex": "34", "replacement": "34" }',
                                  "'source_string': 'Programming is fun', 'regex': 'a|e|i|o|u', 'replacement': '*'}",
                                  "'source_string': 'The cat sat on the mat with another cat', 'regex': 'cat', 'replacement': 'dog'}",]"""
        # Get the arguments for the JSON
        dataset.prompt_answers = ai_workstation.arg_finder(dataset)  # (+)

        # Organise the text then print it !!!!
        outputter.outputter(dataset)
    # (+)
        """except Exception as err:  # (+)
        print("Edge case error detected.", err)
        sys.exit()"""


if __name__ == "__main__":
    main()
