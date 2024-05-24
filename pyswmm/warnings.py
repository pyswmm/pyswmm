class SimulationContextWarning(ResourceWarning):
    """Warning raised for SWMM Simulation Context

    Attributes:
        message -- explanation of the error
    """
    message = """
    \tThe Simulation object is intended for use with the context
    \tmanager. System resources will not be freed
    \twithout calling close method. See Simulation docs for details.
    """