
with open(f"sources_3/gt_onevalue.csv", "r") as gtFile:
	ground_truth = set(gtFile.readlines())

with open(f"sources_3/custom_ground.csv", "r") as cgtFile:
	custom_ground_truth = set(cgtFile.readlines())

# calcolo tp, fn e fp
tp = ground_truth.intersection(custom_ground_truth)
fn = ground_truth.difference(custom_ground_truth)
fp = custom_ground_truth.difference(ground_truth)


print(len(tp))
print(len(fn))
print(len(fp))


precision = len(tp)/(len(tp) + len(fp))
recall = len(tp)/(len(tp) + len(fn))
f_measure = (2 * precision * recall)/(precision + recall)


print("Precision: " + str(precision))
print("Recall: " + str(recall))
print("F-Measure: " + str(f_measure))

print("Creating False Positive")

with open("falsePositive.txt", "w") as fpFile:
	currentList = sorted(list(fp))
	for elm in currentList:
		fpFile.write(f"{elm}\n")