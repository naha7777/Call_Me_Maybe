def state_machine(state: str, prompt: str, model, vocab_data) -> list:
    if state == "start":
        return ([vocab_data["{"]])
    elif state == "first":
        return ([vocab_data["["]])
    elif state == "final":
        return ([vocab_data["}]"]])
    elif state == "quotation_marks":
        return ([vocab_data['"']])
    elif state == "prompt":
        return ([vocab_data['prompt']])
    elif state == "two_points":
        return ([vocab_data[":"]])
    elif state == "space":
        return ([220])
    elif state == "comma":
        return ([vocab_data[","]])
    elif state == "name":
        return ([vocab_data["name"]])
    elif state == "parameters":
        return ([vocab_data["parameters"]])
    elif state == "function":
        function_lst = []
        functions_names = []
        split_prompt = prompt.split("\n")
        for p in split_prompt:
            pr = p.split(":")
            functions_names.append(pr[0])
        for name in functions_names:
            n = model.encode(name)[0].tolist()
            function_lst.extend(n)
        return (function_lst)
    elif state == "end":
        return ([vocab_data["}"]])
    elif state == "param":
        param_lst = []
        for c in prompt:
            if c in vocab_data:
                param_lst.append(vocab_data[c])
            else:
                param_lst.append([220])
        return param_lst
