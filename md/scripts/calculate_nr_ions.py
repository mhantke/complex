#!/usr/bin/env python
import numpy as np
import argparse, sys
from scipy import constants
import gmx_tools.gro

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate required number of NaCl to obtain desired concentration (assuming 216SPC water model)')
    parser.add_argument('-s', '--input', metavar='drop.gro', type=str, help="gromacs file", nargs='?', const=True, required=True)
    parser.add_argument('-c', '--conc_molar', metavar='conc_molar', type=float, help="desired NaCl concentration in mol/l (default is physiological)", nargs='?', const=True, default=0.154)
    if(len(sys.argv) == 1):
        parser.print_help()
        exit(0)
    args = parser.parse_args()

    # Read positions
    m0,x0,y0,z0 = gmx_tools.gro.get_positions(args.input, name="SOL")
    
    # Count number of water atoms
    Na = len(m0)
    # Derive number of water molecules
    Nw = Na/3
    assert Nw*3 == Na

    # Convert concentration to particles/m^3
    c = args.conc_molar * constants.N_A / (0.1)**3

    # Volume of 216 SPC water
    V216 = (1.86206E-9)**3
    # Volume per water molecule,
    Vw = V216 / 216.
    # Volume of all water
    V = Vw * Nw
    
    # Calculate number of NaCl required
    N = c * V
    # Round to integer
    N = int(round(N))
    
    print N
