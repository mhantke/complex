#!/bin/bash
#SBATCH --nodes=3
#SBATCH --nodelist=c003,c004,c005
#,c008,c009,c013
#SBATCH --ntasks-per-node=6
#SBATCH --partition=c
#SBATCH --exclusive
#SBATCH --gres=gpu:3
#SBATCH --exclude=c002,c012
#SBATCH --job-name=gmx_eq1
#SBATCH --output=out/gmx_eq1.out
#echo $HOSTNAME
#ulimit -c unlimited
# source environment
#source /home/hantke/local_intel/parallel_studio_xe_2016.2.062/compilers_and_libraries_2016/linux/mpi/bin64/mpivars.sh
#source /home/hantke/local_gromacs_intel/bin/GMXRC.bash
# go to output directory
#mpirun -iface ib0 gmx_mpi mdrun -deffnm nvt -pin on -ntomp 4 -gpu_id 001122
#mpirun -iface ib0 gmx_mpi mdrun -deffnm nvt -pin on -ntomp 4
#mpirun gmx_mpi mdrun -deffnm nvt
#gmx mdrun -deffnm nvt -pin on
source ./env
cd out/
export OMP_NUM_THREADS=4
mpirun gmx_mpi mdrun -deffnm npt -ntomp 4 -gpu_id 001122
