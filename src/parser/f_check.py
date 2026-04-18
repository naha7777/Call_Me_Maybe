from typing import Any


def check_name(r: dict[Any, Any]) -> None:
    """Validate the function name field"""
    get_name = r.get("name")
    if not isinstance(get_name, str):
        raise ValueError(f"Invalid function name '{r.get('name')}',"
                         " put a string")
    if not get_name.startswith("fn_"):
        raise ValueError("Invalid function name, function name must "
                         "start with 'fn_'")
    if get_name == "fn_":
        raise ValueError("Invalid function name, 'fn_' is not a function"
                         " name, please put a clear function name after "
                         "'fn_'")


def check_description(r: dict[Any, Any]) -> None:
    """Validate the function description field"""
    get_description = r.get("description")
    if not isinstance(get_description, str):
        raise ValueError("Invalid function description"
                         f"'{r.get('description')}', put a string")
    if not get_description or not get_description.strip(" "):
        raise ValueError(f"Invalid description '{r.get('description')}',"
                         " write a clear description of the function")
    if len(get_description) < 20:
        raise ValueError("Invalid description, this description is too "
                         "short to be clear")


def check_parameters(r: dict[Any, Any], valid_types: set[str]) -> None:
    """Validate the parameters field and their types"""
    param = r.get("parameters")
    if not isinstance(param, dict):
        raise ValueError(f"Invalid parameters '{param}', put a dict")
    if len(param) < 1:
        raise ValueError("Missing parameters")
    for k, v in param.items():
        if not isinstance(k, str):
            raise ValueError(f"Invalid variable name '{k}', put a string")
        if not isinstance(v, dict):
            raise ValueError(f"Invalid variable type '{k}', put a dict")
        for key, value in v.items():
            if key != "type":
                raise ValueError(f"Invalid key '{key}', put 'type'")
            if value not in valid_types:
                raise ValueError(f"Invalid type: '{value}'")


def check_returns(r: dict[Any, Any], valid_types: set[str]) -> None:
    """Validate the returns field and its type"""
    re = r.get('returns')
    if not isinstance(re, dict):
        raise ValueError(f"Invalid 'returns' value '{re}', put a dict")
    if len(re) < 1:
        raise ValueError("Missing return type")
    if len(list(re.keys())) > 1:
        raise ValueError("Too much keys for 'returns', put only one")
    for ke, va in re.items():
        if ke != "type":
            raise ValueError(f"Invalid key '{ke}', put 'type'")
        if va not in valid_types:
            raise ValueError(f"Invalid type: '{va}'")


def check_doubles(file: str, readding: list[dict[Any, Any]]) -> None:
    """Check for duplicate keys in the JSON file"""
    with open(file, "r") as f:
        readed = f.read()

    count_name = 0
    count_des = 0
    count_param = 0
    count_re = 0
    lines = readed.split("\n")
    for line in lines:
        if '"name"' in line:
            if '"name": "' in line:
                count_name += 1
            else:
                pass
        if '"description"' in line:
            count_des += 1
        if '"parameters"' in line:
            count_param += 1
        if '"returns"' in line:
            count_re += 1
    count_list = [count_name, count_des, count_param, count_re]
    for count in count_list:
        if count != len(readding):
            raise ValueError("Duplicate keys")
