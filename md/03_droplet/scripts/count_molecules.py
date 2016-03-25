#!/usr/bin/env python
import numpy as np
import argparse, sys
import gmx_tools.gro

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count molecules in structure of .gro file')
    parser.add_argument('-s', '--input', metavar='box.gro', type=str, help="gromacs file", nargs='?', const=True, required=True)
    parser.add_argument('-n', '--name', metavar='SOL', type=str, help="name of molecule type of which atoms shall be counted (e.g. SOL)", nargs='?', const=True, required=True)
    if(len(sys.argv) == 1):
        parser.print_help()
        exit(0)
    args = parser.parse_args()

    # Read positions
    m,x,y,z = gmx_tools.gro.get_positions(args.input, name=args.name)

    # Print number of molecules
    N = 0
    temp = -1
    for mi in m:
        if mi != temp:
            N+=1
        temp = mi

    print N
