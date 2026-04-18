_This project has been created as part of the 42 curriculum by anacharp_

# Call_Me_Maybe

## Description
Call_Me_Maybe is a project implementing a local AI-powered Function Calling system. The primary goal is to force a Large Language Model (Small_LLM_Model) to generate strictly valid JSON outputs by using a state machine-based constrained decoding technique.

The system processes natural language queries (e.g., "Add 5 and 3") and transforms them into structured function calls.

## Instructions
Let's start with environment and package installation :
```bash
make install
```
After that, you only have to run the program with :
```bash
make run
```
If you want to activate the visualizer :
```bash
make visu
```
Or you can do it yourself :
```bash
	uv run python -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calling_results.json
```
For the visualizer too:
```bash
	uv run python -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calling_results.json --visualizer
```
If you want to use 42's moulinette :
```bash
cd moulinette
```
```bash
uv run python -m moulinette grade_student_answers ../data/output/function_calling_results.json --correction_dir data/correction
```

## Algorithm explanation
The core of the project relies on Finite State Machine (FSM) Constrained Decoding. Instead of allowing the LLM to sample any token from its entire vocabulary, I filter allowed tokens at every generation step:
- State Tracking: Based on the current JSON structure (e.g., just opened a bracket), the FSM identifies valid next tokens (e.g., a quotation mark for a key).
- Logit Masking: I retrieve the model's probabilities (logits) for all tokens and set the probability of invalid tokens to −∞, or give a list of valid tokens (excluding automatically every other token)
- Guaranteed Syntax: The model then selects the best token among the remaining valid ones, ensuring 100% JSON syntax validity.

## Design decisions
- Separation of Concerns: Transition logic is isolated in state_machine.py, while generation orchestration resides in generation.py.
- Strict Typing: I use mypy to ensure robust communication between my code and the model SDK.
- Dynamic Argument Extraction: We implemented specific states (param, string, ...) to handle the extraction of varied data types (floats, strings) from the prompts.

## Performance analysis
- Accuracy: Achieved 100% syntactic validity. Semantic accuracy depends on the Small_LLM_Model's ability to map the prompt to the correct function arguments.
- Efficiency: Logit masking introduces negligible CPU overhead but eliminates the need for expensive "retry" loops caused by malformed JSON.
- Speed: it's fast

## Challenges faced
- Parsing : the parsing was a challenge until I discovered 'from json import JSONDecodeError'
- Prompt Engineering Complexity: Finding the right balance in the system prompt was a significant challenge. The model initially struggled to distinguish between general conversation and the specific need to trigger a function. I had to refine the instructions multiple times to ensure the model stayed focused on the input data without adding "hallucinated" context.
- Parameter Mapping Accuracy: My biggest hurdle was ensuring the LLM correctly mapped extracted values to the function's expected parameter names. For instance, ensuring that a value found in the text was correctly assigned to a instead of b in a subtraction, or correctly identifying the name in a greeting prompt. This required a robust state machine logic to bridge the gap between the LLM's raw output and the strict argument requirements of the functions.
- Type Consistency: Mapping LLM outputs (often str or Any) to strict types required by the grader (e.g., float for math functions) required a custom normalization layer in find_values.py.
- SDK Integration: Resolved module resolution issues with Mypy by correctly configuring PYTHONPATH and adding missing type stubs.

## Testing strategy
- Static Analysis: Systematic use of mypy to catch type-related bugs during development.
- Functional Validation: Automated testing via the moulinette tool, comparing generated outputs against ground-truth corrections.
- Visual Inspection: Manual review of 'data/output/function_calling_results.json' to ensure logical consistency.

## Example usage
Input:
```bash
"prompt": "What is the sum of 2 and 3?"
```
Output:
```bash
{
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
        "a": 2.0,
        "b": 3.0
    }
}
```

## Resources
### Documentation
- [Argparse Tutorial](https://www.datacamp.com/tutorial/python-argparse)
- [UV Package Manager Guidev](https://www.datacamp.com/fr/tutorial/python-uv?dc_referrer=https%3A%2F%2Fwww.google.com%2F)
- [States Machines](https://developer.mozilla.org/fr/docs/Glossary/State_machine)
- [JSON Handling in Python](https://www.geeksforgeeks.org/python/json-dump-in-python/)
- [File and directory manipulation](https://dev.to/ericlecodeur/python-manipulation-des-dossiers-et-fichiers-nji)

### AI usage
AI was used for the following tasks :
- explenations about LLM, models, tokens
- makefile debugging
- help with hugging face
- help with space problems
- help with readme
- better understanding certain things in Python
- help create clear docstrings
