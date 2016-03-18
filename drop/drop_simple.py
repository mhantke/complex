import numpy
import h5py
import scipy.constants
import popdrop

from python_tools import multiprocesstools as mpt

# Parameters
# ==========

# Molar protein concentration
c_molar = 100E-6
#c_molar = 200E-6 # [mol/l]
# Protein mass
m_P = 53.3E3 # [Da]
# Simulation volume
V = 0.125E-18 # [m^3]
# Correction factor
x = 2.
# Droplet radius (will be later rescaled to R_D_ksi)
R_D = 9.E-9
# Protein mass density
rho_P = 0.84 / (1E-10)**3 # [Da/m^3]

# Derived
# =======

# Hard sphere radius of protein
R_S = (m_P/rho_P * 3./4./pi)**(1/3.)
# Rescaled droplet radius
#R_D_xi = R_D * x
R_D_xi = array([20,25,30,35])*1E-9
# Rescaled droplet volume
V_D_xi = 4/3.*pi*R_D_xi**3
# SI protein concentration
c = c_molar * scipy.constants.Avogadro / 0.1**3 # [1/m^3]
# Expectation value for number of particles per droplet
p_D_xi = c * V_D_xi
# Number of particles in virutual box
N = int(round(V * c))
# Edge length of virtual box
L = V**(1/3.)

# Assign positions
# ================

Nprocesses = 16
Njobs = 1600
results = []
def worker_i(D, i):
    return {"pos" : popdrop.popdrop(N, L, R_S, R_D_xi[i])}
def getwork():
    return {}
def logres_i(res, i):
    with h5py.File("drops_%i.h5" % i, "r+") as f:
        i = f["/i"][0]
        n_particles = len(res["pos"])
        f["/n_particles"][i] = n_particles
        if n_particles > 0:
            n = min([n_particles,f["/pos"].shape[1]])
            f["/pos"][i,:n,:] = res["pos"][:,:]
        f["/i"][0] = i + 1
def loginit_i(i, N_max=10):
    with h5py.File("drops_%i.h5" % i, "w") as f:
        f["/n_particles"] = numpy.zeros(shape=(Njobs))
        f["/pos"] = numpy.zeros(shape=(Njobs,N_max,3))
        f["/i"] = [0]
def getres_i(i):
    with h5py.File("drops_%i.h5" % i, "r") as f:
        pos = numpy.array(f["/pos"])
        n_particles = numpy.array(f["/n_particles"])
    return n_particles,pos

n_particles = []
res = []
for i in range(len(R_D_xi)):
    print i, R_D_xi[i]
    loginit_i(i, N_max=40)
    print "initialised"
    mpt.multiprocess(Nprocesses,
                     Njobs, 
                     lambda D: worker_i(D, i),
                     getwork, 
                     logres = lambda res:logres_i(res, i),
                     logger = logger)
    print "mp started"
    n_particles_i,res_i = getres_i(i)
    print "collect res"
    n_particles.append(n_particles_i)
    res.append(res_i)
