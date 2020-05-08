#!/bin/sh

#SBATCH --ntasks=8
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00

module load Python/3.7.3-spartan_gcc-8.1.0

cd $HOME/project_d/comp90024/json_data_importer
time srun python json_data_importer.py twitter-melb.json
