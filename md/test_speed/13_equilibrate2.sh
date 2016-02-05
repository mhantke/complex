#!/bin/bash
#
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=6
#SBATCH --gres=gpu:3
#SBATCH --job-name=gmx_eq2
#SBATCH --output=out/gmx_eq2.out
source env
cd out/
mpirun gmx_mpi mdrun -deffnm npt
