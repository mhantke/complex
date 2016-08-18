#!/bin/bash
source ./env
cd out/
gmx mdrun -deffnm npt -v
