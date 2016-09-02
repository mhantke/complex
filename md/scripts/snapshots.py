#!/usr/bin/env python
import os
import numpy as np
import argparse, sys
import gmx_tools.xvg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract snapshots from XTC file')
    parser.add_argument('-f', '--trr-filename', type=str, help="xtc file ", required=True)
    #parser.add_argument('-f', '--xtc-filename', type=str, help="xtc file ", required=True)
    parser.add_argument('-s', '--tpr-filename', type=str, help="tpr file ", required=True)
    parser.add_argument('-x', '--xvg-filename', type=str, help="xvg file with positions (typically \'pullx.xvg\')", required=True)
    parser.add_argument('-n', '--number-of-steps', type=int, help="number of steps to sample", required=True)
    parser.add_argument('-d', '--max-distance-nm', type=float, help="maximum distance in unit nanometer", required=True)
    if(len(sys.argv) == 1):
        parser.print_help()
        exit(0)
    args = parser.parse_args()

    [time, xcom, xset] = gmx_tools.xvg.read_xvg(args.xvg_filename, ncols=3)
    
    x_grid = np.linspace(0, args.max_distance_nm, args.number_of_steps)
    t_grid = np.interp(x_grid, xcom, time)

    for x,t in zip(x_grid, t_grid):
        os.system("source ./env; echo 0 | gmx trjconv -dump %f -f %s -s %s -o snap_%.2fnm.gro" % (t, args.trr_filename, args.tpr_filename, x))
