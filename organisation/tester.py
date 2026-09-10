import json


def tester(path):
    try:
        with open(path) as file:
            buffer = json.load(file)
            file.close()
        print(buffer)
    except Exception as err:
        print(err)
        exit()


def main():
    tester("data/output/function_calls.json")


if __name__ == "__main__":
    main()
