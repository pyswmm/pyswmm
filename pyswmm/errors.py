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