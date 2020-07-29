import datetime
import os
import json
import CommonUtilities
from Constats_App import *


class CollisionDictionary:

    def __init__(self, filePathData):
    
        self.filePathData = filePathData
        self.srcDir = BASE_CL_SOURCE_DIR
        self.outFile = COLLISION_DICTIONARY_DICT
        self.collision_dict = {}
        
        #Dizionario di appoggio per le ricerche
        self.__collision_dict = {}
        
        self.total_values = 0
        
    def Load(self):
        if os.path.exists(self.outFile):
            print(f"{type(self).__name__} CollisionDictionary Founded! Loading")
            self.__loadCollisionDictionary()
        else:
            self.__makeCollisionDictionary()
            self.__printStats()
            
    def __loadCollisionDictionary(self):
        self.collision_dict = CommonUtilities.loadJsonFile(self.outFile, ext="")
        print(f"{type(self).__name__} CollisionDictionary Loaded!")
        
    def __mergeFileWithCollisionDict(self, jsnData):
        for key, value in jsnData.items():
            if not key in self.collision_dict.keys():
                self.collision_dict[key] = { "value_list" : []}
                self.__collision_dict[key] = { "value_list" : []}
            if not value in self.__collision_dict[key]['value_list']:
                self.__collision_dict[key]['value_list'].append(value)
                self.collision_dict[key]['value_list'].append((1, value))
            else:
                indexString = self.__collision_dict[key]['value_list'].index(value)
                count, strRes = self.collision_dict[key]['value_list'][indexString]
                self.collision_dict[key]['value_list'][indexString] = (count+1, strRes)
            
        
    def __makeCollisionDictionary(self):
    
        print(f"[{type(self).__name__}]Running ---> makeCollisionDictionary")

        self.exc_start_time = datetime.datetime.now()
        
        for objectSpect, objectValues in self.filePathData.items():
            for fileSource, filesList in objectValues.items():
                for filepath in filesList:
                    curr_jsonData = CommonUtilities.loadJsonFile(f"{self.srcDir}/{filepath}")
                    self.__mergeFileWithCollisionDict(curr_jsonData)
        CommonUtilities.writeDictToJson(self.collision_dict, self.outFile)
        
        self.exc_end_time = datetime.datetime.now()

        
    def __printStats(self):
        print(f"\n########## {type(self).__name__} ##########\n")
        print(f"Time Spent: {self.exc_end_time - self.exc_start_time}\n")
        #print(f"Linked Object Found:{self.total_object_linked}\nLinked Files:{self.total_file_linkage}\nUnlinked Files:{self.total_file_external}\nTotal Files:{self.total_file_linkage+self.total_file_external}\n")
        print(f"########## ########## ##########\n")