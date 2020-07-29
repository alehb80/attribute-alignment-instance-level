
import CommonUtilities
from Constats_App import *


dictBigCluster = CommonUtilities.loadJsonFile(f"{PHASE_3_SOURCE_DIR}/big_cluster.json", ext="")

dictColl = {}
dictColl2 = {}
dictCollInv = {}


for key, values in dictBigCluster.items():
	dictColl[key] = {}

	for src, val, *out in values:
		if not val in dictColl[key].keys():
			dictColl[key][val] = 0 
		dictColl[key][val] += 1
CommonUtilities.writeDictToJson(dictColl, f"{PHASE_3_SOURCE_DIR}/big_clusterColl.json")

for key, values in dictBigCluster.items():
	dictColl2[key] = {}

	for src, val, *out in values:
		if not val in dictColl2[key].keys():
			dictColl2[key][val] = {}
		if len(out) > 0:
			oldAttrName = out[0]
		else:
			oldAttrName = key
		if not oldAttrName in dictColl2[key][val].keys():
			dictColl2[key][val][oldAttrName] = 0
		dictColl2[key][val][oldAttrName] += 1
CommonUtilities.writeDictToJson(dictColl2, f"{PHASE_3_SOURCE_DIR}/big_clusterColl2.json")


for key, value in dictColl.items():
	
	for valName, valCount in value.items():

		for key2, value2 in dictColl.items():
			for valName2, valCount2 in value2.items():

				if not key == key2 and valCount == 1 and not valCount2 == 1 and not valName.replace(".", "").isdigit():
					if valName == valName2:
						print(key, key2, valName, valCount, valCount2)
						if not valName in dictCollInv.keys():
							dictCollInv[valName] = {}
						dictCollInv[valName][key] = dictColl2[key][valName]
						dictCollInv[valName][key2] = dictColl2[key2][valName]

CommonUtilities.writeDictToJson(dictCollInv, f"{PHASE_3_SOURCE_DIR}/big_clusterCollInv.json")


dictMove = {}
for attrValue, attrNamekeys in dictCollInv.items():
	for attrNameKey, attroldNameKeys in attrNamekeys.items():
		if not attrNameKey in attroldNameKeys.keys():
			for keychild in attroldNameKeys.keys():
				if keychild in attrNamekeys.keys():
					if not attrValue in dictMove.keys():
						dictMove[attrValue] = {}
					if not attrNameKey in dictMove[attrValue].keys():
						dictMove[attrValue][attrNameKey] = {}
					dictMove[attrValue][attrNameKey][keychild] = dictCollInv[attrValue][attrNameKey][keychild]




###Riscrivo il big cluster
big_cluster_2 = {}

for key in dictBigCluster.keys():
	big_cluster_2[key] = []

for key, values in dictBigCluster.items():
	for src, value, *oldAttr in values:
		if len(oldAttr) >= 1:
			item = (src, value, oldAttr[0])
		else:
			item = (src, value)
		if not value in dictMove.keys() or len(oldAttr) < 1:
			big_cluster_2[key].append(item)
		else:
			oldKey = oldAttr[0]
			big_cluster_2[oldKey].append(item)

CommonUtilities.writeDictToJson(big_cluster_2, f"{PHASE_3_SOURCE_DIR}/big_cluster2.json")