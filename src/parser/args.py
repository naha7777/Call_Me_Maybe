import argparse
from typing import Never


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> Never:
        raise ValueError(message)


def parse_args() -> argparse.Namespace:
    parser = ArgumentParser()

    parser.add_argument("--functions_definition",
                        type=str,
                        required=True,
                        choices=["data/input/functions_definition.json"],
                        help="function_definition_file (.json)")

    parser.add_argument("--input",
                        type=str,
                        required=True,
                        choices=["data/input/function_calling_tests.json"],
                        help="input_file (.json)")

    parser.add_argument("--output",
                        type=str,
                        required=True,
                        choices=["data/output/function_calls.json"],
                        help="output_file (.json)")

    return parser.parse_args()
