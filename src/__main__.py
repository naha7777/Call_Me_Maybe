from src.args import parse_args
from llm_sdk import Small_LLM_Model  # doit fonctionner

def main() -> None:
    try:
        args = parse_args()

    except (ValueError, PermissionError, FileNotFoundError, KeyboardInterrupt,
            KeyError, Exception) as e:
        print(f"ERROR: {e}")
        # import traceback
        # traceback.print_exc()
        exit(1)

    print()
    print(args.input)
    print(args.output)
    print(args.functions_definition)


if __name__ == "__main__":
    main()
