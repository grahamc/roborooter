
class Manifest:
  def __init__(self, version, path):
    self.version = version
    self.path = path
    self.components = []

  def version(self):
    return self.version

  def path(self):
    return self.path

  def add_components(self, components):
    self.components += components
    return True
