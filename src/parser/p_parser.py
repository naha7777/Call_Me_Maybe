import json


def read_file(file: str) -> list[dict[str: str]]:
    with open(file, "r") as f:
        return json.load(f)


def p_parser(file: str) -> None:
    readding = read_file(file)
    for line in readding:
        if "prompt" not in line:
            raise ValueError("'prompt' is missing")
        for k, v in line.items():
            if not isinstance(v, str):
                raise ValueError("prompt value must be a string")
