# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""SWMM5 compiled libraries. This module provides the user with some options
for selecting the SWMM5 engine. """

# Standard library imports
import os
import sys

# Machine Architechture
MACHINE_BITS = 8 * tuple.__itemsize__

# Local Path
HERE = os.path.abspath(os.path.dirname(__file__))


# Platform Detection
def _platform():
    """Folder based on platform."""
    if os.name == 'nt':
        return 'windows'

    if sys.platform == 'darwin':
        return 'macos'

    if sys.platform.startswith('linux'):
        return 'linux'


# Library paths
if os.name == 'nt':
    LIB_SWMM = os.path.join(HERE, _platform(), 'swmm5.dll').replace('\\', '/')
elif sys.platform == 'darwin':
    LIB_SWMM = os.path.join(HERE, _platform(), 'libswmm5.dylib').replace('\\', '/')
elif sys.platform.startswith('linux'):
    LIB_SWMM = os.path.join(HERE, _platform(), 'libswmm5.so').replace('\\', '/')
else:
    LIB_SWMM = ''


class _DllPath(object):
    """DllPath Object."""

    def __init__(self):
        self._dll_loc = LIB_SWMM

    @property
    def dll_loc(self):
        """Get/set DLL Name."""
        return self._dll_loc

    @dll_loc.setter
    def dll_loc(self, value):
        """Set DLL Name."""
        self._dll_loc = value

    def __call__(self):
        """Caller returns DLL Name."""
        return self._dll_loc


# Initialize dll path object
DLL_SELECTION = _DllPath()


def use(arg):
    """
    Set the SWMM5 DLL.

    This method allows the user to define the engine they would
    like to use for the simulation.  It is important to understand
    that previous verisons of EPA-SWMM5 do not have the expanded
    toolkit functionality.  Therefore, only basic functionality for
    running a simulation is available.

    To use this, the user should copy and rename their SWMM5 DLL into
    the :file:`site-packages/pyswmm/lib/windows` directory.
    The example below outlines the steps.  This should be done
    before Simulation is imported.

    Examples:

    >>> import pyswmm
    >>> pyswmm.lib.use("swmm5")
    >>>
    >>> from pyswmm import Simulation
    """

    if os.name == 'nt':
        if not arg.endswith('.dll'):
            arg = arg + ".dll"
        if os.path.isfile(
                os.path.join(HERE, _platform(), arg).replace('\\', '/')):
            DLL_SELECTION.dll_loc = os.path.join(HERE, _platform(),
                                                 arg).replace('\\', '/')
        else:
            raise (Exception("Library Not Found"))

    elif sys.platform == 'darwin':
        if not arg.endswith('.dylib'):
            arg = arg + ".dylib"
        if os.path.isfile(
                os.path.join(HERE, _platform(), arg).replace('\\', '/')):
            DLL_SELECTION.dll_loc = os.path.join(HERE, _platform(),
                                                 arg).replace('\\', '/')
        else:
            raise (Exception("Library Not Found"))

    elif sys.platform.startswith('linux'):
        if not arg.endswith('.so'):
            arg = arg + ".so"
        if os.path.isfile(
                os.path.join(HERE, _platform(), arg).replace('\\', '/')):
            DLL_SELECTION.dll_loc = os.path.join(HERE, _platform(),
                                                 arg).replace('\\', '/')
        else:
            raise (Exception("Library Not Found"))
    else:
        raise (Exception("Operating System not Supported"))
