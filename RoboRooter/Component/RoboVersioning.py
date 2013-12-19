
import os
import logging


class RoboVersioning(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def applies_to_manifest(self, manifest):
        return True

    def load_state(self, manifest):
        self.version = manifest.version

    def needs_fixing(self, path, process_all=False):
        version_file = os.path.join(path, './.roborooter')

        version = None
        try:
            with open(version_file) as f:
                version = int(f.read(self.version).strip())
        except IOError as e:
            self.logger.warning(
                'Could not read %s: %s',
                version_file,
                e
            )

        return version != self.version

    def fix(self, path):
        version_file = os.path.join(path, './.roborooter')

        try:
            with open(version_file, 'w') as f:
                f.write(str(self.version))
        except IOError as e:
            self.logger.error(
                'Could not write out roboroot manifest version to %s: %s',
                version_file,
                e
            )
