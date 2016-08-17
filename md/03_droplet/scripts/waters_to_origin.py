#!/usr/bin/env python
import numpy as np
import argparse, sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Move waters to position')
    parser.add_argument('-s', '--input', metavar='gro.gro', type=str, help="gromacs file", nargs='?', const=True, required=True)
    parser.add_argument('-o', '--output', metavar='gro.gro', type=str, help="gromacs file", nargs='?', const=True, required=True)
    parser.add_argument("-x", '--x_pos', type=float, help="x pos", required=True)
    parser.add_argument("-y", '--y_pos', type=float, help="y pos", required=True)
    parser.add_argument("-z", '--z_pos', type=float, help="z pos", required=True) 
    if(len(sys.argv) == 1):
        parser.print_help()
        exit(0)
    args = parser.parse_args()

    with open(args.input, "r") as f:
        lines = f.readlines()

    s = "%8.3f%8.3f%8.3f\n" % (args.x_pos, args.y_pos, args.z_pos)
    for i,l in enumerate(lines):
        if "SOL" == l[5:5+3]:
            lines[i] = "%s%s" % (l[:20],s)
        
    with open(args.output, "w") as f:
        f.writelines(lines)
        
