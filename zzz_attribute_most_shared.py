from Constats_App import *
import CommonUtilities


ordered_value = []

collisionInvData = CommonUtilities.loadJsonFile(COLLISION_DICTIONARY_INV_DICT, ext="")
for key, val in collisionInvData.items():
	
	ordered_value.append((key, len(val['attribute_list'])))

ordered_value.sort(key=lambda x : x[1], reverse=True)

for x in range(0, 50):
	print(ordered_value[x])