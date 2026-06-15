import argparse
from huggingface_hub import upload_folder

parser = argparse.ArgumentParser()
parser.add_argument("data_dir")
args = parser.parse_args()

# Upload the local directory to your dataset repository
upload_folder(
    folder_path=args.data_dir,
    repo_id="HPLT/OpenLID-v3",
    repo_type="dataset",
    path_in_repo="data/",  # Optional: Dest folder in repo. Omit to upload to root.
    commit_message="Upload dataset folder using huggingface_hub"
)
# if using push_to_hub, splitting by language is not preserved
