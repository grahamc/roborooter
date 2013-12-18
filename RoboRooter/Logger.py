
import logging
import pprint

class LoggerConfiguration(object):
    def __init__(self):
        self.fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.log_level = 2

        logger.basicConfig(fmt=self.fmt)

    def configureByOptions(self, values):
        default_level = 2
        verbosity = values.verbose
        shush = values.quiet
        self.log_level = (2 - verbosity + shush) * 10

    def getLogger(self, name):
        logger = logging.getLogger(name)
        self.applyConfigurationToLogger(logger)
        return logger

    def applyConfigurationToLogger(self, logger):
        logger.setLevel(self.log_level)


