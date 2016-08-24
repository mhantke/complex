#!/usr/bin/env python
import numpy as np
import argparse, sys
import gmx_tools.gro

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cut spherical droplet in .gro file')
    parser.add_argument('-s', '--input', metavar='box.gro', type=str, help="gromacs file: box filled with water", nargs='?', const=True, required=True)
    parser.add_argument('-o', '--output', metavar='droplet.gro', type=str, help="gromacs file: droplet filled with water", nargs='?', const=True, required=True)
    parser.add_argument('-p', '--topol', metavar='topol.top', type=str, help="gromacs topology file that shall be updated", nargs='?', const=True, required=True)
    parser.add_argument("-r", '--radius', type=float, help="sphere radius in nanometers", required=True) 
    if(len(sys.argv) == 1):
        parser.print_help()
        exit(0)
    args = parser.parse_args()

    # Read input structure
    print "(1/7) Read input structure: %s" % args.input
    line_header, line_nr_atoms, lines_atoms, line_edge_lengths = gmx_tools.gro.read_gro(args.input)
    
    # Read positions
    print "(2/7) Read positions"
    Lx,Ly,Lz = gmx_tools.gro._get_edge_lengths(line_edge_lengths)
    center = np.array([Lx, Ly, Lz]) / 2.
    m0,x0,y0,z0 = gmx_tools.gro._get_positions(lines_atoms)
    N = len(m0)
    
    # Calculate distance from center
    print "(3/7) Calculate distances from center"
    r0 = np.sqrt((x0-center[0])**2 + (y0-center[1])**2 + (z0-center[2])**2)

    # Crop out sphere
    print "(4/7) Crop out sphere and remove partials"
    crop_mask = r0 < args.radius
    # Remove partials
    partial = (crop_mask[:-1]!=crop_mask[1:])*(m0[:-1]==m0[1:])
    for i in np.arange(0,N-1)[partial]:
        M = m0==m0[i]
        assert (M.sum() == 3) # Water molecules have three atoms
        crop_mask[m0==m0[i]] = False
    # Count atoms that are removed
    N_cropped = (crop_mask==False).sum()
    print "(5/7) %i/%i atoms will be removed (%.1f %%)" % (N_cropped, N, round(100.*float(N_cropped)/N, 1))

    # Write output structure
    print "(6/7) Write output structure: %s" % args.output
    with open(args.output, "w") as f:
        lines_atoms_new = []
        for l in [lines_atoms[i] for i in range(N) if crop_mask[i]]:
            lines_atoms_new.append(l)
        N_atoms_new = len(lines_atoms_new)
        line_nr_atoms_new = "%i\n" % N_atoms_new
        f.writelines([line_header] + [line_nr_atoms_new] + lines_atoms_new + [line_edge_lengths])

    print "(7/7) Update topology (number of SOL molecules)"
    # Count water molecules in droplet
    m,x,y,z = gmx_tools.gro.get_positions(args.output, name="SOL")
    Na_SOL = len(m)
    Nm_SOL = Na_SOL/3
    assert Nm_SOL*3 == Na_SOL
    with open(args.topol, "r") as f:
        lines = f.readlines()
        i = len(lines)-1
        while True:
            if lines[i].startswith("[ molecules ]"):
                break
            else:
                i -= 1
        while True:
            if lines[i].startswith("SOL"):
                lines[i] = "SOL %i\n" % Nm_SOL
                break
            i += 1
    with open(args.topol, "w") as f:
        f.writelines(lines)
    
