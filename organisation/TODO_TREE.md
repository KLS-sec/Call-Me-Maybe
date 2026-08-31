# ONIT
Tuto CMM:
https://github.com/SaraFreitas-dev/Call-me-maybe
  V Read the basic page
    Read the .md
      llm*2 , tokenisation, uv * 2


# NEXT
organise the Ai answer

data et balises readthedocs

notebookllm lui donner le git complet (need password)

# TODO
doc:
  function calling:
  https://www.promptingguide.ai/applications/function_calling
  constrained codding:
  https://www.aidancooper.co.uk/constrained-decoding/
  https://zeroentropy.dev/concepts/constrained-decoding/
  Used AI:
  https://huggingface.co/Qwen/Qwen3-0.6B

parseer:
  creer un parser qui rend les json plus lisibles et exploitable pour moi
    creer une liste des fonctions seules?
various:
  Faire en sorte que le systeme de limitation utilise les json comme source de limitation
    quelle fonction? limiter a fouiller dans la liste de fonctions dispo
    quel argument? Fouiller uniquement dans le prompt lui meme
    remplacer les Ġ par " " pour des comparaisons?


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

securite:
  pour input foireux:
    ajouter une boucle lui demandant si une des fonctions corresponds?
    comment securiser les arguments?

# DONE

V  doc:
V  https://qwen.readthedocs.io/en/latest/getting_started/concepts.html#

V  installer la llm et tester dans le vide

V  AI in general
V  https://www.w3schools.com/gen_ai/
V  https://www.w3schools.com/ai/
V  learn how to use JSON
V  https://www.w3schools.com/python/python_json.asp
V  https://www.w3schools.com/python/ref_module_json.asp