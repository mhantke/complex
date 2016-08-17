#!/bin/bash
#SBATCH --nodes=2
#SBATCH --nodelist=c007,c010
#SBATCH --ntasks-per-node=1
#SBATCH --partition=c
#SBATCH --exclusive
#SBATCH --exclude=c002,c012
#SBATCH --job-name=pingpong
#SBATCH --output=pingpong.out
#Infiniband MPI test program
#Edit the hosts below to match your test hosts
cat > /tmp/hostfile.$$.mpi <<EOF
c007 slots=1
c010 slots=1
EOF
mpirun --mca btl_openib_verbose 1 --mca btl ^tcp -n 2 -hostfile /tmp/hostfile.$$.mpi /usr/lib64/openmpi/bin/mpitests-IMB-MPI1 PingPong
