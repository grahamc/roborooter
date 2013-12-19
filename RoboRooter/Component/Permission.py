
import FileHint
import os
import logging


class Permission(FileHint.FileHint):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.hint_name = './manifests/permissions'
        self.state_expression = r'^\w*:\w* (\d*) (.*)$'
        self.rules = []

    def _filter_violations(self, path):
        for rule in self.rules:
            self.logger.debug('Testing rule: %s', rule)
            rule_path = os.path.join(path, rule[1])
            try:
                expected = int(rule[0], 8)
                current = os.lstat(rule_path).st_mode & 0777
                if current != expected:
                    self.logger.info(
                        'Expected %s to have %o but was %o',
                        rule_path,
                        expected,
                        current
                    )
                    yield (expected, rule_path)
            except OSError as e:
                self.logger.debug(
                    'Failed to check permissions on %s: %s',
                    rule_path,
                    e
                )

    def fix(self, path):
        for change in self._filter_violations(path):
            try:
                os.chmod(change[1], change[0])
            except OSError as e:
                self.logger.error(
                    'Failed to update permissions on %s to %s: %s',
                    change[1],
                    change[0],
                    e
                )
