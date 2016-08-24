#!/usr/bin/env python
import numpy as np
import argparse, sys
import gmx_tools.gro

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count atoms in structure of .gro file')
    parser.add_argument('-s', '--input', metavar='box.gro', type=str, help="gromacs file", nargs='?', const=True, required=True)
    parser.add_argument('-n', '--name', metavar='SOL', type=str, help="name of structure of which atoms shall be counted (e.g. SOL)", nargs='?', const=True, required=True)
    if(len(sys.argv) == 1):
        parser.print_help()
        exit(0)
    args = parser.parse_args()

    # Read positions
    m0,x0,y0,z0 = gmx_tools.gro.get_positions(args.input, name=args.name)

    # Print number of atoms
    print len(m0)
