from typing import Any


def find_values(prompt: str) -> list[Any]:
    """Extract and type-cast argument values from a natural language prompt"""
    user_prompt = ""
    prompt_values: list[Any] = []
    for line in prompt.split("\n"):
        if "Input" in line:
            user_prompt = line.split(":", 1)[1].strip().strip("'").strip('"')

    if "sum" in user_prompt:
        search_values = user_prompt.split("and")
        value = ""
        for c in search_values[0].strip(" "):
            if c.isdigit():
                value += c
        other_value = search_values[1].strip("?").strip(" ")
        if len(other_value) == 0 or len(value) == 0:
            raise ValueError("Invalid value/s")
        try:
            f_value = float(value)
            s_value = float(other_value)
        except Exception:
            raise ValueError("Wrong value type")
        prompt_values.append(f_value)
        prompt_values.append(s_value)

    elif "Greet" in user_prompt:
        if user_prompt == "Greet" or user_prompt == "Greet ":
            raise ValueError("Mssing value")
        fi_value = ""
        fi_value += user_prompt.split(" ")[1]
        if isinstance(fi_value, int):
            raise ValueError("Wrong value type")
        prompt_values.append(fi_value)

    elif "Reverse" in user_prompt:
        if "'" not in user_prompt:
            raise ValueError("Can't see the value, put single quotes")
        fir_value = user_prompt.split("'")[1].strip("'")
        if isinstance(fir_value, int):
            raise ValueError("Wrong value type")
        prompt_values.append(fir_value)

    elif "root" in user_prompt:
        value = user_prompt.split("of")[1].strip(" ").strip("?")
        try:
            firs_value = float(value)
        except Exception:
            raise ValueError("Wrong value type")
        prompt_values.append(firs_value)

    elif "Replace" in user_prompt:
        if '"' in user_prompt:
            cut = user_prompt.split('"')
        elif "'" in user_prompt:
            cut = user_prompt.split("'")
        else:
            raise ValueError("Can't see the value, put single/double quotes")
        first_value = cut[1]
        third_value = cut[2].strip(" with ")
        value = cut[0].split("all")[1]
        value = value.strip(" ")
        sec_value = value.split(" ")[0].strip(" ")
        if third_value == "asterisks":
            third_value = "*"
        if sec_value == "vowels":
            sec_value = "[aeiouAEIOU]"
        prompt_values.append(first_value)
        prompt_values.append(sec_value)
        prompt_values.append(third_value)

    elif "Substitute" in user_prompt:
        if "'" not in user_prompt:
            raise ValueError("Can't see the value, put single quotes")
        divide = user_prompt.split("'")
        second_value = divide[1].strip("'")
        third_value = divide[3].strip("'")
        first2_value = divide[5].strip("'")
        prompt_values.append(first2_value)
        prompt_values.append(second_value)
        prompt_values.append(third_value)
    else:
        prompt_values.append(user_prompt)
    return prompt_values
