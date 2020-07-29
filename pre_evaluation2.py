import json


with open("attrToAnalize.txt", "r") as AttrNamesF:
    gtAttrNames = AttrNamesF.readlines()

gtAttrNames = [line[:-1] for line in gtAttrNames]

# prendo il risultato della terza iterazione
with open('sources_3/big_cluster3.json', 'r') as f:
    distros_dict = json.load(f)
    # sistemo "/" e "//"
    for k, v in distros_dict.items():
        lists = []
        for src, val, attrName in v:
            if attrName in gtAttrNames:
                newLine = f"{src}/{attrName}"
                newLine = newLine.replace("/", "//")
                lists.append(newLine)

        distros_dict[k] = lists
    # scrivo i nuovi json con // al posto di /
    with open(f"sources_3/big_cluster3_refactor.json", "w") as jsFile:
        jsFile.write(json.dumps(distros_dict, indent=4))