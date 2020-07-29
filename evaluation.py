import pandas as pd
from tqdm import tqdm
import json
from collections import defaultdict
import itertools


# Leggo la ground truth in un Pandas dataframe
pos_df = pd.read_csv('sources_3/gt_onevalue.csv')
# set di coppie match
ground_truth = set(map(tuple, pos_df[['left_instance_attribute', 'right_instance_attribute']].values))


all_pairs = set()


# prendo il risultato della terza iterazione
with open('sources_3/big_cluster3_refactor.json', 'r') as f:
    current_json = json.load(f)

    # set di coppie + ordine lessicografico
    # per ogni json mi prendo i valori di ogni chiave rappresentata dal nome di un attributo
    # e li aggiungo ad un set
    d1 = defaultdict(set)
    for k, v in current_json.items():

        if not k == "<page title>" and not k == "__unstructured":

            for vv in v:

                if len(vv) == 3:

                    instance_attr = vv[0] + "//" + vv[2]
                else:
                    instance_attr = vv[0] + "//" + k

                d1[k].add(instance_attr)
                #a=list(d1)


    #with open("d1.json", "w") as outfile:
    #    json.dump(a, outfile)
                #print(k)
                #print(instance_attr)

        # faccio le combinazioni a due di tutti gli elementi in d1
# e li salvo in un nuovo set all_pairs che andrò a confrontare con la ground truth
        #print(d1)
        for k1, v1 in d1.items():
        ##    print(k1)

            pairs = set(itertools.combinations(v1, 2))
            all_pairs.update(pairs)


# ordino le coppie in all_pairs
all_pairs_sorted = set()
for pair in all_pairs:
    left, right = pair
    if left > right:
        pair = (right, left)
    all_pairs_sorted.add(pair)


# calcolo tp, fn e fp
tp = ground_truth.intersection(all_pairs_sorted)
fn = ground_truth.difference(all_pairs_sorted)
fp = all_pairs_sorted.difference(ground_truth)


print(len(tp))
print(len(fn))
print(len(fp))


precision = len(tp)/(len(tp) + len(fp))
recall = len(tp)/(len(tp) + len(fn))
f_measure = (2 * precision * recall)/(precision + recall)


print("Precision: " + str(precision))
print("Recall: " + str(recall))
print("F-Measure: " + str(f_measure))