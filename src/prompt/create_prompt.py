from src.prompt.function_prompt import function_prompt


def create_prompt(function_calling: list[dict],
                  functions_definitions: list[dict]) -> list[str]:
    fn_p = function_prompt(functions_definitions)
    prompts = []
    for prompt in function_calling:
        user_prompt = ""
        user_prompt += f"{fn_p}\n"
        user_prompt += f"Input: '{prompt['prompt']}'\nThe function to call is:"
        prompts.append(user_prompt)
    return (prompts)

# appelle la function prompt qui renvoie une grosse string
# dans cette grosse string on a chaque nom de fonction : sa description et
# ses parametres
# ensuite on appelle la user prompt
# la user prompt renvoie une list de prompt
# pour chaque prompt, on ecrit genre Input: prompt, The function to call is

# ici on renvoie une liste avec a chaque fois les fonctions possibles et en
# dessous le prompt de l'user et la phrase que doit completer le LLM
