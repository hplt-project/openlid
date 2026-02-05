#!/bin/bash

#SBATCH --job-name=shuf
#SBATCH --account=project_465002259
#SBATCH --time=00:30:00
#SBATCH --mem-per-cpu=25G
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=small

set -o errexit  # Exit the script on any error
set -o nounset  # Treat any unset variables as an error

IN=${1}  # openlid_stage3_prep.fasttext
OUT=${2} # openlid_train_sampled_shuffled.fasttext

shuf -o $OUT $IN
