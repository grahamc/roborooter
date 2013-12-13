
class Noop(object):
  def __init__(self, applies=True):
    self.applies = applies

  def applies_to_manifest(self, manifest):
    return self.applies

