import CommonUtilities
from Constats_App import *


dictSim = CommonUtilities.loadJsonFile(f"{COLLISION_DICTIONARY_SIM_DICT}", ext="")

dictSimInv = {}

for key in dictSim:

	dictSimInv[key] = {}
	for key2 in dictSim:
		keysList = dictSim[key2]['attr_sim_list']
		if key in keysList:
			for x in range(0, len(keysList)):
				if dictSim[key2]['attr_sim_list'][x] == key:
					dictSimInv[key][key2] = dictSim[key2]['attr_sim_score'][x]

CommonUtilities.writeDictToJson(dictSimInv, f"{PHASE_3_SOURCE_DIR}/testInv.json")
