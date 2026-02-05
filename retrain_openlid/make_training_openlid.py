import logging
import os
import time
from tqdm import tqdm
from datasets import load_dataset
from tools import openlid_normer as norm
import argparse
import random


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    filename=f'{time.ctime().replace(" ", "_")}.log'
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="directory to write output files")
    parser.add_argument("-c", "--parquet_to_clean",
                        help="run clean only on specified parquet OpenLID file (output $FILE.clean.ft)")
    parser.add_argument("--skip_clean",
                        help="skip step one and start with sort/uniq", action="store_true")
    parser.add_argument("--data_dir", default="../data/", help="directory with *.parquet files by language")
    parser.add_argument("--skip_sort", action="store_true", help="skip sort and start with sampling")
    return parser.parse_args()


args = parse_args()

if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

# path names
stage1_path = os.path.join(args.output_dir,
                           'openlid_stage1_prep.fasttext')  # unsampled, unsorted
stage2_path = os.path.join(args.output_dir,
                           'openlid_stage2_prep.fasttext')  # unsampled, sorted
stage3_path = os.path.join(args.output_dir,
                           'openlid_stage3_prep.fasttext')  # sampled, unshuffled
counts_path = os.path.join(args.output_dir,
                           'openlid_unsampled_cleaned.counts')
stage4_path = os.path.join(args.output_dir,
                           'openlid_train_sampled_shuffled.fasttext')  # ready for training


def clean_and_write_out(indata, outfile):
    """clean and write out iterable of OpenLID format to FastText format"""
    with open(outfile, 'w') as f:
        for line in tqdm(indata, desc="cleaning and converting to fasttext format"):
            try:
                prepped_text = norm.clean_line(line['text'])
                if len(prepped_text) > 3:
                    ft_line = f"__label__{line['language']} {prepped_text}\n"
                    f.write(ft_line)
            except Exception as e:
                logging.info(f"Error '{e}' on line (skipped): {line}")


# clean specified OpenLID file only
if args.parquet_to_clean:
    logging.info(f"cleaning {args.parquet_to_clean}")
    ds = load_dataset("parquet", data_files=args.parquet_to_clean, split="train")
    outfile = os.path.join(args.output_dir,
        f"{os.path.basename(args.parquet_to_clean)}.cleaned.fasttext")
    clean_and_write_out(ds, outfile)
    logging.info(f"wrote stage 1 clean results to {outfile}")
    exit(0)


if not args.skip_clean:
    # load dataset (will cache in $HOME/.cache/huggingface
    #ds = load_dataset('laurievb/OpenLID-v2', split='train')
    ds = load_dataset("parquet", data_dir=args.data_dir, split='train')
    logging.info(ds[0])
    clean_and_write_out(ds, stage1_path)

    # # convert to fasttext format
    # with open(stage1_path, 'w') as f:
    #     for line in tqdm(ds, desc="cleaning and converting to fasttext format"):
    #         try:
    #             prepped_text = norm.clean_line(line['text'])
    #             if len(prepped_text) > 3:
    #                 ft_line = f"__label__{line['language']} {prepped_text}\n"
    #                 f.write(ft_line)
    #         except Exception as e:
    #             logging.info(f"Error '{e}' on line (skipped): {line}")


if not args.skip_sort:
    # sort, uniq (with shell for speed)
    logging.info(f"sort and uniq...")
    os.system(f"sort -u -o {stage2_path} --parallel=16 {stage1_path}")

# count lines and sample with temperature
logging.info("generating counts...")
os.system(f"cut -f1 -d' ' {stage2_path} | uniq -c > {counts_path}")
logging.info("generating counts lookup dict...")
with open(counts_path) as fr:
    total_raw_lines = 0
    lc_lookup = dict()
    for line in fr:
        count, lang = line.strip().split(' ')
        count = int(count)
        lc_lookup[lang] = {"raw_lines": count}
        total_raw_lines += count
logging.info(f"lookup dict finished ({len(lc_lookup)} entries)")
logging.info(f"dataset contains {total_raw_lines} lines")

logging.info("calculating sampling factors")
total_sampling_factors = 0
for lang in lc_lookup:
    # sample lines proportional to factor so smaller langs are upsampled and larger langs are downsampled
    sampling_factor = (lc_lookup[lang]['raw_lines'] / total_raw_lines) ** 0.3
    lc_lookup[lang]["sampling_factor"] = sampling_factor
    total_sampling_factors += sampling_factor

logging.info(f"sampling factor total is {total_sampling_factors}")
logging.info(f"calculating number of lines to sample")
total_lines_to_sample = 0
for lang in lc_lookup:
    lines_to_sample = round(
        lc_lookup[lang]["sampling_factor"] / total_sampling_factors * total_raw_lines)
    lc_lookup[lang]['lines_to_sample'] = lines_to_sample
    total_lines_to_sample += lines_to_sample
prop_size_difference = abs((total_raw_lines - total_lines_to_sample) / total_lines_to_sample)
assert prop_size_difference < 0.01  # sense check that sampled corpus is right size
logging.info(
    f"total raw lines: {total_raw_lines}, "
    f"total sampled lines: {total_lines_to_sample} "
    f"({prop_size_difference:.3%} difference)"
)


def write_out_language(lang_store, lc_lookup, langcode, f):
    """samples language according to lc_lookup and writes to outfile"""
    raw_lines_in_lang = lc_lookup[langcode]["raw_lines"]
    num_lines_to_keep = lc_lookup[langcode]["lines_to_sample"]
    logging.info(f"finished reading {langcode}: "
          f"read in {raw_lines_in_lang}, "
          f"writing {num_lines_to_keep}"
          )
    if raw_lines_in_lang > num_lines_to_keep:
        sampled_lines_gc = (x for x in random.sample(lang_store, num_lines_to_keep))
    else:  # need to oversample, so now use sampling with replacement
        sampled_lines_gc = (x for x in random.choices(lang_store, k=num_lines_to_keep))
    for out in sampled_lines_gc:
        f.write(f"{out}\n")

# assume input file is sorted by group
logging.info(f"sampling data in {stage2_path}")
with open(stage2_path, "r") as fr, open(stage3_path, "w") as fw:
    lang_store = []
    langcode = ""
    while line := fr.readline():
        line = line.strip()
        try:
            nextlang, _ = line.split(' ', 1)
        except ValueError as e:
            logging.info(f"{e} on line {line}")
            continue
        if langcode == nextlang or langcode == "":  # same language
            lang_store.append(line)
        else:  # language change, time to sample and write out
            write_out_language(lang_store, lc_lookup, langcode, fw)
            lang_store = [line]
        langcode = nextlang
    # output final language
    nextlang = "<finished>"
    write_out_language(lang_store, lc_lookup, langcode, fw)
logging.info("sampling complete!")

# friends don't let friends forget to shuffle before training
logging.info("shuffling sampled data...")
os.system(f"shuf -o {stage4_path} {stage3_path}")
logging.info("training data ready!")



