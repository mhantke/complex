#!/usr/bin/env python
import numpy as np
import argparse, sys
from scipy import constants
import gmx_tools.gro
import gmx_tools.top

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove water molecules at the end of .gro file')
    parser.add_argument('-s', '--input', metavar='box.gro', type=str, help="input gromacs file", nargs='?', const=True, required=True)
    parser.add_argument('-p', '--topol', metavar='topol.top', type=str, help="gromacs topology file", nargs='?', const=True, required=True)
    parser.add_argument('-o', '--output', metavar='drop.gro', type=str, help="output gromacs file", nargs='?', const=True, required=True)
    parser.add_argument('-n', '--remove_nr_molecules', metavar='n', type=int, help="number of molecules to be removed", nargs='?', const=True, required=True)
    if(len(sys.argv) == 1):
        parser.print_help()
        exit(0)
    args = parser.parse_args()

    # Read gro input
    line_header, line_nr_atoms, lines_atoms, line_edge_lengths = gmx_tools.gro.read_gro(args.input)
    N_at = len(lines_atoms) - args.remove_nr_molecules * 3
    line_nr_atoms = "%i\n" %  N_at
    lines_atoms = lines_atoms[:N_at]
    # Write gro output
    gmx_tools.gro.write_gro(args.output, line_header, line_nr_atoms, lines_atoms, line_edge_lengths)
    # Modify topology
    i,x,y,z = gmx_tools.gro.get_positions(args.output, name="SOL")
    N_at_sol = len(i)
    N_mol_sol = N_at_sol/3
    assert N_mol_sol*3 == N_at_sol
    gmx_tools.top.set_nr_mol(args.topol, "SOL", N_mol_sol)
    
    
