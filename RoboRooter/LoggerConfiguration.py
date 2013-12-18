
import logging
import pprint

class LoggerConfiguration(object):
    def __init__(self):
        self.fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.log_level = 2

    def configureByOptions(self, values):
        default_level = 2
        verbosity = values.verbose
        shush = values.quiet
        calculated = (2 - verbosity + shush) * 10
        self.log_level = min(50, max(10, calculated))
        logging.basicConfig(format=self.fmt, level=self.log_level)
        logging.getLogger(__name__).debug(
            'Default log level set to %s',
            logging.getLevelName(self.log_level)
        )
