from json import JSONDecodeError
from src.parser.args import parse_args
from src.parser.p_parser import p_parser
from src.parser.f_parser import f_parser
from src.prompt.create_prompt import create_prompt
from src.generate.generation import generation
from llm_sdk import Small_LLM_Model
import json


def main() -> None:

    try:
        args = parse_args()
        function_calling = p_parser(args.input)
        functions_definition = f_parser(args.functions_definition)
        prompt_for_LLM = create_prompt(function_calling, functions_definition)
        model = Small_LLM_Model()
        vocab_path = model.get_path_to_vocab_file()
        with open(vocab_path, "r", encoding="utf-8") as f:
            vocab_data = json.load(f)
        for prompt in prompt_for_LLM:
            generation(prompt, model, vocab_data)
        # generation(prompt_for_LLM[0])

        # string = [{"prompt": "WTF", "name": "fn_add_nb", "parameters": {"a": 2.0, "b": 3.0} },{"prompt": "WTF", "name": "fn_add_nb", "parameters": {"s": "hello"} }]
        # if not exists("data/output"):
        #     os.mkdir("data/output")
        # with open("data/output/function_calling_results.json", "w") as f:
        #     json.dump(string, f, indent=4)

    except (ValueError, PermissionError, FileNotFoundError, KeyboardInterrupt,
            KeyError, JSONDecodeError, Exception) as e:
        print(f"\033[38;2;170;0;0;1mERROR: {e}\033[0m")
        import traceback
        traceback.print_exc()
        exit(1)
    # print()
    # print(args.output)


if __name__ == "__main__":
    main()


# json.dumps() envoit en json bien


# on recupere une liste de prompt a envoyer au LLM un par un
# on envoie les elements de la liste un par un

# on doit construire la machine d'etat

# faire tous les trucs de tokens pour qu'il complete le prompt

# la machine d'etat permet de savoir ou on en est dans le JSON pour savoir
# quels tokens sont interdits: par exemple si on est au debut du JSON le seul
# token autorise c'est celui qui correspond a "["
