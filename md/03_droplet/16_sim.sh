#!/bin/bash
source ./env
cd out
# -cpi/-cpo checkpoints
# -o exact trajectories
# -e energy log
# -g log file
gmx mdrun -s sim.tpr -cpi sim.cpt -cpo sim.cpt -o sim.trr -e sim.edr -g sim.log -c sim.gro -x sim.xtc
