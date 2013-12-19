
import FileHint
import os
import logging


class Whitelist(FileHint.FileHint):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.hint_name = './manifests/whitelist'
        self.state_expression = r'^(.+)$'
        self.rules = []

        self.files = ['./.roborooter']
        self.directories = []

    def load_state(self, manifest):
        self._load_state_via_regex(manifest)

        for rule in self.rules:
            path = rule[0]
            if path[-1] == '/':
                self.directories.append(os.path.normpath(path))
            else:
                self.files.append(path)

        self.logger.debug(
            'Loaded %d whitelisted directories and %d whitelisted files.',
            len(self.directories),
            len(self.files)
        )

    def _filter_violations(self, root_path, rel='./'):
        path = os.path.join(root_path, rel)
        self.logger.debug('Inspecting %s for whitelist violations', path)
        for entry in os.listdir(path):
            scoped_path = os.path.join(
                './',
                os.path.normpath(os.path.join(rel, entry))
            )
            absolute_path = os.path.join(
                './',
                os.path.normpath(os.path.join(root_path, rel, entry))
            )
            if os.path.isfile(absolute_path):
                if scoped_path in self.files:
                    self.logger.debug(
                        'Found whitelisted file: %s',
                        absolute_path
                    )
                    continue
                else:
                    self.logger.info(
                        'Found file violation: %s',
                        absolute_path
                    )
                    yield absolute_path
            elif os.path.isdir(absolute_path):
                if os.path.normpath(scoped_path) in self.directories:
                    self.logger.debug(
                        'Found whitelisted directory: %s',
                        absolute_path
                    )
                    continue
                else:
                    _sub_filter = self._filter_violations(
                        root_path,
                        scoped_path
                    )
                    for yield_path in _sub_filter:
                        yield yield_path

    def fix(self, path):
        for change in self._filter_violations(path):
            self.logger.info('Removing file: %s', change)
            try:
                os.remove(change)
            except OSError as e:
                self.logger.error(
                    'Failed to remove file %s: %s',
                    change,
                    e
                )
