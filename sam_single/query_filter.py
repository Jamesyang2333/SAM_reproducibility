import numpy as np
import pandas as pd
import json
from operator import itemgetter
import argparse

import datasets
import common
from data_loader import load_dataset
from evaluate import Query
from utils import get_qerror

parser = argparse.ArgumentParser()
parser.add_argument('--coverage-ratio', type=str, default='0.8', help='Coverage ratio of the query workload')

args = parser.parse_args()

train_data_raw = load_dataset("census", "./queries/census_train.txt")

start_idx = 0
test_num = 20000

sample_table = datasets.LoadCensus()

idx_filter = []
str_col = [1, 3, 5, 6, 7, 8, 9, 13, 14]
ratio = float(args.coverage_ratio)

for i in range(start_idx, start_idx + test_num):
    if i % 1000 == 0:
        print(i)
    inRange = True
    columns = [sample_table.columns[sample_table.ColumnIndex(col)] for col in train_data_raw['column'][i]]
    cols = train_data_raw['column'][i]
    ops = train_data_raw['operator'][i]
    vals = train_data_raw['val'][i]
    for j in range(len(cols)):
        v = np.array(vals[j]).astype(columns[j].data.dtype)
        if v > columns[j].all_distinct_values[int(ratio * columns[j].distribution_size)]:
            inRange = False
    if inRange:
        # query = "SELECT COUNT(*) FROM dmv WHERE "
        # for j in range(len(cols)):
        #     # col_name = "_".join(cols[i].split(" "))
        #     col_name = "c" + str(cols[j])
        #     if cols[i] in str_col:
        #         query += (col_name + ops[j] + "'" + vals[j] + "'")
        #     else:
        #         query += (col_name + ops[j] + vals[j])
        #     if j != len(cols) - 1:
        #         query += " AND "
        #     else:
        #         query += ";\n"
        idx_filter.append(i)
        if len(idx_filter) == 20000:
            print("Checked a total of {} queries".format(i))
            break

data = {}
data['query_list'] = []
data['card_list'] = []
file_name = './queries/census_100000.txt'
with open(file_name, 'r', encoding="utf8") as f:
    workload_stats = json.load(f)
    data['query_list'] = itemgetter(*idx_filter)(workload_stats['query_list'])
    data['card_list'] = itemgetter(*idx_filter)(workload_stats['card_list'])

output_file = "./queries/census_filter_{}_20000.csv".format(ratio)
with open(output_file, 'w') as f:
    json.dump(data, f)

