import os
from glob import glob
from pprint import pprint as print
from collections import defaultdict

import pandas as pd

if __name__ == '__main__':
    glotlid_corpus_path = "../../glotlid-corpus/v3.1"
    our_langs = set()
    with open("../new_data/clean/openlid_unsampled_cleaned.counts", 'r') as counts_file: # this file is produced by make_training_openlid
        for line in counts_file:
            our_langs.add(line.split('__label__')[-1].rstrip())
    langs_to_use = []
    for lang in os.listdir(glotlid_corpus_path):
        if lang not in our_langs:
            langs_to_use.append(lang)
    total = 1_000_000
    sample_from_language = total // len(langs_to_use)
    non_bible = defaultdict(list)
    unique_sources = set()
    flores_dev = set()
    for lang in our_langs:
        counter = 0
        sources = []
        for lang_path in glob(os.path.join(glotlid_corpus_path, lang, "*.txt")):
            if "floresdev" in lang_path:
                flores_dev.add(lang)
            if ('_cbc' not in lang_path) and ('_pbc' not in lang_path) and ('_jw' not in lang_path) and ('_bloombooks' not in lang_path) \
                    and ('ShaShiYaYi' not in lang_path) and ('_Bibles' not in lang_path) and ('_bhas' not in lang_path) and ('_wanca' not in lang_path) \
                    and ('IN22Conv' not in lang_path) and ('IN22Gen' not in lang_path) and ('JW300' not in lang_path) and ('americasnlp2024' not in lang_path) \
                    and ('_lti' not in lang_path) and ('mt560' not in lang_path) and ('yuecmnengparallel' not in lang_path):
                with open(lang_path, 'r') as lang_file:
                    counter += len(lang_file.readlines())
                    sources.append(os.path.basename(lang_path))
                    unique_sources.add(lang_path.split('_')[-1].rstrip())
        if counter:
            non_bible['lang'].append(lang)
            non_bible['samples'].append(counter)
            non_bible['sources'].append(', '.join(sources))
    print(len(flores_dev))
    print(unique_sources)
    non_bible = pd.DataFrame(non_bible)
    non_bible.sort_values(by='samples', inplace=True, ascending=False)
    print(non_bible.shape[0])
    #non_bible.to_csv('other.tsv', sep='\t', index=False)