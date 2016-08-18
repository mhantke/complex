#!/bin/bash
source ./env
cd out
gmx mdrun -deffnm nvt -v 
