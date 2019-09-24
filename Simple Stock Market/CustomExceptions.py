class CustomExceptions(Exception):
    """Base class for all custom exceptions"""

    def __init__(self, msg):
        super().__init__(msg)
        #sys.exit(1)


class FixedDividendNotDefined(CustomExceptions):
    def __init__(self, msg):
        super().__init__(msg)


class NoFormulaPresentForNewType(CustomExceptions):
    def __init__(self, msg):
        super().__init__(msg)


class NoStockFound(CustomExceptions):
    def __init__(self, msg):
        super().__init__(msg)
