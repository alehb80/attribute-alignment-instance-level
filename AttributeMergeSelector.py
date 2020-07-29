import CommonUtilities
import json
from fuzzywuzzy import fuzz


###Classe dedicata alla assegnazione di una chiave ai valori trovi simili tra due chiavi
### Un valore puo essere simile a piu valori
### Policy
### Se un valore e' simile a piu valori diversi allora si sommano i valori
### Un valore viene assegnato a k1 o k2 in base al count totale di valori nei rispettivi nomi attributo

class AttributeMergeSelector:

    def __init__(self, local_dict_inv, jsonData, similar_array):
        self.local_dict_inv = local_dict_inv
        self.jsonData = jsonData
        self.similarArray = similar_array

        self.partial_key_dict = {}
        self.partial_key_dict_score = {}
        self.operation = []


    ###Produce un dizionario per ogni chiave che riporta la choesione media dei valori e uno score
    ### Lo score viene calcolato come somma delle similitudini moltiplicato per il numero di valori
    def produceKeyScore(self):
        for key, valuesObject in self.partial_key_dict.items():
            value_list = list(valuesObject.keys())
            if len(value_list) > 1:
                cohesion_score = 0
            else:
                cohesion_score = 100
            match_counter = 0
            for x in range(0, len(value_list)):
                for y in range (x+1, len(value_list)):
                    v1 = value_list[x]
                    v2 = value_list[y]
                    cohesion_score += fuzz.ratio(v1.replace(" ", ""), v2.replace(" ", ""))
                    match_counter += 1

            total_element = sum( [self.partial_key_dict[key][element] for element in self.partial_key_dict[key].keys()])
            self.partial_key_dict_score[key]['key_cohesion'] = cohesion_score / max(1, match_counter)
            self.partial_key_dict_score[key]['key_score'] = cohesion_score * total_element


    def SelectValuesXKey(self):
        #print(self.similarArray)

        ##Produto un sottoinsieme delle chiavi valori sulla base degli accoppiamenti
        for prim_key, keys_sim in self.similarArray:
            if not prim_key in self.partial_key_dict.keys():
                self.partial_key_dict[prim_key] = {}
                self.partial_key_dict_score[prim_key] = {}
            for attrSource, attrVal, *other in self.jsonData[prim_key]:
                if not attrVal in self.partial_key_dict[prim_key].keys():
                    self.partial_key_dict[prim_key][attrVal] = 0
                self.partial_key_dict[prim_key][attrVal] += 1
        
        self.produceKeyScore()
        #print(json.dumps(self.partial_key_dict, indent=4, sort_keys=True))
        #print(json.dumps(self.partial_key_dict_score, indent=4, sort_keys=True))

        self.makeMergeDictionary()
    
    ##Produco il dizionario degli spostamenti da fare
    ##Ogni valore viene confrontato con tutti gli altri delle altre chiavi
    ##Se viene trovata una sim >= 70 allora merge
    ##Viene spostato nell attributo con keyscore maggiore
    ##Se la coesione dei due insieme e' alta allora sinonimi
    ##Se la coesione dei due insiemi e' sbilanciata allora omonimi
    def makeMergeDictionary(self):

        keylist = list(self.partial_key_dict.keys())

        #Per ogni chiave prendo la lista dei valori
        for k1 in self.partial_key_dict.keys():
            valuesObj = self.partial_key_dict[k1]
            value_list = list(valuesObj.keys())

            #Per ogni valore della chiave lo confronto con i valori delle chiavi successive
            for v1 in value_list:

                ###Fisso la chiave di destinazione
                attrKeyDest = k1

                for k2 in self.partial_key_dict.keys():

                    if not k1 == k2:
                        valuesObjy = self.partial_key_dict[k2]
                        value_listy = list(valuesObjy.keys())
                        for v2 in value_listy:
                            rat = fuzz.ratio(v1.replace(" ", ""), v2.replace(" ", ""))
                            if rat >= 80:
                                #print(v1, v2, rat)
                                if self.partial_key_dict_score[attrKeyDest]['key_score'] <= self.partial_key_dict_score[k2]['key_score']:
                                    attrKeyDest = k2
                if not k1 == attrKeyDest:
                    self.operation.append((k1, attrKeyDest, v1, v2, self.partial_key_dict_score[k1]['key_cohesion']))
    
    def getListToMerge(self):
        return self.operation


                            

