from src.state_machine import state_machine
import torch

def create_states() -> list:
    return (["start", "quotation_marks", "prompt", "quotation_marks",
            "two_points", "space", "quotation_marks", "string", "comma",
            "quotation_marks", "name", "quotation_marks", "two_points",
            "space", "quotation_marks", "function", "quotation_marks", "comma",
            "quotation_marks", "parameters", "quotation_marks", "two_points"])
            #  "param", "end", "comma"])


def generation(prompt, model, vocab_data) -> None:
    encode = model.encode(prompt)[0].tolist()
    states = create_states()
    ids = []
    decode = ""
    fixed_states = ["start", "quotation_marks", "prompt", "two_points",
                    "space", "comma", "name", "parameters", "end"]

    for state in states:
        if state in fixed_states:
            valid_tokens = state_machine(state, prompt, model, vocab_data)
            logits = model.get_logits_from_input_ids(encode+ids)
            scores = {token_id: logits[token_id] for token_id in valid_tokens}
            best_token_id = max(scores, key=lambda t: scores[t])
            ids.append(best_token_id)
        elif state == "function":
            no_boucle = []
            functions_names = []
            split_prompt = prompt.split("\n")
            for p in split_prompt:
                pr = p.split(":")
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
        elif state == "string":
            i = 0
            sp_pr = prompt.split("\n")
            for line in sp_pr:
                if line.startswith("Input"):
                    s = line.split(":", 1)[1]
                    s = s.strip().strip("'").strip('"')
            while True:
                logits = model.get_logits_from_input_ids(encode+ids)
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
