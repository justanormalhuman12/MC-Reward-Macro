import logging
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        return super().format(record)
