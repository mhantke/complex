import numpy as np

def read_gro(filename):
    with open(filename, "r") as f:
        lines_in = f.readlines()
        line_header = lines_in[0]
        line_nr_atoms = lines_in[1]
        N = int(lines_in[1][:-1])
        lines_atoms = lines_in[2:2+N]
        line_edge_lengths = lines_in[2+N]
        assert (N+3) == len(lines_in)
    return line_header, line_nr_atoms, lines_atoms, line_edge_lengths

def write_gro(filename, line_header, line_nr_atoms, lines_atoms, line_edge_lengths):
    with open(filename, "w") as f:
        f.writelines([line_header]+[line_nr_atoms]+lines_atoms+[line_edge_lengths])


def get_positions(filename, name=None):
    line_header, line_nr_atoms, lines_atoms, line_edge_lengths = read_gro(filename)
    return _get_positions(lines_atoms, name=name)

def _get_positions(lines_atoms, name=None):
    N = len(lines_atoms)
    i = np.zeros(N, dtype=np.uint32)
    x = np.zeros(N)
    y = np.zeros(N)
    z = np.zeros(N)
    n = np.chararray(N, itemsize=3)
    mask = np.ones(N, dtype=np.bool)
    mol_last = -1
    i_current = -1
    for k,l in enumerate(lines_atoms):
        # split string
        s = l[:-1].split(" ")
        s = [s_k for s_k in s if len(s_k)]
        mol = int(s[0][:-3])
        # write to arrays
        if mol_last != mol:
            i_current += 1
        mol_last = mol
        i[k] = i_current
        n[k] = s[0][-3:]
        x[k] = float(s[-3])
        y[k] = float(s[-2])
        z[k] = float(s[-1])
    if name is not None:
        mask = n == name
        i = i[mask]
        x = x[mask]
        y = y[mask]
        z = z[mask]
    return i,x,y,z

def get_edge_lengths(filename):
    line_header, line_nr_atoms, lines_atoms, line_edge_lengths = read_gro(filename)
    return _get_edge_lengths(line_edge_lengths)

def _get_edge_lengths(line_edge_lengths):
    s = line_edge_lengths[:-1].split(" ")
    s = [si for si in s if len(si)]
    Lx = float(s[-3])
    Ly = float(s[-2])
    Lz = float(s[-1])
    return Lx,Ly,Lz

