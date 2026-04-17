import json
from src.parser.f_check import check_description, check_doubles, check_name, \
                               check_parameters, check_returns
from typing import Any


def read_file(file: str) -> Any:
    with open(file, "r") as f:
        return json.load(f)


mandatory_keys = ["name", "description", "parameters", "returns"]
valid_types = {"number", "string", "boolean", "integer", "array", "object",
               "null"}


def f_parser(file: str) -> Any:
    readding = read_file(file)
    for r in readding:
        if mandatory_keys != list(r.keys()):
            raise ValueError(f"Invalid keys '{list(r.keys())}', write it this "
                             f"way: '{mandatory_keys}'")

        check_name(r)
        check_description(r)
        check_parameters(r, valid_types)
        check_returns(r, valid_types)

    check_doubles(file, readding)
    return readding
