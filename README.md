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

## Training

[Instructions on training](https://github.com/hplt-project/mtm25-langid?tab=readme-ov-file#retraining-openlid-with-all-the-new-data-and-changes) (work in progress)

## Citations

If you use our model, please [cite us](https://aclanthology.org/2023.acl-short.75). If you use the dataset, please cite us plus all the articles in the `citations.bib` file. Thank you to everyone who put in so much work creating these datasets! 


## Licenses

The model is licensed under the [GNU General Public License v3.0](LICENSE). The individual datasets that make up the training dataset have different licenses but all allow (at minimum) free use for research - [a full list](licenses.md) is available in this repo.


---------------------------------------------------------------------------------------------

<sub><sup>This project has received funding from the European Union’s Horizon Europe research and innovation programme under grant agreement No 101070350 and from UK Research and Innovation (UKRI) under the UK government’s Horizon Europe funding guarantee [grant number 10052546].
The contents of this publication are the sole responsibility of the HPLT consortium and do not necessarily reflect the opinion of the European Union.</sup></sub>