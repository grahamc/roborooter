
import FileHint
import os
import pwd
import grp
import logging


class Owner(FileHint.FileHint):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.hint_name = './manifests/permissions'
        self.state_expression = r'^(\w*):(\w*) \d* (.*)$'
        self.rules = []

    def _filter_violations(self, path):
        for rule in self.rules:
            self.logger.debug('Testing rule: %s', rule)
            rule_path = os.path.join(path, rule[2])
            try:
                expected_user = rule[0]
                expected_group = rule[1]
                expected = "%s:%s" % (expected_user, expected_group)

                file_stat = os.stat(rule_path)
                current_user = self._uid_to_name(file_stat.st_uid)
                current_group = self._gid_to_name(file_stat.st_gid)
                current = "%s:%s" % (current_user, current_group)

                if current != expected:
                    self.logger.info(
                        'Expected %s to be owned by %s but was owned by %s',
                        rule_path,
                        expected,
                        current
                    )
                    yield (expected_user, expected_group, rule_path)
            except OSError as e:
                self.logger.debug(
                    'Failed to check ownership of %s: %s',
                    rule_path,
                    e
                )

    def _uid_to_name(self, uid):
        return pwd.getpwuid(uid).pw_name

    def _name_to_uid(self, name):
        return pwd.getpwnam(name).pw_uid

    def _gid_to_name(self, gid):
        return grp.getgrgid(gid).gr_name

    def _name_to_gid(self, name):
        return grp.getgrnam(name).gr_gid

    def fix(self, path):
        for change in self._filter_violations(path):
            try:
                change_uid = self._name_to_uid(change[0])
                change_gid = self._name_to_gid(change[1])
                os.chown(change[2], change_uid, change_gid)
            except OSError as e:
                self.logger.error(
                    'Failed to change ownership of %s to %s:%s: %s',
                    change[2],
                    change[0],
                    change[1],
                    e
                )
