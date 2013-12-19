
import os
import Manifest
import logging


class ManifestLoader(object):
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.components = []
        self.versions = {}

    def get_manifest_for_path(self, path):
        try:
            with open(os.path.join(path, '.roborooter')) as f:
                version = int(f.read().strip())

            manifest = self.get_manifest_by_version(version)
        except IOError:
            self.logger.warning(
                'No .roborooter found at %s, falling back to version %d',
                path,
                self.config['default_version']
            )
            version = 'default'

            manifest = self.get_default_manifest()

        if manifest is None:
            msg = 'Completely unable to locate manifest version %s for %s.' % (
                version,
                path
            )
            self.logger.critical(msg)
            raise RuntimeError(msg)

        return manifest

    def get_default_manifest(self):
        version = self.config['default_version']
        manifest = self.get_manifest_by_version(version)

        if manifest is None:
            msg = 'Default manifest version %d cannot be located.' % version
            self.logger.critical(msg)
            raise RuntimeWarning(msg)

        return manifest

    def get_manifest_versions(self):
        try:
            self.logger.debug(
                'Walking %s for viable manifest version directories.',
                self.config['sources_path']
            )
            directories = os.walk(self.config['sources_path']).next()[1]
            versions = [int(x) for x in directories if x.isdigit()]
        except StopIteration:
            self.logger.critical(
                'Failed to walk %s, check the path and permissions.',
                self.config['sources_path']
            )

            versions = []

        versions.sort()

        return versions

    def get_manifest_by_version(self, version):
        min_ver = self.config['minimum_version']
        if version < min_ver:
            self.logger.info(
                'Requested version %s is below minimum %s, upgrading to %d.',
                version,
                min_ver,
                min_ver
            )

            version = min_ver
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
