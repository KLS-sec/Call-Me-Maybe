import ai_workstation
import sys
import parsing


def main() -> None:
    try:

        # Dataset with every info in it
        dataset = parsing.create_dataset()

        # Get the list of function names in order
        dataset.func_answers.clear()
        dataset.func_answers = ['fn_add_numbers',
                                'fn_add_numbers',
                                'fn_greet',
                                'fn_greet',
                                'fn_reverse_string',
                                'fn_reverse_string',
                                'fn_get_square_root',
                                'fn_get_square_root',
                                'fn_substitute_string_with_regex',
                                'fn_substitute_string_with_regex',
                                'fn_substitute_string_with_regex',]
        """dataset.func_answers = ai_workstation.func_name_list(dataset)
        print("\nFinal result:")  # (@)
        for a in dataset.func_answers:  # (@)
            print(a)"""

        ai_workstation.arg_finder(dataset)

    except Exception as err:
        print("Error detected.", err)
        sys.exit()


if __name__ == "__main__":
    main()
