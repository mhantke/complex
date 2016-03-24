#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/env
OUTDIR=/scratch/fhgfs/hantke/complex/02_diffusion/
cd $OUTDIR
gmx rotacf -s out/npt.tpr -f /scratch/fhgfs/hantke/complex/02_diffusion/md.gro -n out/rotacf.ndx -o out/rotacf.xvg
# => t1/2 ~ 10 ns