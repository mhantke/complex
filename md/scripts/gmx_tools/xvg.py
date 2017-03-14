import numpy as np

def read_xvg(filename, ncols):
    with open(filename, "r") as f:
        lines = [l for l in f.readlines() if not (l.startswith(";") or l.startswith("#") or l.startswith("@") or l.startswith("&"))]
        out = []
        for col in range(ncols):
            out.append(np.array([float(l[:-1].split()[col]) for l in lines]))
        out = np.array(out)
    return out
