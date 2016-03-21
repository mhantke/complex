import numpy
import h5py
import scipy.constants
import popdrop

from python_tools import multiprocesstools as mpt

from matplotlib import pyplot as pypl
from scipy.misc import factorial

# Molar protein concentration
cs_molar = [5E-6, 75E-6, 100E-6, 200E-6] # [mol/l]

for c_molar in cs_molar:

    # Parameters
    # ==========

    # Protein mass
    m_P = 53.3E3 # [Da]
    # Simulation volume
    V = 0.125E-18 # [m^3]
    # Correction factor
    #x = 2.
    # Droplet radius (will be later rescaled to R_D_xi)
    R_D = 9.E-9
    # Protein mass density
    rho_P = 0.84 / (1E-10)**3 # [Da/m^3]

    # Derived
    # =======
    
    # Hard sphere radius of protein
    R_S = (m_P/rho_P * 3./4./numpy.pi)**(1/3.)
    # Rescaled droplet radius
    #R_D_xi = R_D * x
    R_D_xi = numpy.array([20,25,30,35])*1E-9
    # Rescaled droplet volume
    V_D_xi = 4/3.*numpy.pi*R_D_xi**3
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

    def worker_i(D, i):
        return {"pos" : popdrop.popdrop(N, L, R_S, R_D_xi[i])}
    def getwork_i(i):
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
            f["/p"] = p_D_xi
            f["/c_molar"] = [c_molar]
    def getres_i(i):
        with h5py.File("drops_%i.h5" % i, "r") as f:
            pos = numpy.array(f["/pos"])
            n_particles = numpy.array(f["/n_particles"])
        return n_particles,pos

    for i in range(len(R_D_xi)):
        print i, R_D_xi[i]
        loginit_i(i, N_max=40)
        print "initialised"
        mpt.multiprocess(Nprocesses,
                         Njobs, 
                         lambda D: worker_i(D, i),
                         lambda : getwork_i(i), 
                         logres = lambda res:logres_i(res, i))

        print "mp started"
        n_particles_i,res_i = getres_i(i)

        print "plot res"
        H = numpy.histogram(n_particles_i, bins=21, range=(-0.5,20.5), normed=True)
        hist_n = H[0]
        hist_bins = H[1]
        hist_bins = hist_bins[:-1] + (hist_bins[1]-hist_bins[0])/2.
        poisson_model = lambda k,l: (l**k*numpy.exp(-l))/factorial(k)
        hist_n_poisson = numpy.array([poisson_model(n, p_D_xi[i]) for n in hist_bins])
        pypl.plot(hist_bins, hist_n_poisson*hist_n.sum()/hist_n_poisson.sum(),c="black",ls='--')
        pypl.plot(hist_bins, hist_n,c='darkblue',lw=1.5)
        
    pypl.ylabel("Abundance")
    pypl.xlabel("Number of biological units")
    pypl.savefig("occupancies_%.1fnM.png" % (c_molar/1E-6), dpi=400)
    pypl.clf()
