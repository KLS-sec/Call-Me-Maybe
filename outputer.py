import re  # (#)
from parsing import DataSet


def organiser(dataset: DataSet) -> list[list[str]]:
    triage = list()
    arg_list = list()
    buffer = list()
    print("FINAL RESULT =")  # (@)
    for res in range(len(dataset.prompt_answers)):  # (@)
        print("---------\n#", dataset.prompt_answers[res], "#", sep="")
    print("cleaned result =")
    for clean in range(len(dataset.prompt_answers)):
        dataset.prompt_answers[clean] = dataset.prompt_answers[clean].strip()
        print(dataset.prompt_answers[clean])
        triage.append(re.split(r": |, ", dataset.prompt_answers[clean]))
        for x in range(len(triage[-1])):
            triage[-1][x] = triage[-1][x].strip(" '\"{}")
            print("x =", triage[-1][x])

    for x in range(len(triage)):
        copy = triage[x]
        while len(copy) > 0:
            buffer.append(copy.pop())
            if len(copy) > 0:
                copy.pop()
        arg_list.append(buffer.copy())
        buffer.clear()
    print("proper result =")
    for x in arg_list:
        print(x)

    return arg_list


def outputter(dataset: DataSet) -> None:
    #!!!!##########################
    arg_list = organiser(dataset)
    # call les json pour trouver le nombre d arg et leurs format (a, s, text etc)
    # corrige le a|e|i|o|u
    # fonction qui cree le bon format
    # rajoute tout le bordel dans le paragraphe output
    # ajoute le tout dans un .txt externe
    ###############################
