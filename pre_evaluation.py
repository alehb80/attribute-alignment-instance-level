import pandas as pd
from tqdm import tqdm
import json
from collections import defaultdict
import itertools

# Leggo la ground truth in un Pandas dataframe
df = pd.read_csv('instance_attributes_gt.csv')


# prendo tutti i positivi
pos_df = df[df['label'] == 1]

pos_df = pos_df.drop(columns=['left_target_attribute', 'right_target_attribute', 'left_instance_value', 'right_instance_value', 'label'])


# ordino lessicograficamente la GT
for index, row in tqdm(pos_df[pos_df['left_instance_attribute'] > pos_df['right_instance_attribute']].iterrows()):


    left_ia = row['left_instance_attribute']
    right_ia = row['right_instance_attribute']

    pos_df.at[index, 'left_instance_attribute'] = right_ia
    pos_df.at[index, 'right_instance_attribute'] = left_ia



pos_df.to_csv(f"sources_3/gt_onevalue.csv", sep=',',encoding='utf-8', index=False)

