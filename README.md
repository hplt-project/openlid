<p align="center"><img width="320" src="https://github.com/laurieburchell/open-lid-dataset/blob/0cbea4aca70677333da1d7d63babeaab538d7e56/openlid-logo.png" alt="OpenLID - fast natural language identification for 200+ languages"></p>

# OpenLID-v3

Fast natural language identification for 184 languages, plus (almost) all the data to train the model (work in progress).

> [!NOTE]
> The previous version -- OpenLID-v2 model and dataset is available on HuggingFace: [OpenLID-v2](https://huggingface.co/datasets/laurievb/OpenLID-v2)

## Features

 - Supports 184 languages
 - High performance
 - Fast and easy to use
 - Fully transparent: training data and per-language performance openly available
 - Used by [HPLT](https://hplt-project.org/)

## Updates compared to OpenLID-v2

- frp_Latn, lat_Latn, srp_Latn classes added
- not-a-language class zxx_Zxxx added
- dyu_Latn class merged with bam_Latn class (the classes are not distinguishable with this type of model trained on the data we were able to obtain)
- for the same reason, Arabic dialects merged into the macrolanguage ara_Arab; pes_Arab and prs_Arab merged into the macrolanguage fas_Arab
- pilar data for oci_Latn class not used (caused false positives)
- for some languages, training data from [glotlid-corpus](https://huggingface.co/datasets/cis-lmu/glotlid-corpus) and Wikipedia added

## Get started

OpenLID is a [fastText](https://fasttext.cc/docs/en/support.html) model.

To download:

```shell
wget https://zenodo.org/records/17601701/files/openlid-v3.bin
```

Example to get most likely labels for $DATA:

```shell
fasttext predict openlid-v3.bin $DATA > output.fasttext

```

## Dataset

work in progress

### Adding GlotLID data

`cd add_data/glotlid`

For v3, we used glotlid-corpus data for several languages.
It is also possible download them using the script `download_glotlid.py`.

`make_list_of_glotlid_sources.py` creates the list of GlotLID sources for each language and shows number of samples in GlotLID data.
There is no need to run it, since the resulting list is in `other.tsv` in the root of this repository.

The script `add_from_glotlid.py` shows how to select only the data sources that are of reliable quality and not proprietary. (Beware of hardcoded paths...)
The list of filters there is also for the languages we worked with before;
for Scandinavian etc., if there are some other sources, check their quality and license according to [GlotLID list](https://github.com/cisnlp/GlotLID/blob/main/sources.md).
We also collected licenses of the sources we used [here](https://docs.google.com/spreadsheets/d/162EzUGXDllmujoNG5s_XngSlL4awOJ9F79t5k2OM_FQ/edit?gid=737547198#gid=737547198) at LangID sources sheet.

That script also ensures that wikipedia GlotLID data do not intersect with OpenLID wikipedia data.

### Adding Wikipedia data

We also used the most recent (at the fall 2025) Wikipedia data for some languages in v3.

`cd add_data/wikipedia`

## Training

`cd retrain_openlid`

This folder contains mostly OpenLID author's scripts with minor changes. The current cleaning is language-independent.

### OpenLID pipeline

Following [OpenLID's instructions](https://huggingface.co/datasets/laurievb/OpenLID-v2/blob/main/how_to_update.md) (be cautious, they were not fully up-to-date),  the pipeline is as follows:

1. Find additional data and format by the scheme `<text>\t<language>\t<source>`. If it is an addition to an existing language, it can be appended to it either from a *.parquet or *.tsv using the script `append_to_openlid_parquet.py`.
If the data are for a new language, just convert to a parquet.

2. Data for all languages must be in the same directory.

3. Cleaning, deduplication, up/downsampling, writing to FastText format and shuffling are done by `make_training_openlid.py`. I was able to run that script on my laptop with only 16 GB of memory, except shuffling. If you fail on memory when shuffling, run `shuf.sh` on LUMI.

When running from scratch, the command is

```commandline
python3 make_training_openlid.py <output_dir> --data_dir <data_dir>
```

If the output of stage 2 from `make_training_openlid.py`, named openlid_stage2_prep.fasttext,  is in <data_dir> directory  and contains only languages of interest, 
the command to run preprocessing will be:

```commandline
python3 make_training_openlid.py <output_dir> --skip_clean --skip_sort
```

4. The training on LUMI is run by `lid.sh`. Don't forget to pass a new path to data/saved model instead of the default one. The hyperparameters are the same as in OpenLID-v2.


## Citations

If you use our model, please [cite us](https://aclanthology.org/2023.acl-short.75). If you use the dataset, please cite us plus all the articles in the `citations.bib` file. Thank you to everyone who put in so much work creating these datasets! 


## Licenses

The model is licensed under the [GNU General Public License v3.0](LICENSE). The individual datasets that make up the training dataset have different licenses but all allow (at minimum) free use for research - [a full list](licenses.md) is available in this repo.


---------------------------------------------------------------------------------------------

<sub><sup>This project has received funding from the European Union’s Horizon Europe research and innovation programme under grant agreement No 101070350 and from UK Research and Innovation (UKRI) under the UK government’s Horizon Europe funding guarantee [grant number 10052546].
The contents of this publication are the sole responsibility of the HPLT consortium and do not necessarily reflect the opinion of the European Union.</sup></sub>