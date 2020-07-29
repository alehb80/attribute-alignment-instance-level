import os
import sys
import json
import datetime
import CommonUtilities
from Constats_App import *
import DynamicDictionaryManager
from AttributeMergeSelector import AttributeMergeSelector




class SecondIterationDictionary:
    
    def __init__(self, jsData):
        self.jsData = jsData
        self.dyn_col_sim = {}
        self.col_inv = {}
        #self.fileID = fileID

    def __makeCollInv(self):
        for AttrName, AttrValueObj in self.jsData.items():
            for AttrPath, AttrValue, *other in AttrValueObj:
                if not AttrValue in self.col_inv.keys():
                    self.col_inv[AttrValue] = { }
                if not AttrName in self.col_inv[AttrValue].keys():
                    self.col_inv[AttrValue][AttrName] = 0
                self.col_inv[AttrValue][AttrName] +=1
            
          
    def __DynColSim(self):
        ###Unisco Prima sulla base dell'uguaglianza dei valori
        
        for AttrName, AttrValues in self.jsData.items():
            self.dyn_col_sim[AttrName] = { }
            
            AttrValues_Set = set([AttrValue for AttrPath, AttrValue, *other in AttrValues])
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
        
        #CommonUtilities.writeDictToJson(self.col_inv, f"test/coll_{self.fileID}.json")
        #CommonUtilities.writeDictToJson(self.dyn_col_sim, f"test/sym_coll_{self.fileID}.json")
        


class SecondIterationAttrAggregator:

    def __init__(self, lk_path_dict, collisionInvDict, collisionSimDict):
        self.lk_path_dict = lk_path_dict
        self.src_dir_name = PHASE_2_SOURCE_DIR
        self.dst_dir_name = PHASE_2_CL_SOURCE_DIR
        self.__collisionInvDict = collisionInvDict
        self.__collisionSimDict = collisionSimDict
        self.__dynDict = DynamicDictionaryManager.DynamicDictionaryManager(COLLISION_DICTIONARY_SIM_DYN_DICT_02)
        self.__current_json_data = None
        
    def __findOrCreateDir(self, dirName):
        dirPath = f"{self.dst_dir_name}/{dirName}"
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
            

        
    def __aggregateSim(self, arrSim):
        mgSelect = AttributeMergeSelector( self.coll_inv_din, self.__current_json_data, arrSim)
        mgSelect.SelectValuesXKey()

        attrAggregationList = mgSelect.getListToMerge()

        ###Fase vera e propria di mergin
        for keySrc, keyDst, attrVal, attrValMtch, keyCohesion in attrAggregationList:
            for attrIndex in reversed(range(0, len(self.__current_json_data[keySrc]))):
                currItem = self.__current_json_data[keySrc][attrIndex]
                if attrVal == currItem[1]:
                    moveItem = self.__current_json_data[keySrc].pop(attrIndex)
                    if len(moveItem) < 3:
                        moveItem.append(keySrc)
                    self.__current_json_data[keyDst].append(moveItem)
                    if keyCohesion >= 80:
                        self.__dynDict.updateDictionary(keySrc, keyDst, attrVal, attrValMtch)
                        self.__dynDict.updateDictionary(keyDst, keySrc, attrValMtch, attrVal)
                    

        ####Pulisco le chiavi vuote
        keyList = self.__current_json_data.keys()

        for key in keyList:
            if len(self.__current_json_data[key]) < 1:
                self.__current_json_data[key]


    def __getSimilarAtrr(self):
        patterAtrr = []
        
        ##Elenco tutte le chiavi del file
        keys = list(self.__current_json_data.keys())
        
        ###Per Ogni Chiave cerco chiavi da accoppiare nel dictSIM dinamico
        for x in range(0, len(keys)):
            common_el = CommonUtilities.common_elements(keys, self.coll_sim_din[keys[x]])
            if len(common_el) > 1:
                patterAtrr.append((keys[x], common_el))
        return len(patterAtrr) > 0, patterAtrr

    def __AggregateAttributes(self):
        hasSim, simArr = self.__getSimilarAtrr()
        if hasSim:
            self.__aggregateSim(simArr)
    
    def __AggregateAttributesFile(self):
        
        progressCount = 0
        print("")
        CommonUtilities.progressBar(progressCount, len(self.lk_path_dict.keys()), status="Loading ..")
        for objectSpect, filepath in self.lk_path_dict.items():
            progressCount +=1 
            CommonUtilities.progressBar(progressCount, len(self.lk_path_dict.keys()), status=f"Agg: {objectSpect}")  
            
                
                
            self.__current_json_data = CommonUtilities.loadJsonFile(f"{self.src_dir_name}/{filepath}")
            #print(f"{self.src_dir_name}/{filepath}")
            ###Appena viene caricato il file per il l' aggregazione creo i dizionari dinamici
            self.dym_dict_local = SecondIterationDictionary(self.__current_json_data)
            self.dym_dict_local.Load()
                
            ##Istanzio nella class i dinionari
            self.coll_sim_din =  self.dym_dict_local.dyn_col_sim
            self.coll_inv_din =  self.dym_dict_local.col_inv
                
            self.__AggregateAttributes()
            
            CommonUtilities.writeDictToJson(self.__current_json_data, f"{self.dst_dir_name}/{filepath}.json")
        self.__dynDict.save()
        
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




class SecondIterationFileAggregator:
    
    def __init__(self, lk_path_dict):
        self.lk_path_dict = lk_path_dict
        self.lk_2_path_dict = {}
        self.src_dir_name = PHASE_1_CL_SOURCE_DIR
        self.dst_dir_name = PHASE_2_SOURCE_DIR
        self.dst_lk_path_dict = SOURCES_PHASE_2_LK_DICT
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
                mergedData[attrName] += attrValue
        return mergedData

    def __AggregateFileSameSourceAndSpect(self):
        
        progressCount = 0
        print("")
        CommonUtilities.progressBar(progressCount, len(self.lk_path_dict.keys()), status="Loading ..")
        for objectSpect, objectSources in self.lk_path_dict.items():
            progressCount +=1 
            CommonUtilities.progressBar(progressCount, len(self.lk_path_dict.keys()), status=f"Agg: {objectSpect}")
            self.lk_2_path_dict[objectSpect] = {}
            
            for sources, filespath in objectSources.items():
                self.__findOrCreateDir(sources)
                
                self.lk_2_path_dict[objectSpect][sources] = f"{sources}/{self.newFileNameID}"
                new_merged_file = self.__AggregateFiles(filespath)
                CommonUtilities.writeDictToJson(new_merged_file, f"{self.dst_dir_name}/{sources}/{self.newFileNameID}.json")
                self.newFileNameID += 1

    def __AggregateFileSameSpect(self):
        
        progressCount = 0
        print("")
        CommonUtilities.progressBar(progressCount, len(self.lk_path_dict.keys()), status="Loading ..")
        for objectSpect, objectSources in self.lk_path_dict.items():
            progressCount +=1 
            CommonUtilities.progressBar(progressCount, len(self.lk_path_dict.keys()), status=f"Agg: {objectSpect}")
            
            pathToMerge = []
            for sources, filespath in objectSources.items():
               pathToMerge.append(filespath)
                
            self.lk_2_path_dict[objectSpect] = f"{self.newFileNameID}"
            new_merged_file = self.__AggregateFiles(pathToMerge)
            CommonUtilities.writeDictToJson(new_merged_file, f"{self.dst_dir_name}/{self.newFileNameID}.json")
            self.newFileNameID += 1
            

        
    def RunInteration(self):
        
        print(f"[{type(self).__name__}]Running ---> RunInteration")
        
        self.exc_start_time = datetime.datetime.now()
        
        self.__findOrCreateDir("")
        self.__AggregateFileSameSpect()
        
        CommonUtilities.writeDictToJson(self.lk_2_path_dict, self.dst_lk_path_dict)
        
        self.exc_end_time = datetime.datetime.now()
        self.__printStats()

    def LoadPath(self):
        self.lk_2_path_dict = CommonUtilities.loadJsonFile(self.dst_lk_path_dict , ext='')
        
    def getDictionary_LK_Path(self):
        return self.lk_2_path_dict
        
    def __printStats(self):
        print(f"\n########## {type(self).__name__} ##########\n")
        print(f"Time Spent: {self.exc_end_time - self.exc_start_time}\n")
        #print(f"Linked Object Found:{self.total_object_linked}\nLinked Files:{self.total_file_linkage}\nUnlinked Files:{self.total_file_external}\nTotal Files:{self.total_file_linkage+self.total_file_external}\n")
        print(f"########## ########## ##########\n")