
import copy

class Manifest:
  def __init__(self, version, path):
    self.version = version
    self.path = path
    self.components = []

  def add_components(self, components):
    [self.add_component(component) for component in components]

  def add_component(self, component):
    if component.applies_to_manifest(self):
      self.components.append(copy.copy(component))

