-> readme
-> le mettre sur le bon git


_This project has been created as part of the 42 curriculum by anacharp_

# Call_Me_Maybe

## Description
Section that clearly presents the project, including its goal and a
brief overview.

## Instructions
Section containing any relevant information about compilation,
installation, and/or execution.

## Resources
### Documentation
- argparse : https://www.datacamp.com/tutorial/python-argparse
- uv : https://www.datacamp.com/fr/tutorial/python-uv?dc_referrer=https%3A%2F%2Fwww.google.com%2F
- machine d'etat : https://developer.mozilla.org/fr/docs/Glossary/State_machine
- json https://www.geeksforgeeks.org/python/json-dump-in-python/
- https://dev.to/ericlecodeur/python-manipulation-des-dossiers-et-fichiers-nji

### AI usage
- explenations about LLM, models, tokens

## Algorithm explanation
Describe your constrained decoding approach in detail

## Design decisions
Explain key choices in your implementation

## Performance analysis
Discuss accuracy, speed, and reliability of your solution

## Challenges faced
Document difficulties encountered and how you solved them

## Testing strategy
Describe how you validated your implementation

## Example usage
Provide clear examples of running your program

cd moulinette

uv run python -m moulinette grade_student_answers ../data/output/function_calling_results.json --correction_dir data/correction
