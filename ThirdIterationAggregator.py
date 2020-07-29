import os
import sys
import json
import datetime
import CommonUtilities
from Constats_App import *
import DynamicDictionaryManager
from AttributeMergeSelector import AttributeMergeSelector




class ThirdIterationFileAggregator:
    
    def __init__(self, lk_path_dict):
        self.lk_path_dict = lk_path_dict
        self.src_dir_name = PHASE_2_CL_SOURCE_DIR
        self.dst_dir_name = PHASE_3_SOURCE_DIR
        self.progress_bar_count = 0
        
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
            self.progress_bar_count +=1 
            CommonUtilities.progressBar(self.progress_bar_count, len(self.lk_path_dict.keys()), status=f"Agg: {filepath}")
        return mergedData


    def __AggregateFileS(self):
        
        self.progress_bar_count = 0
        print("")
        CommonUtilities.progressBar(self.progress_bar_count, len(self.lk_path_dict.keys()), status="Loading ..")
           
                
        new_merged_file = self.__AggregateFiles(self.lk_path_dict.values())
        CommonUtilities.writeDictToJson(new_merged_file, f"{self.dst_dir_name}/big_cluster.json")
            

        
    def RunInteration(self):
        
        print(f"[{type(self).__name__}]Running ---> RunInteration")
        
        self.exc_start_time = datetime.datetime.now()
        
        self.__findOrCreateDir("")
        self.__AggregateFileS()
        
        self.exc_end_time = datetime.datetime.now()
        self.__printStats()

        
    def __printStats(self):
        print(f"\n########## {type(self).__name__} ##########\n")
        print(f"Time Spent: {self.exc_end_time - self.exc_start_time}\n")
        #print(f"Linked Object Found:{self.total_object_linked}\nLinked Files:{self.total_file_linkage}\nUnlinked Files:{self.total_file_external}\nTotal Files:{self.total_file_linkage+self.total_file_external}\n")
        print(f"########## ########## ##########\n")