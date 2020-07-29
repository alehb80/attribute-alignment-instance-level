import os
import sys
import json
import datetime
import CommonUtilities
from DataCleaner import DataCleaner
from Constats_App import *

class DataCleanerManager:

    def __init__(self, cm_path_dict):
        self.src_dir_name = BASE_SOURCE_DIR
        self.dst_dir_name = BASE_CL_SOURCE_DIR
        self.cm_path_dict = cm_path_dict
        self.discarded_info_pool = {}
        self.composite_value_pool = {}

        with open("attrToAnalize.txt", "r") as AttrNamesF:
            gtAttrNames = AttrNamesF.readlines()

        self.gtAttrNames = [line[:-1] for line in gtAttrNames]
         
        #Create Base folder
        self.__findOrCreateDir("")
        
    def __findOrCreateDir(self, dirName):
        dirPath = f"{self.dst_dir_name}/{dirName}"
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)

    def __cleanSingleFile(self, source_name, file_path):
    
        #print(f"[{type(self).__name__}]Running ---> __cleanSingleFile: {file_path}")

        jsnData = CommonUtilities.loadJsonFile(f"{self.src_dir_name}/{file_path}")
        dt_cleaner = DataCleaner(jsnData, self.gtAttrNames)
        dt_cleaner.cleanKeys()
        dt_cleaner.cleanValues()

        jsnDataCl = dt_cleaner.getSignificantData()
        
        empty_keys_d, empty_value_d, composite_value_d = dt_cleaner.getEmptyDataKeys()
        
        if len(empty_keys_d.keys()) + len(empty_value_d.keys()) > 0:
            self.discarded_info_pool[file_path] = { "key_empty" : empty_keys_d, "value_empty" : empty_value_d}
            
        if len(composite_value_d.keys()) > 0:
            self.composite_value_pool[file_path] = composite_value_d
        
        CommonUtilities.writeDictToJson(jsnDataCl, f"{self.dst_dir_name}/{file_path}.json")

    def cleanDataSet(self):
    
        print(f"[{type(self).__name__}]Running ---> cleanDataSet")
        
        self.exc_start_time = datetime.datetime.now()

        for object_spect, object_val in self.cm_path_dict.items():
            for source_name, source_files in object_val.items():
                self.__findOrCreateDir(source_name)
                for file_path in source_files:
                    self.__cleanSingleFile(source_name, file_path)

        CommonUtilities.writeDictToJson(self.discarded_info_pool, f"{DROPPED_ATTRIBUTES_FILES}")
        CommonUtilities.writeDictToJson(self.composite_value_pool, f"{COMPOSITE_ATTRIBUTES_FILES}")
        
        self.exc_end_time = datetime.datetime.now()
        self.__printStats()
        
    def __printStats(self):
        print(f"\n########## {type(self).__name__} ##########\n")
        print(f"Time Spent: {self.exc_end_time - self.exc_start_time}\n")
        #print(f"Linked Object Found:{self.total_object_linked}\nLinked Files:{self.total_file_linkage}\nUnlinked Files:{self.total_file_external}\nTotal Files:{self.total_file_linkage+self.total_file_external}\n")
        print(f"########## ########## ##########\n")