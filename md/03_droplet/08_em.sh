#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --gres=gpu:4
#SBATCH --partition=c
#SBATCH --job-name=gmx_min
#SBATCH --output=out/gmx_min.out
source ./env
cd out
mpirun gmx_mpi mdrun -v -deffnm em
