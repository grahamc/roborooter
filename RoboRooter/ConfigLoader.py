
import os.path
import ConfigParser

class ConfigLoader(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = None
        self._config()
        self._verify_config()

    def get_config(self):
        cfg = {
                'sources_path': self.sources_path(),
                'minimum_version': self.minimum_version(),
                'default_version': self.default_version()
        }

        return cfg

    # Get the path to the sources
    def sources_path(self):
        return os.path.join(os.path.dirname(self.config_file), self.config['sources'])

    def minimum_version(self):
        return int(self.config['minimum_version'])

    def default_version(self):
        return int(self.config['default_version'])

    # Parse the configuration one time
    def _config(self):
        if not self.config:
            config_parser = ConfigParser.ConfigParser(self._defaults())
            config_parser.read(self.config_file)

            self.config = dict(config_parser.items('roborooter'))
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
            raise ValueError('default_version must not be below minimum_version')


