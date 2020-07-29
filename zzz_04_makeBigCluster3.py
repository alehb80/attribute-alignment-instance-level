import CommonUtilities
from Constats_App import *

dictBigCluster2 = CommonUtilities.loadJsonFile(f"{PHASE_3_SOURCE_DIR}/big_cluster2.json", ext="")
clusterTaDict = CommonUtilities.loadJsonFile(f"{PHASE_3_SOURCE_DIR}/big_clusterkey_5.json", ext="")


clusterTaDictinv = {}
bigCluster3 = {}


for key, values in clusterTaDict.items():
	for value in values:
		clusterTaDictinv[value] = key

CommonUtilities.writeDictToJson(clusterTaDictinv, f"{PHASE_3_SOURCE_DIR}/big_clusterkey_5_inv.json")

for key, values in dictBigCluster2.items():
	if len(values) > 0:
		rootKey = clusterTaDictinv[key]
		if not rootKey in bigCluster3.keys():
			bigCluster3[rootKey] = []

		for src, value, *oldAttrName in values:
			if len(oldAttrName) < 1:
				curr_item = (src, value, key)
			else:
				curr_item = (src, value, oldAttrName[0])
			bigCluster3[rootKey].append(curr_item)

CommonUtilities.writeDictToJson(bigCluster3, f"{PHASE_3_SOURCE_DIR}/big_cluster3.json")

