# appends a cleaned tsv of new data in the OpenLID format to the existing parquet file
# author: laurie

import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("existing_parquet", help="Parquet file of existing OpenLID data")
parser.add_argument("new_tsv", help="TSV of new OpenLID data")
parser.add_argument("out_parquet", help="path to write combined parquet file")
parser.add_argument("lang")
args = parser.parse_args()

# open files
current_data_pq = pd.read_parquet(args.existing_parquet)
print(f"current data length: {len(current_data_pq)}")
if '.parquet' in args.new_tsv:
    new_data_tsv = pd.read_parquet(args.new_tsv)
else:
    new_data_tsv = pd.read_csv(
        args.new_tsv,
        sep="\t",
        header=None,
        names=['text', 'language', 'source'],
    )
print(f"new data length: {len(new_data_tsv)}")

# combine and check
combined_df = pd.concat([current_data_pq, new_data_tsv], ignore_index=True)
combined_df["language"] = [args.lang for _ in range(combined_df.shape[0])]
print(f"combined data length: {len(combined_df)}")
print("combined data head and tail:")
print(combined_df.head())
print(combined_df.tail())
print(f"writing to {args.out_parquet}")
combined_df.to_parquet(args.out_parquet, compression="gzip")
