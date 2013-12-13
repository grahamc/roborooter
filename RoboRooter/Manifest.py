
import copy

class Manifest(object):
  def __init__(self, version, path):
    self.version = version
    self.path = path
    self.components = []

  def add_components(self, components):
    [self.add_component(component) for component in components]

  def add_component(self, component):
    if not component.applies_to_manifest(self):
      return False

    local_component = copy.copy(component)
    local_component.load_state(self)
    self.components.append(local_component)

    return True

