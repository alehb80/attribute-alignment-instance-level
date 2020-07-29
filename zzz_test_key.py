import CommonUtilities
from Constats_App import *
from fuzzywuzzy import fuzz


bigcluster = CommonUtilities.loadJsonFile(f"{PHASE_3_SOURCE_DIR}/big_cluster")
keySimInv = CommonUtilities.loadJsonFile( f"{PHASE_3_SOURCE_DIR}/testInv")

outputData = {}
outputData2 = {}
outputData3 = {}
outputData4 = {}
outputData5 = {}

##Passo 1 count gli elementi per ogni nomeAttributo
for key, values in bigcluster.items():
	if len(values) > 0 :
		outputData[key] = len(values)

CommonUtilities.writeDictToJson(outputData, f"{PHASE_3_SOURCE_DIR}/big_clusterkey.json")


####Passo 2 Conto gli elementi di ogni chiave suddividendoli secondo il nome attributo originale
for key, values in bigcluster.items():
	if len(values) > 0:
		outputData2[key] = {}
		for src, val, *oldAttrname in values:
			if len(oldAttrname) > 0 :
				if not oldAttrname[0] in outputData2[key].keys():
					outputData2[key][oldAttrname[0]] = 0
				outputData2[key][oldAttrname[0]] += 1
			else:
				if not key in outputData2[key].keys():
					outputData2[key][key] = 0
				outputData2[key][key] += 1


for key, value in outputData2.items():
	
	keyList= list(value.keys())

	for k2 in keyList:
		if outputData2[key][k2] < 3:
			score2 = fuzz.partial_ratio(key, k2)
			if score2  < 65:
				if not key in keySimInv[k2].keys():
					print(f"Elimino {k2} da {key}")
					del outputData2[key][k2]
			else:
				print(key, k2, score2)

CommonUtilities.writeDictToJson(outputData2, f"{PHASE_3_SOURCE_DIR}/big_clusterkey_2.json")



###Passo 3 Calcolo lo score | Per ogni chiave confronto la lista delle chiavi valore con tutte le altre
###Score calcolato come % di inclusione dell 'insieme piu piccolo
keylist = list(outputData2.keys())
for k1 in keylist:
	outputData3[k1] = {}
	for k2 in keylist:
		if len(outputData2[k1].keys()) > 0 and len(outputData2[k2].keys()) > 0:
			set_1 = set(outputData2[k1].keys())
			set_2 = set(outputData2[k2].keys())

			score = CommonUtilities.jaccard2( set_1, set_2)
			if score > 0.5:
				#if not k2 in outputData2[k1].keys():
				outputData3[k1][k2] = score * outputData[k2]
				#else:
					#outputData3[k1][k2] = score * outputData2[k1][k2]

CommonUtilities.writeDictToJson(outputData3, f"{PHASE_3_SOURCE_DIR}/big_clusterkey_3.json")

###Passo 4 Pulisco output del passo 3 tenendo solo il valore piu alto per ogni chiave
for key, value in outputData3.items():
	maxScore = 0
	maxkey = ""
	for key1, score in value.items():
		if score > maxScore:
			maxScore = score
			maxkey = key1
	outputData4[key] = { maxkey : maxScore }

CommonUtilities.writeDictToJson(outputData4, f"{PHASE_3_SOURCE_DIR}/big_clusterkey_4.json")




def findRootKey(currentKey):
	if currentKey in outputData5.keys():
		return currentKey
	else:
		#print(currentKey)
		#print(outputData4[currentKey])
		valkeys = list(outputData4[currentKey].keys())
		if len(valkeys) > 0:
			return findRootKey(valkeys[0])
		else:
			return "exceptions"

##Passo 5 trovo prima le root Key
for key, values in outputData4.items():
	for keySim in values.keys():
		if keySim == key:
			outputData5[key] = []
			outputData5[key].append(key)
outputData5["exceptions"] = []	

####Collego alle root key i nomi attributo corrispondenti
for key, values in outputData4.items():
	for keySim in values.keys():
		if not keySim == key:
			#print(f"Looking for rootKey {keySim}")
			if len(keySim) > 0 :
				rootk = findRootKey(keySim)
				outputData5[rootk].append(key)

CommonUtilities.writeDictToJson(outputData5, f"{PHASE_3_SOURCE_DIR}/big_clusterkey_5.json")


