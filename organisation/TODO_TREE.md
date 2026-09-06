# ONIT
0V finir de tester la dict
1V tester le code general et le timer (2:47)
2 parser la reponse
  systeme de decoupage pour ne garder que les arguments
  ############
  import ast

  text = "{'source_string': 'The cat sat on the mat with another cat', 'regex': 'cat', 'replacement': 'dog'}"
  data = ast.literal_eval(text)

  print(data["source_string"])
  print(data["regex"])
  print(data["replacement"])
  ----------------------------------
  json.load(text) si mauvais format ca echoue
  json.dump(text) transforme un texte en format json
  ############
2.1
    -format de la reponse strict en 3 lignes
    -utiliser le nom de la fonction pour recuperer le bon json
    -1 prompt 2 nom fonc 3 arguments
      -recupere les noms des parametres, les compter, remplir le tout avec les arguments recuperes
3 hardcoder le regex et remplacer a|e|i|o|u par aeiouyAEIOUY + V le '}' en EOS


Pour trouver comment prendre les arguments et gerer regex:
  Tuto CMM:
  https://github.com/SaraFreitas-dev/Call-me-maybe
    V Read the basic page
      Read the .md
        llm*2 , tokenisation, uv * 2


# NEXT

notebookllm lui donner le git complet ou le pdf de cours? (need password)

apprendre a utiliser json.load

# TODO
documentation:
  function calling:
  https://www.promptingguide.ai/applications/function_calling
  constrained codding:
  https://www.aidancooper.co.uk/constrained-decoding/
  https://zeroentropy.dev/concepts/constrained-decoding/
  Used AI:
  https://huggingface.co/Qwen/Qwen3-0.6B

parseer:
V  creer un parser qui rend les json plus lisibles et exploitable pour moi
V    creer une liste des fonctions seules?
V  creer une classe qui reprend tout le parsing pour le rendre plus facile a transporter
  creer une verification des input
    verifie le format du json d entree(necessaire?)
  fignoler arg et input

plan:
  boucle 1:
    prompt pour trouver la bonne fonction
      limite ses droit de token a la liste de fonction
  boucle 2:
    je donne le prompt + la fonction choisit et demmande les arguments
      limite ses droits a ce qui est dans le prompt
        me sert du type pour limiter encore plus
      doit trouver un moyen d assurer le bon nombre d arguments
        me servir de la description des fonctions?
  A TESTER
    Une fois le nom recupere lui donner le json correspondant
     a completer et voir ce au il recrache

securite:
  pour input foireux:
    securiser pour les json mal formate  en entree
      pydentic
    comment securiser les arguments? 
      regex hy per constraint

input (page 10):
  Your program must be run using the following command (where src is the folder containing your files):
  Running the program
  uv run python -m src [--functions_definition <function_definition_file>] [--input <input_file>] [--
  output <output_file>]
  By default, the program will read input files from the data/input/
  directory and write output to the data/output/ directory. You
  can optionally specify custom paths using the --input and --output
  arguments. For example:
  uv run python -m src
  --functions_definition data/input/functions_definition.json
  --input data/input/function_calling_tests.json
  --output data/output/function_calls.json
        argument = sys.argv[1]
        print(argument)

various:


# DONE

V  doc:
V    https://qwen.readthedocs.io/en/latest/getting_started/concepts.html#
V  AI in general
V    https://www.w3schools.com/gen_ai/
V    https://www.w3schools.com/ai/
V  learn how to use JSON
V    https://www.w3schools.com/python/python_json.asp
V    https://www.w3schools.com/python/ref_module_json.asp

V  installer la llm et tester dans le vide