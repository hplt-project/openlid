from huggingface_hub import snapshot_download

folder = snapshot_download(
    "cis-lmu/glotlid-corpus",
    repo_type="dataset",
    local_dir="../../glotlid-corpus/v3.1",
    # Replace "v3.1/bal_Arab/*" with the path for another language available in the dataset
    allow_patterns="zxx/*",
)
