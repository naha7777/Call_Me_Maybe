from src.generate.find_values import find_values
from src.generate.state_machine import state_machine
from llm_sdk.__init__ import Small_LLM_Model
import numpy as np
from typing import Any


def state_fix(state: str, prompt: str, model: Small_LLM_Model,
              vocab_data: dict[str, int], logits: list[float],
              ids: list[int], visualizer: bool) -> Any:
    valid_tokens = state_machine(state, prompt, model, vocab_data)
    scores = {token_id: logits[token_id] for token_id in valid_tokens}
    best_token_id = max(scores, key=lambda t: scores[t])
    ids.append(best_token_id)
    decode = model.decode(ids)
    if visualizer:
        print(decode)
    return decode


def state_function(prompt: str, model: Small_LLM_Model, encode: list[str],
                   ids: list[int], state: str,
                   vocab_data: dict[str, int], visualizer: bool) -> None:
    no_boucle: list[int] = []
    functions_names = []
    split_prompt = prompt.split("\n")
    for p in split_prompt:
        pr = p.split(":")
        if pr[0].startswith("You") or pr[0].startswith("Available") \
           or pr[0].startswith("Input") or pr[0].startswith("Output"):
            continue
        if pr[0].startswith("Example") or pr[0].startswith(" ") \
           or not pr[0] or pr[0].startswith("Find"):
            continue
        else:
            functions_names.append(pr[0])
    best_id = None
    while True:
        logits = model.get_logits_from_input_ids(encode+ids)
        valid_tokens = state_machine(state, prompt, model, vocab_data)
        if len(no_boucle) != 0 and best_id is not None:
            valid_tokens.remove(best_id)
        lo = np.array(logits)
        mask = np.full(lo.shape, -np.inf)
        for token_id in valid_tokens:
            mask[token_id] = lo[token_id]
        best_id = np.argmax(mask).item()
        if best_id in no_boucle:
            break
        check_func = model.decode(no_boucle)
        if check_func in functions_names and len(check_func) > 0:
            break
        no_boucle.append(best_id)
        ids.append(best_id)
    if visualizer:
        decode = model.decode(ids)
        print(decode)


def state_string(prompt: str, model: Small_LLM_Model, ids: list[int],
                 vocab_data: dict[str, int], logits: list[float],
                 visualizer: bool) -> None:
    i = 0
    sp_pr = prompt.split("\n")
    for line in sp_pr:
        if line.startswith("Input"):
            s = line.split(":", 1)[1]
            s = s[2:-1]
    while True:
        if i < len(s):
            c = s[i]
            if c == " ":
                valid_tokens = [220]
            elif c == '"':
                valid_tokens = [vocab_data["'"]]
            else:
                valid_tokens = [vocab_data[c]]
            best_id = max({t: logits[t] for t in valid_tokens})
            ids.append(best_id)
            i += 1
        else:
            ids.append(1)
            break
    if visualizer:
        decode = model.decode(ids)
        print(decode)


def state_param(prompt: str, model: Small_LLM_Model, ids: list[int],
                vocab_data: dict[str, int], visualizer: bool) -> None:
    all_name = {}
    prompt_values = find_values(prompt)

    f = model.decode(ids).split('"name": "')[-1].split('"')[0]
    find_parameters = prompt.split("\n")
    for param in find_parameters:
        split_param = param.split(":", 1)
        if f in split_param[0]:
            parameters = split_param[1].split(":")
            function_parameters = parameters[1]

    i = 0
    if "," in function_parameters:
        funct_parameters = function_parameters.split(",")
        for f in funct_parameters:
            s_p = f.split("(")
            all_name[s_p[0].strip(" ")] = prompt_values[i]
            i += 1
    else:
        s_p = function_parameters.split("(")
        all_name[s_p[0].strip(" ")] = prompt_values[0]

    i = 0
    params = ""
    for name, value in all_name.items():
        formatted_value: Any
        if isinstance(value, float):
            formatted_value = value
        elif isinstance(value, str):
            formatted_value = f'"{value}"'
        if i == len(all_name) - 1:
            params += f'"{name}": {formatted_value}'
            break
        else:
            params += f'"{name}": {formatted_value}, '
        i += 1

    params += "}"
    i = 0
    while True:
        if i < len(params):
            c = params[i]
            if c == " ":
                valid_token = 220
            else:
                valid_token = vocab_data[c]
            ids.append(valid_token)
            i += 1
        else:
            break
    if visualizer:
        decode = model.decode(ids)
        print(decode)
