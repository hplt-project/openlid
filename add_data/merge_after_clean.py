import argparse
import os

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--in_folder', default="~/PycharmProjects/OpenLID-v2/new_data/final")
parser.add_argument('--out_folder', default="~/PycharmProjects/OpenLID-v2/new_data/bod_lij_new_wiki")
parser.add_argument('--clean_data_to_add', default="~/PycharmProjects/OpenLID-v2/new_data/lij_bod.txt")
args = parser.parse_args()

args.in_folder = os.path.expanduser(args.in_folder)
args.out_folder = os.path.expanduser(args.out_folder)
args.clean_data_to_add = os.path.expanduser(args.clean_data_to_add)

if not os.path.exists(args.out_folder):
    os.makedirs(args.out_folder, exist_ok=True)
with open(f'{args.in_folder}/openlid_stage1_prep.fasttext', 'r') as f1, open(args.clean_data_to_add, 'r') as f2:
    with open(f'{args.out_folder}/openlid_stage1_prep.fasttext', 'w') as f3:
        for line in tqdm(f1):
            f3.write(line)
        for line in tqdm(f2):
            f3.write(line)
