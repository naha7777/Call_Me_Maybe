from src.state_machine import state_machine
from llm_sdk import Small_LLM_Model

def create_states(prompt) -> list:
    print(prompt)

    return (["start", "quotation_marks", "prompt", "quotation_marks",
            "two_points", "space", "quotation_marks", "string",
            "quotation_marks", "comma", "quotation_marks",
            "name", "quotation_marks", "two_points", "space",
            "quotation_marks", "function", "quotation_marks", "comma",
            "quotation_marks", "parameters", "quotation_marks", "two_points",
             "param", "end", "comma"])


def generation(prompt) -> None:
    model = Small_LLM_Model()
    encode = model.encode(prompt)
    states = create_states(prompt)
    ids = []
    decode = ""
    for state in states:
        valid_tokens = state_machine(state, prompt, model)
        get_logits = model.get_logits_from_input_ids(encode[0].tolist())
        # print(valid_tokens)
        scores = {token_id: get_logits[token_id] for token_id in valid_tokens}
        # print(scores)
        if state == "string":
            for token in valid_tokens:
                ids.append(token)
        else:
            best_token_id = max(scores, key=lambda t: scores[t])
            ids.append(best_token_id)
        # if state == "function":
            # function_name = model.decode()
        # print(encode[0].tolist())
        # best_token_id = get_logits.index(max(get_logits))
        # decode = model.decode(best_token_id)
        # print(decode)

    decode += model.decode(ids)
    print(decode)




# si c'est le dernier prompt il faut pas mettre la comma de fin
# param ca depend du nombre de parametres puisquon ecrit les characters
# un par un

# good jusqu'a function
