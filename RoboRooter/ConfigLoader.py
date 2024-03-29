
import os.path
import ConfigParser
import logging


class ConfigLoader(object):
    def __init__(self, config_file):
        self.logger = logging.getLogger(__name__)
        self.config_file = config_file
        self.config = None
        self._config()
        self._verify_config()

    def override(self, attribute, value):
        self.config[attribute] = value

    def get_config(self):
        cfg = {
            'sources_path': self.sources_path(),
            'minimum_version': self.minimum_version(),
            'default_version': self.default_version()
        }

        return cfg

    # Get the path to the sources
    def sources_path(self):
        config_dir_path = os.path.dirname(self.config_file)
        return os.path.join(config_dir_path, self.config['sources'])

    def minimum_version(self):
        return int(self.config['minimum_version'])

    def default_version(self):
        return int(self.config['default_version'])

    # Parse the configuration one time
    def _config(self):
        if not self.config:
            config_parser = ConfigParser.ConfigParser(self._defaults())
            config_parser.read(self.config_file)

            try:
                self.config = dict(config_parser.items('roborooter'))
            except ConfigParser.NoSectionError as e:
                self.logger.critical(
                    'Could not parse config file %s: %s',
                    self.config_file,
                    e
                )
                raise e

        return self.config

    def _defaults(self):
        default = {
            'sources': '/usr/local/roborooter/',
            'minimum_version': '1',
            'default_version': '1'
        }

        return default

    def _verify_config(self):
        if self.default_version() < self.minimum_version():
            msg = 'default_version must not be below minimum_version'
            logging.critical(msg)
            raise ValueError(msg)
