from distutils.core import setup, Extension
import numpy.distutils.misc_util

ext = Extension("popdrop", sources=["popdropmodule.c"])
setup(name="condor_popdrop",ext_modules=[ext], include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs())
