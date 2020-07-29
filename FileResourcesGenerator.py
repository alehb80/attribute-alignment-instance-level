import os
import sys
import xlrd 
import json
import CommonUtilities
import datetime
from Constats_App import *

class FileResourcesGenerator:

    def __init__(self, linkageFileName=ENTITY_FILE_PATH):

        self.lkFileName = linkageFileName
        self.dictionary_lk_path = {}
        self.dictionary_ext_path = {}
        self.dictionary_cm_path = {}
        self.resources_founded = []

        self.total_object_linked = 0
        self.total_file_linkage = 0
        self.total_file_external = 0



    def __getLeftRightElment(self, rowElment):
        return [ colm.replace("//", "/") for colm in rowElment]
        
    def getDictionary_CM_Path(self):
        return self.dictionary_cm_path
        
    def getDictionary_LK_Path(self):
        return self.dictionary_lk_path
        

    def loadJsonPathFiles(self):

        self.dictionary_lk_path = CommonUtilities.loadJsonFile(SOURCES_BASE_LK_DICT, ext="")
        self.dictionary_ext_path = CommonUtilities.loadJsonFile(SOURCES_BASE_EXT_DICT, ext="")
        self.dictionary_cm_path = CommonUtilities.loadJsonFile(SOURCES_BASE_CM_DICT, ext="")

        print(f"[{type(self).__name__}]Completed ---> loadJsonPathFiles")

    def loadAndMakePathResources(self):
        
        self.exc_start_time = datetime.datetime.now()
        
        self.makeJsonPathFile_LK()
        self.makeJsonPathFile_EXT()
        self.makeJsonPathFile_Common()
        
        self.exc_end_time = datetime.datetime.now()
        
        self.printStats()
        
        
        

    def makeJsonPathFile_LK(self): 
    
        print(f"[{type(self).__name__}]Running ---> makeJsonPathFile_LK")
        
        wb = xlrd.open_workbook(self.lkFileName) 
        sheet = wb.sheet_by_index(0) 
        
        for x in range(1, sheet.nrows):
            CommonUtilities.progressBar(x, sheet.nrows)
            row = CommonUtilities.splitOnComma(sheet.cell_value(x, 0))
            left_r, righ_r = self.__getLeftRightElment(row)
            source_lr = CommonUtilities.getSourceFromPath(left_r)
            source_rr = CommonUtilities.getSourceFromPath(righ_r)
            
            if not left_r in self.dictionary_lk_path.keys() and not left_r in self.resources_founded:
                self.dictionary_lk_path[left_r] = { source_lr : [left_r] }
                self.resources_founded.append(left_r)
                self.total_object_linked += 1
                self.total_file_linkage += 1
                
            if not righ_r in self.resources_founded:
                if not source_rr in self.dictionary_lk_path[left_r].keys():
                    self.dictionary_lk_path[left_r][source_rr] = []
                self.dictionary_lk_path[left_r][source_rr].append(righ_r)
                self.resources_founded.append(righ_r)
                self.total_file_linkage += 1

        CommonUtilities.writeDictToJson(self.dictionary_lk_path, SOURCES_BASE_LK_DICT)
            
    def makeJsonPathFile_EXT(self): 
    
        print(f"[{type(self).__name__}]Running ---> makeJsonPathFile_EXT")

        for dir in os.listdir(BASE_SOURCE_DIR):
            for file in os.listdir(f"{BASE_SOURCE_DIR}/{dir}/"):
                filename = file.split(".")[0]
                rs = f"{dir}/{filename}"
                if not rs in self.resources_founded:
                    self.dictionary_ext_path[rs] = { CommonUtilities.getSourceFromPath(rs) : [rs] }
                    self.total_file_external += 1
        
        CommonUtilities.writeDictToJson(self.dictionary_ext_path, SOURCES_BASE_EXT_DICT)


    def makeJsonPathFile_Common(self):
    
        print(f"[{type(self).__name__}]Running ---> makeJsonPathFile_Common")

        self.dictionary_cm_path = CommonUtilities.merge_two_dicts(self.dictionary_lk_path, self.dictionary_ext_path)
        CommonUtilities.writeDictToJson(self.dictionary_cm_path, SOURCES_BASE_CM_DICT)
        
        
    def printStats(self):
        print(f"\n########## {type(self).__name__} ##########\n")
        print(f"Time Spent: {self.exc_end_time - self.exc_start_time}")
        print(f"Linked Object Found:{self.total_object_linked}\nLinked Files:{self.total_file_linkage}\nUnlinked Files:{self.total_file_external}\nTotal Files:{self.total_file_linkage+self.total_file_external}\n")
        print(f"########## ########## ##########\n")
