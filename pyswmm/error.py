class SWMM5FutureWarning(FutureWarning):
    def __init__(self, message):
        self.message = message


class SWMMException(Exception):
    """Custom exception class for SWMM errors."""

    def __init__(self, error_code, error_message):
        self.warning = False
        self.args = (error_code, )
        self.message = error_message

    def __str__(self):
        return self.message


class PYSWMMException(Exception):
    """Custom exception class for PySWMM errors. """

    def __init__(self, error_message):
        self.warning = False
        self.message = error_message

    def __str__(self):
        return self.message
