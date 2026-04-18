from llm_sdk.__init__ import Small_LLM_Model
from src.generate.states import state_fix, state_function
from src.generate.states import state_param, state_string
from src.generate.state_machine import state_machine
from typing import Any
import json
import os
from pathlib import Path


SAVE_GEN = []


def create_states(nb_prompts: int, i: int) -> list[str]:
    if i == nb_prompts:
        return (["first", "start", "quotation_marks", "prompt",
                 "quotation_marks", "two_points", "space", "quotation_marks",
                 "string", "comma", "quotation_marks", "name",
                 "quotation_marks", "two_points", "space", "quotation_marks",
                 "function", "quotation_marks", "comma", "quotation_marks",
                 "parameters", "quotation_marks", "two_points", "space",
                 "start", "param", "end", "final"])
    else:
        return (["first", "start", "quotation_marks", "prompt",
                 "quotation_marks", "two_points", "space", "quotation_marks",
                 "string", "comma", "quotation_marks", "name",
                 "quotation_marks", "two_points", "space", "quotation_marks",
                 "function", "quotation_marks", "comma", "quotation_marks",
                 "parameters", "quotation_marks", "two_points", "space",
                 "start", "param", "end", "comma"])


def json_gen(decode: list[str]) -> None:
    if not Path("data/output").exists():
        os.mkdir("data/output")
    full_string = "".join(decode).strip()
    data = json.loads(full_string)
    with open("data/output/function_calling_results.json", "w") as f:
        json.dump(data, f, indent=4)


def generation(prompt: str, model: Small_LLM_Model, vocab_data: dict[Any, Any],
               first_activate: bool, nb_prompts: int, i: int) -> bool:
    encode = model.encode(prompt)[0].tolist()
    states = create_states(nb_prompts, i)
    ids: list[int] = []
    fixed_states = ["start", "quotation_marks", "prompt", "two_points",
                    "space", "comma", "name", "parameters", "end", "final"]
    this_is_the_end = False

    logits = model.get_logits_from_input_ids(encode+ids)
    for state in states:
        if state == "first" and first_activate is False:
            valid_tokens = state_machine(state, prompt, model, vocab_data)
            scores = {token_id: logits[token_id] for token_id in valid_tokens}
            best_token_id = max(scores, key=lambda t: scores[t])
            ids.append(best_token_id)
            decode = model.decode(ids)
            first_activate = True
        if state in fixed_states:
            decode = state_fix(state, prompt, model, vocab_data, logits, ids)
        if state == "end" and state == states[-1]:
            break
        elif state == "function":
            state_function(prompt, model, encode, ids, state, vocab_data)
        elif state == "string":
            state_string(prompt, model, ids, vocab_data, logits)
        elif state == "param":
            state_param(prompt, model, ids, vocab_data)
    # print(decode)
    SAVE_GEN.append(decode)
    if "final" in states:
        this_is_the_end = True
    if this_is_the_end:
        json_gen(SAVE_GEN)
    return True
