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
            alternative_function: Callable = None,
            warning_message: str = None,
        ):
        self.function_name = function_name
        self.swmm_toolkit_minimum_version = swmm_toolkit_minimum_version
        self._alternative_function = alternative_function
        self.warning_message = warning_message

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
        True if self._alternative_function is not None else False
    
    def patch(self,module):
        """Apply monkey patch to module if toolkit version is less than minimum version"""
        if packaging.version.parse(_tk_version) < packaging.version.parse(self.swmm_toolkit_minimum_version):
            if self.warning_message is not None:
                warnings.warn(self.warning_message,MonkeyPatchWarning)
            
            if not hasattr(module,self.function_name) or self.force_patch:
                setattr(module,self.function_name,self.alt_function) 


_solver_monkey_patches = [
    _monkey_patch(function_name = "swmm_hotstart",swmm_toolkit_minimum_version="0.15.0"),
]

def _patch_solver(solver_module):
    for monkey_patch in _solver_monkey_patches:        
        monkey_patch.patch(solver_module)