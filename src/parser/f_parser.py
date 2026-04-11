import json

def read_file(file: str) -> str:
    with open(file, "r") as f:
        return json.load(f)


mandatory_keys = ["name", "description", "parameters", "returns"]
valid_types = {"number", "string", "boolean", "integer", "array", "object",
               "null"}


def f_parser(file: str) -> None:
    readding = read_file(file)
    for r in readding:
        print(r)
        print( )
        if len(list(r.keys())) != len(set(r.keys())):
            raise ValueError("Duplicate keys")
        if mandatory_keys != list(r.keys()):
            raise ValueError(f"Invalid keys {list(r.keys)}, write it this "\
                             f"way: {mandatory_keys}")

        if not isinstance(r.get("name"), str):
            raise ValueError(f"Invalid function name {r.get('name')}," \
                             " put a string")
        if not isinstance(r.get("description"), str):
            raise ValueError("Invalid function description" \
                             f"{r.get('description')}, put a string")
        param = r.get("parameters")
        if not isinstance(param, dict):
            raise ValueError(f"Invalid parameters {param}, put a dict")

        for k, v in param.items():
            if not isinstance(k, str):
                raise ValueError(f"Invalid variable name {k}, put a string")
            if not isinstance(v, dict):
                raise ValueError(f"Invalid variable type {k}, put a dict")
            for key, value in v.items():
                if key != "type":
                    raise ValueError(f"Invalid key {key}, put 'type'")
                if value not in valid_types:
                    raise ValueError(f"Invalid type: {value}")

        re = r.get('returns')
        if not isinstance(re, dict):
            raise ValueError(f"Invalid 'returns' value {re}, put a dict")
        if len(list(re.keys())) > 1:
            raise ValueError("Too much keys for 'returns', put only one")
        for ke, va in re.items():
            if ke != "type":
                raise ValueError(f"Invalid key {ke}, put 'type'")
            if va not in valid_types:
                raise ValueError(f"Invalid type: {va}")












    # lines = check_extrimities(readding)
    # clear_readding = readding.strip("[\n").rstrip("\n]")
    # is_valid_brackets(clear_readding)
    # paragraphs = divide_into_paragraphs(clear_readding)

    # for p in paragraphs:
    #     i = 1
    #     if not p[1].startswith('    "name": "') \
    #        or not p[2].startswith('    "description": "') \
    #        or not p[3].startswith('    "parameters": {') \
    #        or not p[1].endswith('",') or not p[2].endswith('.",'):
    #         raise ValueError('Please respect this order \n    "name": '\
    #                          '"function_name",\n    "description": '\
    #                          '"function_description.",\n    "parameters": {')
    #     if '    "returns": {' not in p:
    #         raise ValueError('Please put a return type using "returns": { ')
    #     if (3+i) < len(p):
    #         while p[3+i] != '    "returns": {':
    #             if not p[3+i].startswith('      "') \
    #                or not p[3+i].endswith('": {'):
    #                 raise ValueError('Please put valid parameters: \n'\
    #                                 '"      "parameter_name": {"')
    #             i += 1
    #             if not p[3+i].startswith('        "type": "') \
    #             or not p[3+i].endswith('"'):
    #                 raise ValueError('Please put a type for your parameter:\n'\
    #                                 '"        "type": "valid_type"')
    #             if '"string"' not in p[3+i] and '"number"' not in p[3+i] \
    #             and '"boolean"' not in p[3+i]:
    #                 raise ValueError('Please put a valid type: "string", ' \
    #                                 '"number", "boolean", etc')
    #             i += 1
    #             if (p[3+i+2] != '    "returns": {' and p[3+i] != '      },') :
    #                 raise ValueError('Please put "      }," after type line')
    #             if (p[3+i+2] == '    "returns": {' and p[3+i] != '      }'):
    #                 raise ValueError('Please put "      }" after type line')
    #             i += 1
    #             if p[3+i+1] == '    "returns": {':
    #                 i += 4
    #                 break
    #     i += 1
    #     if not p[i].startswith('      "type": "') or not p[i].endswith('"'):
    #         raise ValueError('Please put "      "type": "valid_type""')
    #     if '"string"' not in p[i] and '"number"' not in p[i] \
    #        and '"boolean"' not in p[i]:
    #         raise ValueError('Please put a valid type: "string", ' \
    #                          '"number", "boolean", etc')
    #     if p[i+1] != "    }":
    #         raise ValueError('Please close the returns brackets with "    }"')
    #     if p[i+2] != "  }," and (i+2) != len(lines) - 3:
    #         raise ValueError('Please close the definition function with'\
    #                          '"  },"')

# parameters ouvre toujours une bracket, dans ces brackets ya une ou plusieurs
# variables qui ouvre aussi des brackets avec un type a chaque fois
# ensuite on faire les brackets de parameters
# puis ya returns (en fait 4 obligatoires pas 3) qui ouvre aussi des brackets
# et qui a juste un type

# mandatory keys = name, description, parameters, returns

# mandatory values = type



    # if not readding:
    #     raise ValueError(f"{file} can't be empty")
    # return readding


# def check_extrimities(readding: str) -> list[str]:
#     lines = readding.split("\n")
#     for i, line in enumerate(lines):
#         if i == 0 and line != "[":
#             raise ValueError(f"First line must be '[', not '{line}'")
#         if i == len(lines) - 2 and line != "]":
#             raise ValueError(f"Last line must be ']', and not {line}")
#         if i == 1 and line != "  {":
#             string = '  {'
#             raise ValueError(f"Second line must be '{string}', not '{line}'")
#         if i == len(lines) - 3 and line != "  }":
#             string = '  }'
#             raise ValueError(f"Penultimate line must be '{string}',"\
#                              f" not '{line}'")
#     return lines


# def is_valid_brackets(clear_readding: str):
#     opens = []
#     close = []
#     for c in clear_readding.strip(" "):
#         if c == "{":
#             opens.append(c)
#         if c == "}":
#             close.append(c)
#         else:
#             pass
#     if len(opens) != len(close):
#         if len(close) < len(opens):
#             raise ValueError("Missing one or more '}'")
#         else:
#             raise ValueError("Missing one or more '{'")


# def divide_into_paragraphs(clear_readding: str) -> list:
#     opens = []
#     close = []
#     paragraphs = []
#     y = 0
#     for i, c in enumerate(clear_readding):
#         if c == "{":
#             opens.append(c)
#         if c == "}":
#             close.append(c)
#         if len(opens) == len(close) and len(opens) != 0:
#             paragraphs.append(clear_readding[y+1:i+1])
#             y = i
#     split_paragraphs = []
#     for para in paragraphs:
#         if not para or para == "\n":
#             paragraphs.remove(para)
#         else:
#             split_paragraphs.append(para.split("\n"))

#     last_para = []
#     final_para = []
#     count = 0
#     for i in range(0, len(split_paragraphs)):
#         count += 1
#         if i == len(split_paragraphs) -1:
#             final_para.append(split_paragraphs[i])
#         else:
#             last_para.extend(split_paragraphs[i])
#         if count == 3:
#             count = 0
#             final_para.append(last_para)
#             last_para = []
#     return final_para
