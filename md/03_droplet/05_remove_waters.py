#!/usr/bin/env python
import numpy as np
import argparse, sys

def get_positions(lines_atoms):
    m = np.zeros(len(lines_atoms), dtype=np.uint32)
    x = np.zeros(len(lines_atoms))
    y = np.zeros(len(lines_atoms))
    z = np.zeros(len(lines_atoms))
    mi_last = 0
    offset = 0
    for i,l in enumerate(lines_atoms):
        s = l[:-1].split(" ")
        s = [si for si in s if len(si)]
        m[i] = np.uint32(s[0][:-3]) + offset
        if m[i] < mi_last:
            offset += 100000
            m[i] += 100000
        mi_last = m[i]
        x[i] = float(s[-3])
        y[i] = float(s[-2])
        z[i] = float(s[-1])
    return m,x,y,z

def get_edge_lengths(line_dims):
    s = line_dims[:-1].split(" ")
    s = [si for si in s if len(si)]
    Lx = float(s[-3])
    Ly = float(s[-2])
    Lz = float(s[-1])
    return Lx,Ly,Lz


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cut spherical droplet in .gro file')
    parser.add_argument('-s', '--input', metavar='box.gro', type=str, help="gromacs file: box filled with water", nargs='?', const=True, required=True)
    parser.add_argument('-o', '--output', metavar='droplet.gro', type=str, help="gromacs file: droplet filled with water", nargs='?', const=True, required=True)
    parser.add_argument("-r", '--radius', type=float, help="sphere radius in nanometers", required=True) 
    if(len(sys.argv) == 1):
        parser.print_help()
        exit(0)
    args = parser.parse_args()

    # Read input structure
    print "(1/6) Read input structure: %s" % args.input
    with open(args.input, "r") as f:
        lines_in = f.readlines()
        first_line = lines_in[0]
        N = int(lines_in[1][:-1])
        lines_atoms0 = lines_in[2:2+N]
        last_line = lines_in[2+N]
        assert (N+3) == len(lines_in)

    # Read positions
    print "(2/6) Read positions"
    Lx,Ly,Lz = get_edge_lengths(last_line)
    center = np.array([Lx, Ly, Lz]) / 2.
    m0,x0,y0,z0 = get_positions(lines_atoms0)
    
    # Calculate distance from center
    print "(3/6) Calculate distances from center"
    r0 = np.sqrt((x0-center[0])**2 + (y0-center[1])**2 + (z0-center[2])**2)

    # Crop out sphere
    print "(4/6) Crop out sphere and remove partials"
    crop_mask = r0 < args.radius
    # Remove partials
    partial = (crop_mask[:-1]!=crop_mask[1:])*(m0[:-1]==m0[1:])
    for i in np.arange(0,N-1)[partial]:
        crop_mask[m0==m0[i]] = False
    # Count atoms that are removed
    N_cropped = (crop_mask==False).sum()
    print "(5/6) %i/%i atoms will be removed (%.1f %%)" % (N_cropped, N, round(float(N_cropped)/N, 1))

    # Write output structure
    print "(5/6) Write output structure: %s" % args.output
    with open(args.output, "w") as f:
        lines_atoms1 = []
        for l in [lines_atoms0[i] for i in range(N) if crop_mask[i]]:
            lines_atoms1.append(l)
        second_line = "%i\n" % len(lines_atoms1)
        f.writelines([first_line] + [second_line] + lines_atoms1 + [last_line])
