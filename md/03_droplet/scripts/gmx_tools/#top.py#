
def set_nr_mol(filename, molecule_name, N):
    with open(filename, "r") as f:
        lines = f.readlines()
        i = len(lines)-1
        while True:
            if lines[i].startswith("[ molecules ]"):
                break
            else:
                i -= 1
        while True:
            if lines[i].startswith(molecule_name):
                lines[i] = "SOL %i\n" % N
                break
            i += 1
    with open(filename, "w") as f:
        f.writelines(lines)
    
