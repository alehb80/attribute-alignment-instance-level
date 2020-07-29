import json
import math
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def splitOnComma(row):
    return row.split(",")

def getSourceFromPath(strPath):
    return strPath.split("/")[0]

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z
    
def writeDictToJson(dict_obj, fileName):
    with open(fileName, "w") as src_base_file:
        src_base_file.write(json.dumps(dict_obj, indent=4))
        
def loadJsonFile(file_path, ext=".json"):
    with open(f"{file_path}{ext}", "r") as src_jsnFile:
        jsnData = json.load(src_jsnFile)
    return jsnData
    
def listToStringOrSetList(l1):
    new_l1 = list(set(l1))
    if len(new_l1) == 1:
        return new_l1[0]
    return new_l1
    
#ritorna l'intersezione di due array monodimensionali
def common_elements(list1, list2):
    return [element for element in list1 if element in list2]
    
#ritorna il numero di occorre del valore associato a k1, k2
def scoreBinaryValueMatch(k1, k2, valueInv):
    try:
        valScore1 = 0
        valScore2 = 0

        for keyCount, keyName in valueInv:
            if keyName == k1:
                valScore1 = keyCount
            if keyName == k2:
                valScore2 = keyCount
        return valScore1, valScore2
    except:
        print("Score exeption return 1")
        return 1, 0
        
##Ritorna due array ordinati decrescenti degli indici di l1 e l2 che matchano e i rispettivi valori
def matchValues(l1, l2):
    matching_index1 = set()
    matching_index2 = set()
    for x in range(0, len(l1)):
        for y in range(0,len(l2)):
            #if l1[x][1] == l2[y][1] or fuzz.token_sort_ratio(l1[x][1], l2[y][1]) > 70:
                #print("Match", x, y, l1[x], l2[y])
            if fuzz.token_sort_ratio(l1[x][1], l2[y][1]) > 70:
                matching_index1.add((x, l2[y][1]))
                matching_index2.add((y, l1[x][1]))
               
    matching_index1 = list(matching_index1)
    matching_index1.sort(key=lambda x : x[0], reverse = True)
    matching_index2 = list(matching_index2)
    matching_index2.sort(key=lambda x : x[0], reverse = True)
    return matching_index1, matching_index2
    
    
##Funzione che data una stringa e un array di tuple ritorna il count_della stringa e il count_totale
def get_count_and_total_of(key, l1):
    sub_count = list(filter(lambda x : x[1] == key, l1))[0][0]
    total = sum([element[0] for element in l1])
    return sub_count, total
  
def get_max_in_tuple_list(l1):
    return max([element[0] for element in l1])

##Funzione che ritorna il valor medio da un array numerico
def get_vMed_numeric(l1):
    l1_ord = sorted(l1, reverse = True)
    mid_of_list = math.floor(len(l1_ord)/2)
    return l1_ord[mid_of_list]

##Funzione che ritorna il valor medio da un array di tuple
def get_vMed(l1):
    l1_ord = sorted([element[0] for element in l1], reverse = True)
    mid_of_list = math.floor(len(l1_ord)/2)
    return l1_ord[mid_of_list]
    
#implementing jaccard
def jaccard(a, b):
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

#implementing jaccard digglet
def jaccard2(a, b):
    c = a.intersection(b)
    return float(len(c)) / min((len(a) , len(b)))
    
def getSimilarValues(baseValue, l1):
    l1_sim = []
    for val in l1:
        rat = fuzz.token_sort_ratio(baseValue, val)
        if rat > 70 + (baseValue.isdigit() * 15):
            l1_sim.append(val)
    return l1_sim
    
##Progress Bar
def progressBar(count, total, status=''):
    bar_len = 30
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    if count == total:
        print('[%s] %s%s ...%s                      \r\n' % (bar, percents, '%', status), end='')
    else:
        print('[%s] %s%s ...%s                       \r' % (bar, percents, '%', status), end='')
