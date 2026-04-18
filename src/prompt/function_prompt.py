from typing import Any


def function_prompt(functions_definitions: list[dict[Any, Any]]) -> str:
    """
    Build a formatted string listing all available functions and their
    parameters
    """
    prompt = ""
    for fn in functions_definitions:
        i = 0
        params = ""
        for k, v in fn['parameters'].items():
            i += 1
            if i == len(fn['parameters'].items()):
                params += f" {k} ({v['type']})"
            else:
                params += f" {k} ({v['type']}),"
        prompt += f"{fn['name']}: {fn['description']} Parameters:{params}\n"
    return (prompt)
