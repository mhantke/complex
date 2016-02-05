#!/bin/bash
#
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=6
#SBATCH --gres=gpu:3
#SBATCH --job-name=gmx_sim
#SBATCH --output=out/gmx_sim.out
source env
cd out/
mpirun gmx_mpi mdrun -deffnm md_0_1
