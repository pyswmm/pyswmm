class IncompleteSimulation(Exception):
    """Exception raised for incomplete simulation

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class OutputException(Exception):
    """Exception raised for SWMM Output object

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


_multi_sim_message = """\tDue to architectural limitations inside of EPA-SWMM
\tmultiple Simulations cannot be completed within a single
\tinstance of Python.  Consider launching the model runs
\tusing a Python Subprocess and a Queue manager.\n"""


class MultiSimulationError(Exception):
    """Exception raised if more than one SWMM Simulation
    class is trying to be created within a single instance
    of Python.
    """

    def __init__(self, message):

        self.message = message + "\n\n" + _multi_sim_message
        super().__init__(self.message)
