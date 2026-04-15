from src.generate.state_machine import state_machine
import torch


def create_states() -> list:
    return (["first", "start", "quotation_marks", "prompt", "quotation_marks",
             "two_points", "space", "quotation_marks", "string", "comma",
             "quotation_marks", "name", "quotation_marks", "two_points",
             "space", "quotation_marks", "function", "quotation_marks",
             "comma", "quotation_marks", "parameters", "quotation_marks",
             "two_points", "space", "start", "param", "end", "comma", "final"])
# comma a la fin sauf sur le dernier state des states !!!!!!!!!

def state_fix(state, prompt, model, vocab_data, logits, ids) -> None:
    valid_tokens = state_machine(state, prompt, model, vocab_data)
    scores = {token_id: logits[token_id] for token_id in valid_tokens}
    best_token_id = max(scores, key=lambda t: scores[t])
    ids.append(best_token_id)
    decode = model.decode(ids)
    print(decode)


def state_function(prompt, model, encode, ids, state, vocab_data) -> str:
    no_boucle = []
    functions_names = []
    split_prompt = prompt.split("\n")
    final_function = ""
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
        lo = torch.tensor(logits)
        mask = torch.full(lo.shape, float("-inf"))
        for token_id in valid_tokens:
            mask[token_id] = lo[token_id]
        best_id = torch.argmax(mask).item()
        if best_id in no_boucle:
            break
        check_func = model.decode(no_boucle)
        if check_func in functions_names and len(check_func) > 0:
            break
        no_boucle.append(best_id)
        ids.append(best_id)
        decode = model.decode(ids)
        print(decode)
        final_function += decode
    return final_function


def state_string(prompt, model, ids, vocab_data, logits) -> str:
    i = 0
    sp_pr = prompt.split("\n")
    for line in sp_pr:
        if line.startswith("Input"):
            s = line.split(":", 1)[1]
            s = s[2:-1]
    while True:
        logits += model.get_logits_from_input_ids(ids)
        if i < len(s):
            c = s[i]
            if c == " ":
                valid_tokens = [220]
            else:
                valid_tokens = [vocab_data[c]]
            best_id = max({t: logits[t] for t in valid_tokens})
            ids.append(best_id)
            i += 1
        else:
            ids.append(1)
            break
        decode = model.decode(ids)
        print(decode)
    return s


def generation(prompt, model, vocab_data) -> None:
    encode = model.encode(prompt)[0].tolist()
    states = create_states()
    ids = []
    fixed_states = ["start", "quotation_marks", "prompt", "two_points",
                    "space", "comma", "name", "parameters", "end", "first",
                    "final"]

    logits = model.get_logits_from_input_ids(encode+ids)
    for state in states:
        if state in fixed_states:
            state_fix(state, prompt, model, vocab_data, logits, ids)
        if state == "end" and state == states[-1]:
            break
        elif state == "function":
            state_function(prompt, model, encode, ids, state, vocab_data)
        elif state == "string":
            state_string(prompt, model, ids, vocab_data, logits)

        elif state == "param":
            s = ""
            for line in prompt.split("\n"):
                if "Input" in line:
                    s = line.split(":", 1)[1].strip().strip("'").strip('"')
            # f = model.decode(ids).split('"name": "')[-1].split('"')[0]
            instruction = f"Task: Extract parameters names from '{s}'\nFormat: \"a\": value, \"b\": value\nResult: "
            work = model.encode(instruction)[0].tolist()
            param_ids = []

            while True:
                logits = model.get_logits_from_input_ids(work+param_ids)
                last_text = model.decode(param_ids)
                last_char = last_text[-1] if len(param_ids) > 0 else None
                print(f"last text: {last_text}")
                if last_char is None:
                    valid_tokens = [vocab_data['"']]
                elif last_char == '"':
                    if len(last_text) >= 2 and last_text[-2].isalpha():
                        valid = ":"
                    else:
                        valid = "abcdefghijklmnopqrstuvwxyz"
                    valid_tokens = [vocab_data[c] for c in valid if c in vocab_data]
                elif last_char == ':':
                    valid = " "
                    valid_tokens = [220]
                elif last_char == ' ':
                    if len(last_text) >= 2 and last_text[-2] == ",":
                        valid = '"'
                    else:
                        valid = "0123456789"
                    valid_tokens = [vocab_data[c] for c in valid if c in vocab_data]
                elif last_char == '.':
                    valid = "0123456789"
                    valid_tokens = [vocab_data[c] for c in valid if c in vocab_data]
                elif last_char in "0123456789":
                    if last_text[-2] == ".":
                        valid = ","
                    else:
                        valid = "0123456789.}"
                    valid_tokens = [vocab_data[c] for c in valid if c in vocab_data]
                elif last_char == ',':
                    valid = " "
                    valid_tokens = [220]
                else:
                    valid_tokens = state_machine(state, prompt, model, vocab_data)
                device = "cuda" if torch.cuda.is_available() else "cpu"
                lo = torch.tensor(logits).to(device)
                mask = torch.full(lo.shape, float("-inf")).to(device)
                for token_id in valid_tokens:
                    mask[token_id] = lo[token_id]
                best_id = torch.argmax(mask).item()
                if best_id == vocab_data.get('}') or len(param_ids) > 25:
                    break
                param_ids.append(best_id)
            ids.extend(param_ids)
            decode = model.decode(ids)
            print(decode)
