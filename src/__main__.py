from src.args import parse_args
from src.prompt_parser.p_parser import p_parser
# from src.functions_parser.f_parser import f_parser
# from llm_sdk import Small_LLM_Model


def main() -> None:
    try:
        args = parse_args()
        p_parser(args.input)

    except (ValueError, PermissionError, FileNotFoundError, KeyboardInterrupt,
            KeyError, Exception) as e:
        print(f"ERROR: {e}")
        # import traceback
        # traceback.print_exc()
        exit(1)

    # f_parser(args.functions_definition)
    # print()
    # print(args.input)
    # print(args.output)
    # print(args.functions_definition)


if __name__ == "__main__":
    main()
