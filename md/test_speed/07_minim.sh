#!/bin/bash
#
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=6
#SBATCH --gres=gpu:3
#SBATCH --job-name=gmx_min
#SBATCH --output=out/gmx_min.out
source env
cd out
mpirun gmx_mpi mdrun -v -deffnm em

