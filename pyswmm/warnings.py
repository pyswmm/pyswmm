class SimulationContextWarning(ResourceWarning):
    """Warning raised for SWMM Simulation Context

    Attributes:
        message -- explanation of the error
    """
    message = """
    \tThe Simulation object is intended to be used with a context
    \tmanager. System resources will not be freed without calling 
    \tthe close method. See Simulation class docs for details.
    """