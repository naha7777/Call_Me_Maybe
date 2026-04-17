from typing import Any


def find_values(prompt: str) -> list[Any]:
    user_prompt = ""
    prompt_values = []
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
        first_value = float(value)
        second_value = float(other_value)
        prompt_values.append(first_value)
        prompt_values.append(second_value)
    elif "Greet" in user_prompt:
        first_value = ""
        first_value += user_prompt.split(" ")[1]
        prompt_values.append(first_value)
    elif "Reverse" in user_prompt:
        first_value = user_prompt.split("'")[1].strip("'")
        prompt_values.append(first_value)
    elif "root" in user_prompt:
        value = user_prompt.split("of")[1].strip(" ").strip("?")
        first_value = float(value)
        prompt_values.append(first_value)
    elif "Replace" in user_prompt:
        if '"' in user_prompt:
            cut = user_prompt.split('"')
        elif "'" in user_prompt:
            cut = user_prompt.split("'")
        first_value = cut[1]
        second_value = cut[2].strip(" with ")
        value = cut[0].split("all")[1]
        value = value.strip(" ")
        third_value = value.split(" ")[0].strip(" ")
        prompt_values.append(first_value)
        prompt_values.append(second_value)
        prompt_values.append(third_value)
    elif "Substitute" in user_prompt:
        divide = user_prompt.split("'")
        third_value = divide[1].strip("'")
        second_value = divide[3].strip("'")
        first_value = divide[5].strip("'")
        prompt_values.append(first_value)
        prompt_values.append(second_value)
        prompt_values.append(third_value)
    else:
        prompt_values.append(user_prompt)
    return prompt_values
