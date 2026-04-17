from src.prompt.function_prompt import function_prompt
from typing import Any


def create_prompt(function_calling: list[dict[Any, Any]],
                  functions_definitions: list[dict[Any, Any]]) -> list[str]:
    fn_p = function_prompt(functions_definitions)
    prompts = []
    for prompt in function_calling:
        user_prompt = ""
        user_prompt = "You are a helpful assistant that outputs only JSON.\n"
        user_prompt += "Available functions:\n"
        user_prompt += f"{fn_p}\n\n"
        user_prompt += "Example:\n"
        user_prompt += f"Input: '{prompt['prompt']}'\n"
        user_prompt += f'Output: "prompt": {prompt["prompt"]}, "name":' \
                       f'"function_name", "parameters": prompt_values\n\n'
        # user_prompt += "Find the write function for the prompt"
        prompts.append(user_prompt)
    return (prompts)
