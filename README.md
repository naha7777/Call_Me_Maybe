- dossier src
- fichiers pyproject.toml et uv.lock
- dossier llm_sdk (copie du package)
- dossier data/input/ avec les fichiers tests
- README

- ne pas laisser le dossier output, il sera genere pendant l'evaluation

LLM = machine qui a lu tout internet et capable de deviner la fin des phrases : "le ciel est ..." le modele devine "bleu"
=> fait des statistiques

Token = morceaux d'un texte car le modele ne lit pas lettre par lettre et mot par mot : "hello world" = ["hello", "world"]
Chaque token a un numero = ID car le modele ne manipule que des nombres
= TOKENISATION "hello" = 9906

Generation de texte du modele : a chaque etape le modele regarde tous les tokens recus et produit un score pour chaque token possible du vocabulaire (score = logits)
Token "bleu" -> score de 8.5 donc tres probable
Token "rouge" -> score de 3.2 donc moins probable
Token "chien" -> score de 0.1 donc peu probable
On choisit le token avec le score le plus eleve, on l'ajoute au texte, et on recommence

JSON = format tes strict = PROBLEME si on laise le modele ecrire librement il va ecrire n'importe quoi.
Qwen 0.6B est un petit modele reussissant a produire du JSON seulement 30% du temps.

Donc -> CONSTRAINED DECODING = au lieu de laisser le modele choisir librement il faut bloquer les mauvais tokens avant qu'il choisisse. POur ca on met le score des tokens invalides a -infini pour qu'il ne soit JAMAIS choisi.
Exemple : le modele vient d'ecrire "{" donc les seuls tokens valides maintenant sont les noms des cles JSON possibles : name, parameters..., il faut bloquer tout le reste.

Tensor = tableau des nombres = format que les biblis d'IA utilisent.
[9906, 1913, 374] <- tensor 1D (une liste) / [[1,2],[3,4]] <- tensor 2D (une grille)
get_logits_from_input_ids = on donne une liste de nombre (IDs des tokens) et on recupere une liste de scores (un score par token du vocabulaire)

SDK = boite a outil : au lieu de comprendre le modele en interne, on nous donne 4 fonctions :
- encode("hello") -> [9906] == (text -> IDs)
- get_logits_from_input_ids([9906, 1935, 374]) -> [scores pour chaque token]
- get_path_to_vocabulary_json() -> "vocab.json"
- decode([9906]) -> "hello" == (IDs -> text)
Le vocabulaire JSON c'est un dictionnaire qui dit "le token numero 9906 correspond au texte "hello"". On en a besoin pour savoir quels tokens correspondent a {"n a m e"} etc et decider lesquels sont valides a chaque etape

Function calling = capacite de transformer une phrase en appel de fonction structure.
entree : "What is the sum of 2 and 3 ?"
sortie : {
	"name": "fn_add_number",
	"parameter": {"a": 2.0, "b": 3.0}
}
Le modele doit comprendre ce que l'utilisateur veut, choisir la bonne fonction parmi celles dispos et extraire les bons arguments. Il ne faut pas renvoyer la reponse mais comment la calculer.

1- lire les fonctions dispos (function_definitions.json)
2- lire les prompts (function_calling_tests.json)
3- pour chaque prompt : encoder, demander au modele le score du prochain token, bloquer les tokens invalides, choisir le meilleur token, repeter jusqu'au JSON complet.
4- ecrire dans un JSON

== Parsing progressif : suivre ou on en est dans la structure JSON et decider ce qui est OK ou non.


machine d'etat

installer llm et comprendre comment il communique notamment encode et decode
savoir les tokens des symboles importants


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

### AI usage

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
