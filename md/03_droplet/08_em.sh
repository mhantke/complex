#!/bin/bash
#SBATCH --nodes=10
#SBATCH --nodelist=c003,c004,c005,c007,c008,c009,c010,c011,c013,c014
#SBATCH --ntasks-per-node=6
#SBATCH --gres=gpu:3
#SBATCH --exclusive
#SBATCH --partition=c
#SBATCH --exclude=c002,c012
#SBATCH --job-name=gmx_min
#SBATCH --output=out/gmx_min.out
source ./env
cd out
export OMP_NUM_THREADS=4
mpirun gmx_mpi mdrun -v -deffnm em -pin on -ntomp 4 -gpu_id 001122
