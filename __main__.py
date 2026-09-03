import AI_workstation
import sys
import parsing


def main() -> None:
    try:
        dataset = parsing.create_dataset()
        function_name_list = AI_workstation.func_name_list(dataset)
        print("\nFinal result:")
        for a in function_name_list:
            print(a)
    except Exception as err:
        print("Error detected.", err)
        sys.exit()


if __name__ == "__main__":
    main()
