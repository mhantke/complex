#!/bin/bash
source ./env
cd out
gmx mdrun -v -deffnm em
