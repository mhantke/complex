#!/bin/bash
#
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=6
#SBATCH --gres=gpu:3
#SBATCH --job-name=gmx_eq1
#SBATCH --output=out/gmx_eq1.out
source env
cd out/
mpirun gmx_mpi mdrun -deffnm nvt
