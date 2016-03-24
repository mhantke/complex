#!/bin/bash
#
#SBATCH --nodes=16
#SBATCH --ntasks-per-node=6
#SBATCH --gres=gpu:3
#SBATCH --job-name=gmx_sim
#SBATCH -p low
#SBATCH --output=out/gmx_sim.out
source env
cd out/
OUTDIR=/scratch/fhgfs/hantke/complex/02_diffusion/
# -cpi/-cpo checkpoints
# -o exact trajectories
# -e energy log
# -g log file
mpirun gmx_mpi mdrun -s ./md_0_1.tpr -cpi $OUTDIR/md.cpt -cpo $OUTDIR/md.cpt -o $OUTDIR/md.trr -e $OUTDIR/md.edr -g $OUTDIR/md.log -c $OUTDIR/md.gro -x $OUTDIR/md.xtc
