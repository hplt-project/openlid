from glob import glob
import pandas as pd
from tqdm import tqdm
from retrain_openlid.tools import openlid_normer as norm
import csv
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_dir', default='~/PycharmProjects/OpenLID-v2/new_data/oci_no_pilar_glotlid/')
    parser.add_argument('--out', default='~/PycharmProjects/OpenLID-v2/new_data/oci_no_pilar_glotlid/oci_glotlid_frp.txt')
    return parser.parse_args()


def clean_and_write_out(indata, f):
    """clean and write out iterable of OpenLID format to FastText format"""
    for line in tqdm(data.iterrows(), desc="cleaning and converting to fasttext format"):
        line = line[1]
        try:
            prepped_text = norm.clean_line(line[0])
            if len(prepped_text.split()) > 2:
                ft_line = f"__label__{line[1]} {prepped_text}\n"
                f.write(ft_line)
        except Exception as e:
            print(f"Error '{e}' on line (skipped): {line[0]}")


if __name__ == '__main__':
    args = parse_args()
    with open(os.path.expanduser(args.out), 'w') as f:
        for tsv in glob(f'{os.path.expanduser(args.in_dir)}/*.tsv'):
            print(tsv, flush=True)
            data = pd.read_csv(tsv, sep='\t', header=None, quoting=csv.QUOTE_NONE, on_bad_lines='warn')
            clean_and_write_out(data, f)
