#include <Python.h>
#include <numpy/arrayobject.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

PyDoc_STRVAR(popdrop__doc__, "popdrop(n_particles, box_edge_length, particle_radius, droplet_radius, random_seed=None)\n\nDrOP algorithm\n\nPopulate box with particles at non-overlapping locations and cut out spherical droplet.");
static PyObject *popdrop(PyObject *self, PyObject *args, PyObject *kwargs)
{

  int n_particles;
  double box_edge_length, particle_radius, droplet_radius;
  
  static char *kwlist[] = {"n_particles", "box_edge_length", "particle_radius", "droplet_radius", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iddd", kwlist, &n_particles, &box_edge_length, &particle_radius, &droplet_radius)) {
    return NULL;
  }

  if (box_edge_length <= 0.) {
    PyErr_SetString(PyExc_ValueError, "Box edge length must be > 0.");
    return NULL;
  }

  if (particle_radius <= 0.) {
    PyErr_SetString(PyExc_ValueError, "Particle radius must be > 0.");
    return NULL;
  }

  if (droplet_radius <= 0.) {
    PyErr_SetString(PyExc_ValueError, "Droplet radius must be > 0.");
    return NULL;
  }

  if (droplet_radius >= (box_edge_length/2.)) {
    PyErr_SetString(PyExc_ValueError, "Droplet radius must be smaller than half the box edge length.");
    return NULL;
  }

  if (droplet_radius <= particle_radius) {
    PyErr_SetString(PyExc_ValueError, "Particle radius must be smaller than droplet radius.");
    return NULL;
  }

  double * pos = (double *) malloc(sizeof(double) * n_particles * 3);
  double * temp = (double *) malloc(sizeof(double) * n_particles * 3);
  
  int i;
  int n_box;
  int n_droplet;
  int overlap;
  int try = 0;
  int max_try = INT_MAX;
  double x,y,z,dx,dy,dz,d_sq;
  double particle_radius_sq;
  double droplet_radius_sq;

  // setup unbuffered urandom
  FILE * urandom = fopen ("/dev/urandom", "r");
  setvbuf (urandom, NULL, _IONBF, 0);  // turn off buffering
  
  // setup state buffer
  unsigned short randstate[3];
  // fgetc() returns a `char`, we need to fill a `short`
  randstate[0] = (fgetc (urandom) << 8) | fgetc (urandom);
  randstate[1] = (fgetc (urandom) << 8) | fgetc (urandom);
  randstate[2] = (fgetc (urandom) << 8) | fgetc (urandom);
  
  // cleanup urandom
  fclose (urandom);


  
  printf("n_particles = %i; box_edge_length = %e; particle_radius = %e; droplet_radius = %e\n", n_particles, box_edge_length, particle_radius, droplet_radius);

  // 1) Place spherical particles at random positions in box. Do not allow overlap
  //    (Allow spheres to be partially outside of the box!)
  n_box = 0;
  particle_radius_sq = (particle_radius / box_edge_length)*(particle_radius / box_edge_length);
  
  while ((n_box < n_particles) && (try < max_try)) {
    //x = (double) rand() / (RAND_MAX+1.);
    //y = (double) rand() / (RAND_MAX+1.);
    //z = (double) rand() / (RAND_MAX+1.);
    x = erand48(randstate);
    y = erand48(randstate);
    z = erand48(randstate);
    overlap = 0;
    // Check if position overlaps with any particle in box
    for (i=0; i<n_box; i++) {
      dx = x-pos[i*3+0];
      dy = y-pos[i*3+1];
      dz = z-pos[i*3+2];
      d_sq = dx*dx + dy*dy + dz*dz;
      if (d_sq < particle_radius_sq) {
	overlap = 1;
      }
    }
    // Assign particle position if no overlap found
    if (overlap == 0) {
      try = 0;
      pos[n_box*3+0] = x;
      pos[n_box*3+1] = y;
      pos[n_box*3+2] = z;
      n_box++;
    } else {
      try++;
    }
  }
  if (try == max_try) {
    PyErr_SetString(PyExc_ValueError, "Reached limit of tries for placing particles into the box. Too high particle density?");
    return NULL;
  }

  // 2) Select spherical volume (droplet) from the box and count the particles that live in it
  //    (Allow particles to be partially outside of the droplet!)
  n_droplet = 0;
  droplet_radius_sq = (droplet_radius / box_edge_length)*(droplet_radius / box_edge_length);
    
  for (i=0; i<n_particles; i++) {
    x = pos[i*3+0];
    y = pos[i*3+1];
    z = pos[i*3+2];
    // Check if particle entirely in droplet
    dx = 0.5-x;
    dy = 0.5-y;
    dz = 0.5-z;
    d_sq = dx*dx + dy*dy + dz*dz;
    if (d_sq < droplet_radius_sq) {
      temp[n_droplet*3+0] = x;
      temp[n_droplet*3+1] = y;
      temp[n_droplet*3+2] = z;
      n_droplet++;
    }     
  }

  // Alloc python numpy array for output
  int droplet_dim[] = {n_droplet, 3};
  PyObject *droplet_array = (PyObject *)PyArray_FromDims(2, droplet_dim, NPY_FLOAT64);
  double *droplet = PyArray_DATA(droplet_array);

  for (i=0; i<(n_droplet*3); i++) {
    droplet[i] = temp[i];
  }
  
  free(pos);
  free(temp);
  
  return droplet_array;
}


static PyMethodDef PopdropMethods[] = {
  {"popdrop", (PyCFunction)popdrop, METH_VARARGS|METH_KEYWORDS, popdrop__doc__},
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initpopdrop(void)
{
  import_array();
  PyObject *m = Py_InitModule3("popdrop", PopdropMethods, "Random placement of particles into spherical volume");
  if (m == NULL)
    return;
}
