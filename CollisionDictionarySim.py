import datetime
import os
import sys
import json
import CommonUtilities
from Constats_App import *
import time

class CollisionDictionarySim:
    
    def __init__(self, coll_dict, coll_inv_dict):
        self.__coll_dict = coll_dict
        self.__coll_inv_dict = coll_inv_dict
        self.outFile = COLLISION_DICTIONARY_SIM_DICT
        
        self.__collision_sim_dict = {}
        self.collision_sim_dict = {}
    ###Prende come input una 1) Chiave, 2) Un array di chiavi che hanno in comune il valore corrente,  3) Un array di valori della chiave
    def __getScore(self, k, arr, arrVal):
        lscore = 0
        tscore = 0
        
        for elm in arr:
            if elm[1] == k:
                lscore = elm[0]
        for elm in arrVal:
            tscore += elm[0]
        return float(lscore/(tscore/len(arrVal)))
        
    def Load(self):
        if os.path.exists(self.outFile):
            print(f"{type(self).__name__} CollisionSimDictionary Founded! Loading")
            self.__loadCollisionSimDictionary()
        else:
            self.__makeCollisionSimDictionary()
            self.__printStats()
            
    def __loadCollisionSimDictionary(self):
        self.collision_sim_dict = CommonUtilities.loadJsonFile(self.outFile, ext="")
        print(f"{type(self).__name__} CollisionSimDictionary Loaded!")
        
    def __getAttrRelevance(self, attrName, attrValue):

        #Prendo tutti i nomi attributi correlati a quel valore
        keysMatchingValue = self.__coll_inv_dict[attrValue]['attribute_list']
        
        #Prendo tutti i valori associati al nome attributo
        valuesOfAttribute = self.__coll_dict[attrName]['value_list']
        
        ##Calcolo valore e totale di ogni insieme
        key_count, ktotal_count = CommonUtilities.get_count_and_total_of(attrName, keysMatchingValue)
        val_count, vtotal_count = CommonUtilities.get_count_and_total_of(attrValue, valuesOfAttribute)
        
        ###Per ogni insieme keysMatchingValue, valuesOfAttribute calcolo la media dei punteggi e il valor medio        
        keysMatchingValue_med = ktotal_count / len(keysMatchingValue)
        keysMatchingValue_vmed = CommonUtilities.get_vMed(keysMatchingValue)
        
        valuesOfAttribute_med = vtotal_count / len(valuesOfAttribute)
        valuesOfAttribute_vmed = CommonUtilities.get_vMed(valuesOfAttribute)
        
        ######Calcolo il peso del nomeAttr/valorAttr rispetto all'insieme di appartenenza
        prcAttrVInAttrName = float(key_count/ktotal_count) 
        prcAttrNameInAttrV = float(val_count/vtotal_count) 
        
        ##Per keysMatchingValue, valuesOfAttribute scelgo il min tra media e valor medio
        keysMatchingValue_min = float(min(keysMatchingValue_med, keysMatchingValue_vmed) / ktotal_count)
        valuesOfAttribute_min = float(min(valuesOfAttribute_med, valuesOfAttribute_vmed) / vtotal_count)
        
        if CommonUtilities.get_max_in_tuple_list(keysMatchingValue) == keysMatchingValue_min:
            keysMatchingValue_min *= 0.9
            
        if CommonUtilities.get_max_in_tuple_list(valuesOfAttribute) == valuesOfAttribute_min:
            valuesOfAttribute_min *= 0.9
        
        relevantScore = max( 0, (prcAttrVInAttrName - keysMatchingValue_min) , (prcAttrNameInAttrV - valuesOfAttribute_min) , (prcAttrVInAttrName - keysMatchingValue_min)  +  (prcAttrNameInAttrV - valuesOfAttribute_min) )
        
        # if attrName == "ean13":
            # print(attrName, attrValue)
            # print(key_count, ktotal_count, prcAttrVInAttrName, keysMatchingValue_min, len(keysMatchingValue))
            # print(val_count, vtotal_count, prcAttrNameInAttrV, valuesOfAttribute_min, len(valuesOfAttribute))
            # print(f"Final Score: {relevantScore}")
        
        
        return keysMatchingValue, float(relevantScore) * 100
        
    def __make_dirty_dict_sim(self):
        print(f"[{type(self).__name__}]Running ---> __make_dirty_dict_sim")
        for keyAttribute, valueAttributeList in self.__coll_dict.items():
            self.__collision_sim_dict[keyAttribute] = { 'attr_sim_list' : [], 'attr_sim_score' : []}
            #Per ogni valore associato ad un attributo
            for valueAttributeCount, valueAttribute in valueAttributeList["value_list"]:
            
                keysMatchingValue, keyValueScore = self.__getAttrRelevance(keyAttribute, valueAttribute)
                
                #Calcololo lo score per capire quanto quel valore sia pesante rispetto all attributo
                #keyValueScore = self.__getScore(keyAttribute, keysMatchingValue, valueAttributeList["value_list"])

                #Cutoff per contributi Minimi (Rumore di singoli valori)
                #if keyValueScore > 0.03:
                
                #Per ogni nome attributo di quel valore
                for attrNameCount, attrName in keysMatchingValue:
                    #Se non é ancora associato attrName al keyAttribute corrente
                    if not attrName in self.__collision_sim_dict[keyAttribute]['attr_sim_list']:
                        self.__collision_sim_dict[keyAttribute]['attr_sim_list'].append(attrName)
                        self.__collision_sim_dict[keyAttribute]['attr_sim_score'].append(0)
                    elm_index = self.__collision_sim_dict[keyAttribute]['attr_sim_list'].index(attrName)
                    keysMatchingValue, attrNameValueScore = self.__getAttrRelevance(attrName, valueAttribute)
                    self.__collision_sim_dict[keyAttribute]['attr_sim_score'][elm_index] += keyValueScore * attrNameValueScore
    
    def __make_clean_dict_sim(self):
        print(f"[{type(self).__name__}]Running ---> __make_clean_dict_sim")
        for keyAttribute, simAttrKeys in self.__collision_sim_dict.items():
            self.collision_sim_dict[keyAttribute] = { 'attr_sim_list' : [], 'attr_sim_score' : []}
            tmpScorArr = [] + self.__collision_sim_dict[keyAttribute]['attr_sim_score']
            
            #if len(tmpScorArr) > 0:
                # valMediana = sum(tmpScorArr) - tmpScorArr[0]
                # valMediana = valMediana / len(tmpScorArr)
            #halfScoreList = CommonUtilities.get_vMed_numeric( self.__collision_sim_dict[keyAttribute]['attr_sim_score'])
            #avgScoreList = sum(self.__collision_sim_dict[keyAttribute]['attr_sim_score']) / len(self.__collision_sim_dict[keyAttribute]['attr_sim_score'])
            #avgScoreAccept =  avgScoreList * 0.5
            for idx in range(0, len(self.__collision_sim_dict[keyAttribute]['attr_sim_list'])):
                #Cutoff per contributi SottoMedia (Rumore di somma valori)
                if self.__collision_sim_dict[keyAttribute]['attr_sim_score'][idx] > 1:
                    self.collision_sim_dict[keyAttribute]['attr_sim_list'].append(self.__collision_sim_dict[keyAttribute]['attr_sim_list'][idx])
                    self.collision_sim_dict[keyAttribute]['attr_sim_score'].append(self.__collision_sim_dict[keyAttribute]['attr_sim_score'][idx])
        
    def __makeCollisionSimDictionary(self):
        print(f"[{type(self).__name__}]Running ---> __makeCollisionSimDictionary")

        self.exc_start_time = datetime.datetime.now()
        
        self.__make_dirty_dict_sim()
        self.__make_clean_dict_sim()
        
        CommonUtilities.writeDictToJson(self.collision_sim_dict, self.outFile)
        
        self.exc_end_time = datetime.datetime.now()
        
    def __printStats(self):
        print(f"\n########## {type(self).__name__} ##########\n")
        print(f"Time Spent: {self.exc_end_time - self.exc_start_time}\n")
        #print(f"Linked Object Found:{self.total_object_linked}\nLinked Files:{self.total_file_linkage}\nUnlinked Files:{self.total_file_external}\nTotal Files:{self.total_file_linkage+self.total_file_external}\n")
        print(f"########## ########## ##########\n")