from json import JSONDecodeError
from src.args import parse_args
from src.parser.p_parser import p_parser
from src.parser.f_parser import f_parser
# from src.functions_parser.f_parser import f_parser
# from llm_sdk import Small_LLM_Model


def main() -> None:
    try:
        args = parse_args()
        p_parser(args.input)
        f_parser(args.functions_definition)

    except (ValueError, PermissionError, FileNotFoundError, KeyboardInterrupt,
            KeyError, JSONDecodeError, Exception) as e:
        print(f"\033[38;2;170;0;0;1mERROR: {e}\033[0m")
        # import traceback
        # traceback.print_exc()
        exit(1)
    # print()
    # print(args.output)


if __name__ == "__main__":
    main()
