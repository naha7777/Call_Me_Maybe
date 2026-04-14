import json


def state_machine(state: str, prompt: str, model) -> list:
    vocab_path = model.get_path_to_vocab_file()
    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab_data = json.load(f)

    if state == "start":
        return ([vocab_data["{"]])
    elif state == "quotation_marks":
        return ([vocab_data['"']])
    elif state == "prompt":
        return ([vocab_data['prompt']])
    elif state == "two_points":
        return ([vocab_data[":"]])
    elif state == "space":
        return ([220])
    elif state == "string":
        char_lst = []
        sp_pr = prompt.split("\n")
        for line in sp_pr:
            if line.startswith("Input"):
                cut_line = line.split(":", 1)[1]
                cut_line = cut_line.strip().strip("'").strip('"')
                for c in cut_line:
                    if c == " ":
                        char_lst.append(220)
                    else:
                        char_lst.append(vocab_data[c])
        return (char_lst)
    elif state == "comma":
        return ([vocab_data[","]])
    elif state == "name":
        return ([vocab_data["name"]])
    elif state == "parameters":
        return ([vocab_data["parameters"]])
    elif state == "function":
        split_prompt = prompt.split("\n")
        functions_names = []
        functions_list = []
        for p in split_prompt:
            pr = p.split(":")
            functions_names.append(pr[0])
        for name in functions_names:
            name_ids = model.encode(name)
            if name_ids[0].tolist() == [2505]:
                break
            functions_list.extend(name_ids[0].tolist())
        return (functions_list)
    elif state == "end":
        return ([vocab_data["}"]])
    # elif state == "param":


