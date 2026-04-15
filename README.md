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

Donc -> CONSTRAINED DECODING = au lieu de laisser le modele choisir librement il faut bloquer les mauvais tokens avant qu'il choisisse. Pour ca on met le score des tokens invalides a -infini pour qu'il ne soit JAMAIS choisi.
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


machine d'etat : pour savoir a chaque instant ou on en est dans la generation du JSON :
ÉTAT: début          → seul token valide : "{"
ÉTAT: clé fonction   → seuls tokens valides : "fn_add_numbers", "fn_greet"...
ÉTAT: séparateur     → seul token valide : ":"
ÉTAT: valeur param a → seuls tokens valides : digits ("2", "3", "4"...)
ÉTAT: fin            → seul token valide : "}"

---------------------------------------------------------------------------------------
FONCTION POUR CREER L'OUTPUT :
met tout dans une string et a la fin with open(data/input/.., "w") as f : json.dump(string, f, indent=4)


on donne la liste de prompts au LLM au debut ?
machine d'etat sur debut : on autorise comme seul token un certain token


avant de faire la machine d'etat on transforme tout le necessaire en token


ETAPE 1 :
tokeniser tout ce qui va etre utile:
- "{"
- les noms des fonctions
- les noms des parametres
- les trucs importants du JSON : ":", ",", "}", '"' etc
- les digits de 0 a 9, ".", "-"

PROBLEME : les noms de fonctions vont surement etres divises en plusieurs tokens
ex: fn_add_numbers = fn, add, numbers : 3 tokens
donc apres avoir choisi fn il faut forcer add et numbers
Mais ils commencent tous par fn
Donc prendre les 3 avec les meilleurs scores ?---------------------------------------

==utiliser get_path_to_vocab_file() -> au lieu de tokeniser chaque string a la main, je charge le vocabulaire entier et je fais la correspondance token_id -> string directement

ETAPE 2: BOUCLE
J'envois les prompts au LLM des le debut, et en fonction de l'etat de ma machine d'etat j'autorise des tokens ou non.
Quand je suis arrivee a la derniere etape de ma machine d'etat, je peux passer au prompt suivant dans ma liste de prompts et repartir du debut dans ma liste d'etat

Reste plus qu'a savoir si ma machine trouve bien la bonne fonction avec ce prompt ou si je vais plus galerer avec le prompt mais au pire je changerai le prompt donc je peux avancer comme ca
-----------------------------------------------------------------------------------



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
