def p_parser(file: str) -> None:
    with open(file, "r") as f:
        readding = f.read()

    if not readding:
        raise ValueError(f"{file} can't be empty")

    lines = readding.split("\n")
    count = 0
    for i, line in enumerate(lines):
        if i != 0 and i != len(lines) - 2 and i != len(lines) - 1:
            count += 1
            if count == 4:
                count = 1
        if i == 0 and line != "[":
            raise ValueError(f"{file} must start with '[', not '{line}'")
        if i == len(lines) - 2 and line != "]":
            raise ValueError(f"{file} must end with ']', not '{line}'")

        if i == 1 and line != "  {" or count == 1 and line != "  {":
            string = '  {'
            raise ValueError(f"'{line}' must be '{string}'")
        if count == 2:
            if not line.startswith('    "prompt":'):
                raise ValueError(f'"{line}" must start with : "    "prompt":"')
            s_p = line.split(":")
            if not s_p[1].startswith(' "') or not s_p[1].endswith('"'):
                raise ValueError(f'"{s_p[1]}" must start with a space and be'
                                 ' surrounded by ""')
        if count == 3:
            if not line.startswith('  },'):
                if i != len(lines) - 3 and i != len(lines) - 2 \
                   and i != len(lines) - 1:
                    end_string = '  },'
                    raise ValueError(f'"{line}" must be "{end_string}"')
            if i == len(lines) - 3 and line != '  }':
                if line != "  }":
                    end_two = '  }'
                    raise ValueError(f'"{line}" must be "{end_two}"')
