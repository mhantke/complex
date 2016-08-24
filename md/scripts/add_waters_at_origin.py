#!/usr/bin/env python
import numpy as np
import argparse, sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cut spherical droplet in .gro file')
    parser.add_argument('-s', '--input', metavar='gro.gro', type=str, help="gromacs file", nargs='?', const=True, required=True)
    parser.add_argument('-o', '--output', metavar='gro.gro', type=str, help="gromacs file", nargs='?', const=True, required=True)
    parser.add_argument("-n", '--n_water', type=int, help="number of water molecules to be added", required=True) 
    if(len(sys.argv) == 1):
        parser.print_help()
        exit(0)
    args = parser.parse_args()

    with open(args.input, "r") as f:
        lines0 = f.readlines()
        
    lines_water = ["%5d%-5s%5s%5d%8.3f%8.3f%8.3f%8.4f%8.4f%8.4f\n" % (1, "SOL", "OW1", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                   "%5d%-5s%5s%5d%8.3f%8.3f%8.3f%8.4f%8.4f%8.4f\n" % (1, "SOL", "HW2", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                   "%5d%-5s%5s%5d%8.3f%8.3f%8.3f%8.4f%8.4f%8.4f\n" % (1, "SOL", "HW3", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

    lines1 = lines0[:-1] + lines_water * args.n_water + [lines0[-1]]
    
    with open(args.output, "w") as f:
        f.writelines(lines1)
        
