import AI_workstation


def main() -> None:
    function_name_list = AI_workstation.func_name_list()
    print("Final result:")
    for a in function_name_list:
        print(a)


if __name__ == "__main__":
    main()
