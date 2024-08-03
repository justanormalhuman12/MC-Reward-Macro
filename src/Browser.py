class Browser:
    def __init__(self, mobile=False, account=None, args=None):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    class utils:
        @staticmethod
        def formatNumber(number):
            return number

        @staticmethod
        def getRemainingSearches():
            return (0, 0)