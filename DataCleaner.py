from Constats_App import *
import CommonUtilities


class StringKeyCleaner:

    def __init__(self, srcString):
        self.srcString = srcString.lower()
        self.srcString = self.srcString.encode('ascii', errors="ignore").decode()
        
    def cleanKeyStr(self):
        self.replaceSpecialChar()
        self.removeAddInfoKeys()
        self.remove_bad_token_key()
        return self.srcString

    def removeAddInfoKeys(self):
        if ":" in self.srcString:
            self.srcString = self.srcString[0:self.srcString.find(":")]

    def replaceSpecialChar(self):
        escape_char = ["(", ")", "-"]
        for cr in escape_char:
            if cr in self.srcString:
                self.srcString = self.srcString.replace(cr, "")
        if "/" in self.srcString:
            self.srcString = self.srcString.replace("/", " ")
        
    def remove_bad_token_key(self):
        self.srcString = " ".join([word for word in self.srcString.split(" ") if not word in BAD_WORDS_KEY and len(word) > 1])
        
        
class StringValueCleaner:

    def __init__(self, srcString):
        self.srcString = srcString.lower()
        self.srcString = self.srcString.encode('ascii', errors="ignore").decode()

    def cleanValStr(self):
        self.replaceSpecialChar()
        self.remove_bad_token_value()
        return self.srcString

    def replaceSpecialChar(self):
        escape_char = ["(", ")", "-", "\\n", "\n", "/", ",", "&", ";", "specified manufacturer"]
        for cr in escape_char:
            if cr in self.srcString:
                self.srcString = self.srcString.replace(cr, " ")
        misurWord = [" mp", "megapixels", "megapixel"]
        for cr in misurWord:
            if cr in self.srcString:
                self.srcString = self.srcString.replace(cr, " mp")
        
    def getStr(self):
        return self.srcString

    def remove_bad_token_value(self):
        self.srcString = " ".join([word for word in self.srcString.split(" ") if not word in BAD_WORDS_VALUES and len(word) > 1])


class StringCompositeValueCleaner:

    def __init__(self, srcArray):
        self.srcArray = srcArray
        self.dstArray = []

    def cleanValues(self):
        for vStr in self.srcArray:
            new_vStr = StringValueCleaner(vStr)
            new_vStr.replaceSpecialChar()
            self.dstArray.append(new_vStr.getStr())
        return self.dstArray

class DataCleaner:

    def __init__(self, srcData, validKeysArr):
        self.srcData = srcData
        self.dstData = {}
        self.dstCleanData = {}
        self.droppedKeys = {}
        self.droppedValues = {}
        self.compositeValues = {}
        self.validKeys = validKeysArr
        
    def cleanKeys(self):
        uuidKey = 0
        for key, value in self.srcData.items():
            if key == "<page title>":
                continue
            strkCleaner = StringKeyCleaner(key)
            newKey = strkCleaner.cleanKeyStr()
            if not newKey in self.validKeys:
                continue
            if type(value).__name__ == 'list':
                value = CommonUtilities.listToStringOrSetList(value)
            if not newKey == key and newKey in self.dstData.keys():
                newKey += str(uuidKey)
                uuidKey +=1
            if len(newKey) and not type(value).__name__ == 'list':
                self.dstData[newKey] = value
            elif type(value).__name__ == 'list':
                value_cl = StringCompositeValueCleaner(value)
                value = value_cl.cleanValues()
                self.compositeValues[key] = value
            else:
                self.droppedKeys[key] = value
            
    
    def cleanValues(self):
        for key, value in self.dstData.items():
            
            strValCleaner = StringValueCleaner(value)
            newVal = strValCleaner.cleanValStr()

            uuidVal = ""
            index = 0
            if len(newVal) and len(newVal) <= 50:
                if "pixel" in key and newVal.replace('.','',1).isdigit():
                    newVal += " mp"
                self.dstCleanData[key] = newVal
            else:
                self.droppedValues[key] = value
 
    def getSignificantData(self):
        return self.dstCleanData
        
    def getEmptyDataKeys(self):
        return self.droppedKeys, self.droppedValues, self.compositeValues
