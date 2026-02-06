import argparse
import os
import pandas as pd
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--first', default='frp')
parser.add_argument('--second', default='oci')

args = parser.parse_args()
pq = os.path.expanduser(f"~/PycharmProjects/OpenLID-v2/data/{args.first}_Latn.parquet")


new_data = pd.read_parquet(pq)
for source in new_data.source.unique():
    print(source)

