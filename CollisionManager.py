import CollisionDictionary
import CollisionDictionaryInv
import CollisionDictionarySim
from Constats_App import *
import CommonUtilities

class CollisionManager:

    def __init__(self):
        self.filePathData = None
        self.collisionDict = None
        self.collisionInvDict = None
        self.collisionSimDict = None
        
    def __loadPathDataFromFile(self):
        self.filePathData = CommonUtilities.loadJsonFile(SOURCES_BASE_CM_DICT, ext="")
        
    def LoadPathData(self, filePathData):
        self.filePathData = filePathData
        
    def LoadCollisionDictionary(self):
        if not self.filePathData:
            self.__loadPathDataFromFile()
        self.collisionDict = CollisionDictionary.CollisionDictionary(self.filePathData)
        self.collisionDict.Load()
        
    def getCollisionDictionary(self):
        if not self.collisionDict:
            self.LoadCollisionDictionary()
        return self.collisionDict.collision_dict
        
    def LoadCollisionInvDictionary(self):
        self.collisionInvDict = CollisionDictionaryInv.CollisionDictionaryInv(self.getCollisionDictionary())
        self.collisionInvDict.Load()

    def getCollisionInvDictionary(self):
        if not self.collisionInvDict:
            self.LoadCollisionInvDictionary()
        return self.collisionInvDict.collision_inv_dict
    
    def LoadCollisionSimDictionary(self):
        self.collisionSimDict = CollisionDictionarySim.CollisionDictionarySim(self.getCollisionDictionary(), self.getCollisionInvDictionary())
        self.collisionSimDict.Load()

    def getCollisionSimDictionary(self):
        if not self.collisionSimDict:
            self.LoadCollisionSimDictionary()
        return self.collisionSimDict.collision_sim_dict