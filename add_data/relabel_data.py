from tqdm import tqdm
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='openlid_stage1_prep.fasttext')
    parser.add_argument('--in_folder', default="~/PycharmProjects/OpenLID-v2/new_data/bod_lij_new_wiki")
    parser.add_argument('--out_folder', default="~/PycharmProjects/OpenLID-v2/new_data/bam")
    parser.add_argument('--labels_to_replace', default="dyu_Latn")
    parser.add_argument('--replace_with', default="bam_Latn")
    return parser.parse_args()


def replace_label(line, in_, out):
    if line.startswith(f'__label__{in_}'):
        line = line.replace(in_, out)
    return line


if __name__ == '__main__':
    args = parse_args()
    args.in_folder = os.path.expanduser(args.in_folder)
    args.out_folder = os.path.expanduser(args.out_folder)
    os.makedirs(args.out_folder, exist_ok=True)
    langs = args.labels_to_replace.split(',')
    with open(f'{args.in_folder}/{args.file}', 'r') as fin, open(f'{args.out_folder}/{args.file}', 'w') as fout:
        for line in tqdm(fin):
            for lang in langs:
                line = replace_label(line, lang, args.replace_with)
            fout.write(line)
