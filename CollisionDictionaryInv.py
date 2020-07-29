import datetime
import os
import json
import CommonUtilities
from Constats_App import *

class CollisionDictionaryInv:

    def __init__(self, collision_dict):
        self.__collision_dict = collision_dict
        self.outFile = COLLISION_DICTIONARY_INV_DICT
        self.collision_inv_dict = {}
        
    def Load(self):
        if os.path.exists(self.outFile):
            print(f"{type(self).__name__} CollisionInvDictionary Founded! Loading")
            self.__loadCollisionInvDictionary()
        else:
            self.__makeCollisionInvDictionary()
            self.__printStats()
            
    def __loadCollisionInvDictionary(self):
        self.collision_inv_dict = CommonUtilities.loadJsonFile(self.outFile, ext="")
        print(f"{type(self).__name__} CollisionInvDictionary Loaded!")
        
    def __makeCollisionInvDictionary(self):
        print(f"[{type(self).__name__}]Running ---> __makeCollisionInvDictionary")

        self.exc_start_time = datetime.datetime.now()
        
        for keyAttribute, valueAttributeList in self.__collision_dict.items():
            for valueAttributeCount, valueAttribute in valueAttributeList["value_list"]:
                if not valueAttribute in self.collision_inv_dict.keys():
                    self.collision_inv_dict[valueAttribute] = { 'attribute_list' : []}
                self.collision_inv_dict[valueAttribute]['attribute_list'].append( (valueAttributeCount, keyAttribute) )
        CommonUtilities.writeDictToJson(self.collision_inv_dict, self.outFile)
        
        self.exc_end_time = datetime.datetime.now()
        
    def __printStats(self):
        print(f"\n########## {type(self).__name__} ##########\n")
        print(f"Time Spent: {self.exc_end_time - self.exc_start_time}\n")
        #print(f"Linked Object Found:{self.total_object_linked}\nLinked Files:{self.total_file_linkage}\nUnlinked Files:{self.total_file_external}\nTotal Files:{self.total_file_linkage+self.total_file_external}\n")
        print(f"########## ########## ##########\n")