
import os

class ManifestLoader:
  def __init__(self, config):
    self.config = config

  def get_manifests(self):
    return self.config.sources_path()

  def get_manifest_versions(self):
    directories = os.walk(self.config.sources_path()).next()[1]
    versions = [int(x) for x in directories if x.isdigit()]
    return versions



