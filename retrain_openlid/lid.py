import argparse
import os

import fasttext

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', default="/scratch/project_465002259/eurolid/dzo-lij-bam/")
args = parser.parse_args()

model = fasttext.train_supervised(
    os.path.join(args.data_dir, "openlid_train_sampled_shuffled.fasttext"),
    minCount=1000, bucket=1000000,
    minn=2, maxn=5, lr=0.8, dim=256, epoch=2, thread=68, wordNgrams=1,
)
print(model.predict("lorem ipsum dolor sit amet"))
model.save_model(os.path.join(args.data_dir, "model.bin"))
