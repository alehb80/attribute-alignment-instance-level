from Constats_App import *
import CommonUtilities


dimdict_1 = CommonUtilities.loadJsonFile(COLLISION_DICTIONARY_SIM_DYN_DICT_01, ext="")
dimdict_2 = CommonUtilities.loadJsonFile(COLLISION_DICTIONARY_SIM_DYN_DICT_02, ext="")

set_1 = set(dimdict_1.keys())
set_2 = set(dimdict_2.keys())

print(set_2.symmetric_difference(set_1))
print(len(set_1), len(set_2), len(set_2.intersection(set_1)), len(set_2.symmetric_difference(set_1)))


