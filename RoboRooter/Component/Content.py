
import FileHint
import hashlib
import shutil
import os
import logging


class Content(FileHint.FileHint):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.hint_name = './manifests/md5'
        self.state_expression = r'^([0-9a-f]{32})\s+(.+)$'
        self.rules = []
        self.origin = None
        super(FileHint.FileHint, self).__init__()

    def load_state(self, manifest):
        self._load_state_via_regex(manifest)
        self.origin = os.path.join(manifest.path, './sources/')

    def set_origin(self, origin):
        self.origin = origin

    def _filter_violations(self, path):
        for rule in self.rules:
            self.logger.debug('Testing rule: %s', rule)
            rule_path = os.path.join(path, rule[1])
            origin_path = os.path.join(self.origin, rule[1])

            try:
                expected = rule[0]
                current = self._calculate_md5(rule_path)
                if current != expected:
                    self.logger.info(
                        'File %s should have hash %s but currently has %s',
                        rule_path,
                        expected,
                        current
                    )
                    yield (origin_path, rule_path)
            except(OSError):
                continue

    def fix(self, path):
        for change in self._filter_violations(path):
            target_dir = os.path.dirname(change[1])
            if not os.path.isdir(os.path.dirname(change[1])):
                self.logger.debug(
                    'Path does not exist, creating: %s',
                    target_dir
                )
                try:
                    os.makedirs(target_dir)
                except OSError as e:
                    self.logger.error(
                        'Failed to create directory %s: %s',
                        target_dir,
                        e
                    )

            self.logger.info(
                'Copying file from %s to %s.',
                change[0],
                change[1]
            )
            try:
                shutil.copyfile(change[0], change[1])
            except(OSError, IOError) as e:
                self.logger.error(
                    'Failed to copy from %s to %s: %s',
                    change[0],
                    change[1],
                    e
                )

    def _calculate_md5(self, filename):
        md5 = hashlib.md5()
        try:
            with open(filename, 'r') as f:
                for chunk in iter(lambda: f.read(256*128), b''):
                    md5.update(chunk)
        except IOError as e:
            self.logger.debug('Failed to sum %s due to: %s', filename, e)
            return None

        return md5.hexdigest()
