import os
import sys
import json
import datetime
import CommonUtilities
from Constats_App import *



class FirstIterationAttrAggregator:

    def __init__(self, lk_path_dict, collisionInvDict, collisionSimDict):
        self.lk_path_dict = lk_path_dict
        self.src_dir_name = PHASE_1_SOURCE_DIR
        self.dst_dir_name = PHASE_1_CL_SOURCE_DIR
        self.__collisionInvDict = collisionInvDict
        self.__collisionSimDict = collisionSimDict
        
        self.__current_json_data = None
        
    def __findOrCreateDir(self, dirName):
        dirPath = f"{self.dst_dir_name}/{dirName}"
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
            
    def __getSimilarAtrr(self):
        patterAtrr = []
        
        ##Elenco tutte le chiavi del file
        keys = list(self.__current_json_data.keys())
        
        ###Per Ogni Chiave cerco chiavi da accoppiare nel dictSIM
        for x in range(0, len(keys)):
            common_el = CommonUtilities.common_elements(keys, self.__collisionSimDict[keys[x]]['attr_sim_list'])
            if len(common_el) > 1:
                patterAtrr.append((keys[x], common_el))
        return len(patterAtrr) > 0, patterAtrr
        
    def __aggregateSim(self, arrSim):
        ##Per ogni coppia chiave --> chiavi_simili
        for key, keySim in arrSim:
            for k2 in keySim:
                ###Se la chiave e' sinonimo e non la stessa
                if not key == k2:
                    ###Se k2 esiste potrebbe essere stata accorpata
                    if k2 in self.__current_json_data.keys() and key in self.__current_json_data.keys():
                        #Costruisco due array contenenti gli indici numerici dei valori comuni delle due chiavi
                        currmtc1, currmtc2 = CommonUtilities.matchValues(self.__current_json_data[key], self.__current_json_data[k2])
                        if len(currmtc2) > 0:
                            for idx in range(0, len(currmtc2)):
                                ##Calcolo le occorrenze delle chiavi rispetto al valore X ogni valore in comune
                                s1, s2 = CommonUtilities.scoreBinaryValueMatch(key, k2, self.__collisionInvDict[self.__current_json_data[k2][currmtc2[idx]][1]])
                                if s1 >= s2:
                                    item = self.__current_json_data[k2].pop(currmtc2[idx])
                                    item.append(k2)
                                    self.__current_json_data[key].append(item)
                                    ##Dopo aver fatto il pop se la chiave non contiene valori la elimino
                                    if len(self.__current_json_data[k2]) < 1:
                                        del self.__current_json_data[k2]

                            for idx in range(0, len(currmtc1)):
                                s1, s2 = CommonUtilities.scoreBinaryValueMatch(key, k2, self.__collisionInvDict[self.__current_json_data[key][currmtc1[idx]][1]])
                                if s1 < s2:
                                    item = self.__current_json_data[key].pop(currmtc1[idx])
                                    item.append(key)
                                    self.__current_json_data[k2].append(item)
                                    ##Dopo aver fatto il pop se la chiave non contiene valori la elimino
                                    if len(self.__current_json_data[key]) < 1:
                                        del self.__current_json_data[key]

    def __AggregateAttributes(self):
        hasSim, simArr = self.__getSimilarAtrr()
        if hasSim:
            self.__aggregateSim(simArr)
    
    def __AggregateAttributesFile(self):
        
        for objectSpect, objectSources in self.lk_path_dict.items():
            for sources, filepath in objectSources.items():
            
                self.__findOrCreateDir(sources)
                
                self.__current_json_data = CommonUtilities.loadJsonFile(f"{self.src_dir_name}/{filepath}")
                self.__AggregateAttributes()

                CommonUtilities.writeDictToJson(self.__current_json_data, f"{self.dst_dir_name}/{filepath}.json")
                
        
    def RunInterationCleaning(self):
        
        print(f"[{type(self).__name__}]Running ---> RunInterationCleaning")
        
        self.exc_start_time = datetime.datetime.now()
        
        self.__findOrCreateDir("")
        self.__AggregateAttributesFile()
        
        self.exc_end_time = datetime.datetime.now()
        self.__printStats()
        
    def __printStats(self):
        print(f"\n########## {type(self).__name__} ##########\n")
        print(f"Time Spent: {self.exc_end_time - self.exc_start_time}\n")
        #print(f"Linked Object Found:{self.total_object_linked}\nLinked Files:{self.total_file_linkage}\nUnlinked Files:{self.total_file_external}\nTotal Files:{self.total_file_linkage+self.total_file_external}\n")
        print(f"########## ########## ##########\n")



class FirstIterationDictionary:
    
    def __init__(self, jsData, fileID):
        self.jsData = jsData
        self.dyn_col_sim = {}
        self.col_inv = {}
        self.fileID = fileID
        
    def __makeDynCollSym(self):
        pass

    def __makeCollInv(self):
        for AttrName, AttrValueObj in self.jsData.items():
            for AttrPath, AttrValue in AttrValueObj:
                if not AttrValue in self.col_inv.keys():
                    self.col_inv[AttrValue] = { }
                if not AttrName in self.col_inv[AttrValue].keys():
                    self.col_inv[AttrValue][AttrName] = 0
                self.col_inv[AttrValue][AttrName] +=1
            
          
    def __DynColSim(self):
        ###Unisco Prima sulla base dell'uguaglianza dei valori
        
        for AttrName, AttrValues in self.jsData.items():
            self.dyn_col_sim[AttrName] = { }
            
            AttrValues_Set = set([AttrValue for AttrPath, AttrValue in AttrValues])
            for AttrValue in AttrValues_Set:
                ###Per ogmi valore Attributo di AttrName cerco valori Attr uguali e simili
                similarValueList = CommonUtilities.getSimilarValues(AttrValue, self.col_inv.keys())
                #print(AttrValue, similarValueList)
                ###Per ogni valore Attributo Trovato cerco a quale chiave è associato e lo aggiungo            
                for similarValue in similarValueList:
                    keysOfAttributes = self.col_inv[similarValue]
                    for key, key_count in keysOfAttributes.items():
                        if not key in self.dyn_col_sim[AttrName].keys():
                            self.dyn_col_sim[AttrName][key] = 0
                        self.dyn_col_sim[AttrName][key] += key_count
        
    def Load(self):
        self.__makeCollInv()
        self.__DynColSim()
        
        CommonUtilities.writeDictToJson(self.col_inv, f"test/coll_{self.fileID}.json")
        CommonUtilities.writeDictToJson(self.dyn_col_sim, f"test/sym_coll_{self.fileID}.json")
        


class FirstIterationFileAggregator:
    
    def __init__(self, lk_path_dict):
        self.lk_path_dict = lk_path_dict
        self.lk_1_path_dict = {}
        self.src_dir_name = BASE_CL_SOURCE_DIR
        self.dst_dir_name = PHASE_1_SOURCE_DIR
        self.dst_lk_path_dict = SOURCES_PHASE_1_LK_DICT
        self.newFileNameID = 1
        
    def __findOrCreateDir(self, dirName):
        dirPath = f"{self.dst_dir_name}/{dirName}"
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
            
    def __AggregateFiles(self, filesList):
        
        mergedData = {}

        for filepath in filesList:
            jsdata = CommonUtilities.loadJsonFile(f"{self.src_dir_name}/{filepath}")
            for attrName, attrValue in jsdata.items():
                if not attrName in mergedData.keys():
                    mergedData[attrName] = []
                mergedData[attrName].append((filepath, attrValue))
        return mergedData

    def __AggregateFileSameSourceAndSpect(self):
        
        for objectSpect, objectSources in self.lk_path_dict.items():
            self.lk_1_path_dict[objectSpect] = {}
            
            for sources, filespath in objectSources.items():
                self.__findOrCreateDir(sources)
                
                self.lk_1_path_dict[objectSpect][sources] = f"{sources}/{self.newFileNameID}"
                new_merged_file = self.__AggregateFiles(filespath)
                dym_dict = FirstIterationDictionary(new_merged_file, self.newFileNameID)
                dym_dict.Load()
                CommonUtilities.writeDictToJson(new_merged_file, f"{self.dst_dir_name}/{sources}/{self.newFileNameID}.json")
                self.newFileNameID += 1
            

        
    def RunInteration(self):
        
        print(f"[{type(self).__name__}]Running ---> RunInteration")
        
        self.exc_start_time = datetime.datetime.now()
        
        self.__findOrCreateDir("")
        self.__AggregateFileSameSourceAndSpect()
        
        CommonUtilities.writeDictToJson(self.lk_1_path_dict, self.dst_lk_path_dict)
        
        self.exc_end_time = datetime.datetime.now()
        self.__printStats()
        
    def getDictionary_LK_Path(self):
        return self.lk_1_path_dict
        
    def __printStats(self):
        print(f"\n########## {type(self).__name__} ##########\n")
        print(f"Time Spent: {self.exc_end_time - self.exc_start_time}\n")
        #print(f"Linked Object Found:{self.total_object_linked}\nLinked Files:{self.total_file_linkage}\nUnlinked Files:{self.total_file_external}\nTotal Files:{self.total_file_linkage+self.total_file_external}\n")
        print(f"########## ########## ##########\n")