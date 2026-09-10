from pathlib import Path
from . import ai_workstation
from . import outputter
from . import parsing


def main() -> None:
    try:
        # Dataset with every info in it.
        dataset = parsing.create_dataset()
        dataset.func_answers.clear()

        # Get the list of function names in order.
        dataset.func_answers = ai_workstation.func_name_list(dataset)

        # Get the arguments for the JSON.
        dataset.prompt_answers.clear()
        dataset.prompt_answers = ai_workstation.arg_finder(dataset)

        # Organise the text.
        final: str = outputter.outputter(dataset)

        # Create the JSON result.
        output_path = Path("data/output/function_calls.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w") as file:
            file.write(final)

    except ValueError as err:
        print("Error type:", type(err).__name__)
        print("Edge case error detected.", err)
        exit()


if __name__ == "__main__":
    main()
