from glob import glob

import pandas as pd

if __name__ == '__main__':
    # converting GlotLID to OpenLID format
    column_headers = ['text', 'language', 'source']
    for lang in (#'lat_Latn', 'srp_Latn', 'und_Zxxx',
            'zxx_Zxxx',
    ):
        df = pd.DataFrame(columns=column_headers)
        for file_path in glob(f"../new_data/{lang}*.txt"):
            print(file_path)
            print(f"current data length: {len(df)}")
            with open(file_path + '.tmp', 'w') as out:  # fixing tabs in source data
                with open(file_path, 'r') as f:
                    for line in f:
                        splitted_line = line.split('\t')
                        new_line = ' '.join(splitted_line[:-2]) + '\t' + '\t'.join(splitted_line[-2:])
                        out.write(new_line + '\n')
            new_data_tsv = pd.read_csv(
                file_path + '.tmp',
                sep="\t",
                header=None,
                names=column_headers,
            )
            print(f"new data length: {len(new_data_tsv)}")
            # combine and check
            df = pd.concat([df, new_data_tsv], ignore_index=True)
            print(f"combined data length: {len(df)}")
            print("combined data head and tail:")
            print(df.head())
            print(df.tail())
        out_parquet = f"{lang}.parquet"
        print(f"writing to {out_parquet}")
        df.to_parquet(out_parquet, compression="gzip")
