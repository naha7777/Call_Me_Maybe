def check_name(r: dict) -> None:
    if not isinstance(r.get("name"), str):
        raise ValueError(f"Invalid function name '{r.get('name')}',"
                         " put a string")
    if not r.get("name").startswith("fn_"):
        raise ValueError("Invalid function name, function name must "
                         "start with 'fn_'")
    if r.get("name") == "fn_":
        raise ValueError("Invalid function name, 'fn_' is not a function"
                         " name, please put a clear function name after "
                         "'fn_'")


def check_description(r: dict) -> None:
    if not isinstance(r.get("description"), str):
        raise ValueError("Invalid function description"
                         f"'{r.get('description')}', put a string")
    if not r.get("description") or not r.get("description").strip(" "):
        raise ValueError(f"Invalid description '{r.get('description')}',"
                         " write a clear description of the function")
    if len(r.get("description")) < 20:
        raise ValueError("Invalid description, this description is too "
                         "short to be clear")


def check_parameters(r: dict, valid_types: set[str]) -> None:
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


def check_returns(r: dict, valid_types: set[str]) -> None:
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


def check_doubles(file: str, readding: list[dict]) -> None:
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
