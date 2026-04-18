from json import JSONDecodeError
from src.parser.args import parse_args
from src.parser.p_parser import p_parser
from src.parser.f_parser import f_parser
from src.prompt.create_prompt import create_prompt
from src.generate.generation import generation
from llm_sdk.__init__ import Small_LLM_Model
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
        first_activate = False
        i = 0
        count = len(prompt_for_LLM)
        for prompt in prompt_for_LLM:
            i += 1
            first_activate = generation(prompt, model, vocab_data,
                                        first_activate, count, i)

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
