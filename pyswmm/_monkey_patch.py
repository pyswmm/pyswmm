"""
This module implements monkey patches to the swmm.toolkit.solver module.

As the SWMM API is expanded and/or the EPA updates the engine, pyswmm should grow to 
accomodate the new features. However, sometimes the API changes in a way that is not 
backwards compatible. In these cases, we can use monkey patches to add the new features 
to older versions of the toolkit.

Those monkey patches may be python implementations of the new features or they
may be a wrapper around the new toolkit function api that raises an error if the
user tries to use the new feature with an older version of the toolkit.
"""

from typing import Callable
import warnings

import packaging.version
from swmm.toolkit import __version__ as _tk_version
from swmm.toolkit import solver
from pyswmm.swmm5 import PySWMM

# %% ###########################
# region MonkeyPatchTypes ######
################################
class ToolkitVersionException(Exception):
    pass

class MonkeyPatchWarning(Warning):
    pass

class _monkey_patch:
    """
    A class to store and implement monkey patches
    """
    def __init__(
            self,
            function_name: str,
            swmm_toolkit_minimum_version: str,
            object_to_patch: object,
            alternative_function: Callable = None,
            warning_message: str = None,
        ):
        self.function_name = function_name
        self.swmm_toolkit_minimum_version = swmm_toolkit_minimum_version
        self._alternative_function = alternative_function
        self.warning_message = warning_message
        self._object_to_patch = object_to_patch

    def _toolkit_error_func(self,*args,**kwargs):
        """A default monkey patch function that raises a toolkit version error"""        
        raise ToolkitVersionException(
            f'SWMM version must be at least {self.swmm_toolkit_minimum_version}. '
            f"The currently installed version is {_tk_version}"
        )
    
    @property
    def alt_function(self):
        """Return the alternative function or the default toolkit error function 
        depending on availability"""
        if self._alternative_function is None:
            return self._toolkit_error_func
        else:
            return self._alternative_function
    
    @property
    def force_patch(self):
        """
        always patch if the alternative function is not None

        There might be a case where we don't necesarily want to patch the function but only
        want to issue a warning at runtime (e.g. if api doen't change but as expanded capabilities in a newer version)
        """
        return True if self._alternative_function is not None else False
    
    def patch(self):
        """Apply monkey patch to module if toolkit version is less than minimum version"""
        if packaging.version.parse(_tk_version) < packaging.version.parse(self.swmm_toolkit_minimum_version):
            if self.warning_message is not None:
                warnings.warn(self.warning_message,MonkeyPatchWarning)
            
            if not hasattr(self._object_to_patch,self.function_name) or self.force_patch:
                setattr(self._object_to_patch,self.function_name,self.alt_function) 

# endregion MonkeyPatchTypes ####

# %% ##############################
# region PySWMMObjectPatches ######
###################################

def swmm_stride(self, advanceSeconds):
    """
    This function allows for user defined stride length to advance
    the model simulation by a defined time.  This is useful when control
    rules are managed externally by PySWMM. Instead of evaluating rules
    every routing step, instead the simulation can be advanced further
    in time before the PySWMM can intervene. When a 0 is returned, the
    simulation period has reached the end.

    :param int advanceSeconds: Number seconds to advance the simulation
                                forward.
    :return: Current simulation time after a stride in decimal days (float)
    :rtype: float

    Examples:

    >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
    >>> swmm_model.swmm_open()
    >>> swmm_model.swmm_start(True)
    >>> while(True):
    ...     time = swmm_model.swmm_stride(600)
    ...     if (time <= 0.0): break
    >>>
    >>> swmm_model.swmm_end()
    >>> swmm_model.swmm_report()
    >>> swmm_model.swmm_close()
    """
    ctime = self.curSimTime
    secPday = 3600.0 * 24.0
    advanceDays = advanceSeconds / secPday
    eps = advanceDays * 0.00001
    elapsed_time = 0

    while self.curSimTime <= ctime + advanceDays - eps:
        elapsed_time = solver.swmm_step()
        if elapsed_time == 0:
            return 0.0
        self.curSimTime = elapsed_time

    return elapsed_time

# endregion PySWMMObjectPatches ####


# Patches
_patches = [
    _monkey_patch(function_name = "swmm_hotstart",swmm_toolkit_minimum_version="0.15.0",object_to_patch=solver),
    _monkey_patch(function_name = "swmm_stride" ,swmm_toolkit_minimum_version="0.15.0",object_to_patch=PySWMM,alternative_function=swmm_stride),

]
def patch():    
    # patch solver
    for monkey_patch in _patches:        
        monkey_patch.patch()