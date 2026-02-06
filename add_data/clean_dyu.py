from huggingface_hub import snapshot_download
from glob import glob
import os
import pandas as pd
import swifter

if __name__ == '__main__':
    local_dir = "../../Koumankan_mt_dyu_fr"
    if not os.path.exists(local_dir):
        folder = snapshot_download(
            "uvci/Koumankan_mt_dyu_fr",
            repo_type="dataset",
            local_dir=local_dir,
        )
    for file in glob(f"{local_dir}/data/*.parquet"):
        data = pd.read_parquet(file)
        data['dyula'] = data.translation.swifter.apply(lambda x: x['dyu'].lower())
        print(file)
    source = 'koumankanmtdyufr'
    out_file = f'../new_data/better_parquets/dyu_Latn_{source}.txt'
    oldata = pd.read_parquet(f'../data/dyu_Latn.parquet')
    old_texts_set = set()
    for text in oldata.text:
        old_texts_set.update(set(text.lower().split('\n')))
    with open(out_file, 'w') as out:
        for text in data.dyula:
            if text not in old_texts_set:
                out.write(text + '\n')
    command = f"cat {out_file} | awk '" + '{print $0"\tdyu_Latn\tkoumankanmtdyufr"}' + f"' > {out_file.replace('txt', 'tsv')}"
    os.system(command)
