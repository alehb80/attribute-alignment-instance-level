import json
import CommonUtilities


with open("attrToAnalizeFull.txt", "r") as AttrNamesF:
    gtAttrNames = AttrNamesF.readlines()

gtAttrNames = set([line[:-1] for line in gtAttrNames])

with open(f"sources_3/big_cluster3_refactor.json", 'r') as f:
    distros_dict = json.load(f)
    newLine = ''
    arrResult = ["left_instance_attribute,right_instance_attribute\n"]
    for key, value in distros_dict.items():
        ###Faccio il prodotto cartesiano e ordino le coppie
        print(f"Working On {key}")
        current_list = set(value)
        slist = sorted(list(current_list.intersection(gtAttrNames)))
        elementCount = len(slist)
        print("List sorted")
        for x in range(0, elementCount):
            
            currente = slist[x]
            ll = [currente +","+s + "\n" for s in slist[x+1:]]
            arrResult += ll
            CommonUtilities.progressBar(x+1, elementCount, f"{x}/{elementCount}")
        print(f"Start Writing: {len(arrResult)} lines of {key}")
        with open(f"sources_3/custom_ground.csv", "a+") as gF:
            gF.writelines(arrResult)
        arrResult = []
        print(f"File Saved")
            
