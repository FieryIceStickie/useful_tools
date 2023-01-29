class Error(Exception):
    pass


class InvalidPolynomialTypeError(Error):
    def __init__(self, passed_type: type):
        self.passed_type = str(passed_type)
        super().__init__()

    def __str__(self):
        return f'Expected type str | Sequence | CoefDict, got {self.passed_type} instead'
