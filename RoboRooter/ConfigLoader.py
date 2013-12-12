
import ConfigParser

class ConfigLoader:
  def __init__(self, config_file):
    self.config_file = config_file
    self.config = None
    self._config()

  # Get the path to the sources
  def sources_path(self):
    return self.config['sources']

  def minimum_version(self):
    return self.config['minimum_version']

  def default_version(self):
    return self.config['default_version']

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
