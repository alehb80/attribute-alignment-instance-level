import json
import os
import CommonUtilities
from Constats_App import *



class DynamicDictionaryManager:

    def __init__(self, path):
        self.__pathDictionary = path

        self.__Load()

    def __Load(self):
        if not os.path.exists(self.__pathDictionary):
            CommonUtilities.writeDictToJson({}, self.__pathDictionary)
        self.__dyn_dictionary = CommonUtilities.loadJsonFile(self.__pathDictionary, ext="")

    def getDynDictionary(self):
        return self.__dyn_dictionary

    def updateDictionary(self, key, keySim, val, valSim):
        if not key in self.__dyn_dictionary.keys():
            #self.__dyn_dictionary[key] = { "valSimSet" : [] }
            self.__dyn_dictionary[key] = { }
        if not keySim in self.__dyn_dictionary[key].keys():
            self.__dyn_dictionary[key][keySim] = 0
        self.__dyn_dictionary[key][keySim] += 1
        #if not val in self.__dyn_dictionary[key]["valSimSet"]:
        #    self.__dyn_dictionary[key]["valSimSet"].append(val)
        #if not valSim in self.__dyn_dictionary[key]["valSimSet"]:
        #    self.__dyn_dictionary[key]["valSimSet"].append(valSim)

    def save(self):
        CommonUtilities.writeDictToJson(self.__dyn_dictionary, self.__pathDictionary)