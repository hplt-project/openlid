from glob import glob
import os

from alphabet_detector import AlphabetDetector
import pandas as pd
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('new_data_path')
    parser.add_argument('old_data_path')
    parser.add_argument('--iso', default='lij_Latn')
    parser.add_argument('--script', default='LATIN')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    ad = AlphabetDetector()
    oldata = pd.read_parquet(os.path.join(args.old_data_path, f'{args.iso}.parquet'))
    old_texts_set = set()
    for text in oldata.text:
        old_texts_set.update(set(text.lower().split('\n')))
    out_file = os.path.join(args.new_data_path, f'{args.iso}_wiki.txt')
    to_write = set()

    for path in glob(os.path.join(args.new_data_path, f'{args.iso}/AA/wiki*')):
        print(path)
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and ('<' not in line) and (args.script in ad.detect_alphabet(line)):
                    text = line.lower().rstrip()
                    if ('_Latn' in args.iso) and (len(line.split())>1) or ('_Latn' not in args.iso):  # get rid of "hawaii"
                        if text not in old_texts_set:
                            to_write.add(text.replace(' ', ' ').replace('	', ' '))
    with open(out_file, 'w') as out:
        out.write('\n'.join(to_write))
    command = f"cat {out_file} | awk '" + "{print $0" + f'"\t{args.iso}\twiki"' + '}' + f"' > {out_file.replace('txt', 'tsv')}"
    os.system(command)
