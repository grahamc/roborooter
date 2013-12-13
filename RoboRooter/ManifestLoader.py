
import os
import RoboRooter.Manifest as Manifest

class ManifestLoader:
  def __init__(self, config):
    self.config = config
    self.components = []
    self.versions = {}

  def get_manifests(self):
    return self.config['sources_path']

  def get_manifest_versions(self):
    try:
      directories = os.walk(self.config['sources_path']).next()[1]
      versions = [int(x) for x in directories if x.isdigit()]
    except:
      versions = []

    versions.sort()

    return versions

  def get_manifest_by_version(self, version):
    if version not in self.get_manifest_versions():
      return None
    if version not in self.versions:
      self._create_and_store_manifest(version)

    return self.versions[version]

  def add_component(self, component):
    if not component:
      raise ValueError

    self.components.append(component)

    return True

  def _create_and_store_manifest(self, version):
    if version not in self.get_manifest_versions():
      raise ValueError

    manifest = Manifest.Manifest(
      version,
      os.path.join(
        self.config['sources_path'],
        str(version)
      )
    )

    manifest.add_components(self.components)

    self.versions[version] = manifest

    return True



