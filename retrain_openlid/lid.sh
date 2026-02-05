#!/bin/bash

#SBATCH --job-name=lid
#SBATCH --account=project_465002259
#SBATCH --time=4:00:00
#SBATCH --mem-per-cpu=1750
#SBATCH --cpus-per-task=68 # threads, see https://docs.lumi-supercomputer.eu/runjobs/scheduled-jobs/lumic-job/
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 # One task (process)
#SBATCH --partition=small

set -o errexit  # Exit the script on any error
set -o nounset  # Treat any unset variables as an error


export EBU_USER_PREFIX=/projappl/project_465002310/software

module --quiet purge
module load LUMI
module load PyTorch/2.6.0-rocm-6.2.4-python-3.12-singularity-20250404

srun singularity exec $SIF python3 lid.py  ${@}
