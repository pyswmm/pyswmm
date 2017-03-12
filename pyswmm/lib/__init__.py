# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""SWMM5 compiled libraries."""

# Standard library imports
import os

# Machine Architechture
MACHINE_BITS = 8 * tuple.__itemsize__

# Local Path
HERE = os.path.abspath(os.path.dirname(__file__))

# Platform Detection
def _platform():
    """ Folder based on platform """
    if os.name == 'nt':
        return 'windows'

# Library paths
if os.name == 'nt':
    LIB_SWMM = os.path.join(HERE, _platform(),
                            'swmm5.dll').replace('\\', '/')

class _DllPath(object):
    """
    DllPath Object.
    """
    def __init__(self):
        self._dll_loc = LIB_SWMM
    @property
    def dll_loc(self):
        """Get/set DLL Name """
        return self._dll_loc
    @dll_loc.setter
    def dll_loc(self, value):
        """Set DLL Name """
        self._dll_loc = value
    def __call__(self):
        """ """
        return self._dll_loc

# Initialize dll path object
DLL_SELECTION = _DllPath()

def use(arg):
    """
    Set the SWMM5 DLL

    Examples:
    >>> import pyswmm
    >>> pyswmm.lib.use("TestDLL")

    from pyswmm import Simulation
    """
    if not arg.endswith('.dll'):
        arg = arg + ".dll"
    if os.path.isfile(os.path.join(HERE, _platform(),
                                   arg).replace('\\', '/')):
        DLL_SELECTION.dll_loc = os.path.join(HERE, _platform(),
                                             arg).replace('\\', '/')
    else:
        raise(Exception("Library Not Found"))
