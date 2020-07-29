import pandas as pd
from tqdm import tqdm
import json
from collections import defaultdict
import itertools
import CommonUtilities

# Leggo la ground truth in un Pandas dataframe
pos_df = pd.read_csv('sources_3/gt_onevalue.csv')

attrNameSet = set()

# ordino lessicograficamente la GT
for index, row in pos_df.iterrows():


    left_ia = row['left_instance_attribute']
    right_ia = row['right_instance_attribute']

    attrNameSet.add(left_ia.split("//")[2])
    attrNameSet.add(right_ia.split("//")[2])

    CommonUtilities.progressBar(index+1, pos_df.shape[0], f"{index+1}/{pos_df.shape[0]}")


with open("attrToAnalize.txt", "w") as attrFile:
    for attr in sorted(list(attrNameSet)):
        attrFile.write(f"{attr}\n")


