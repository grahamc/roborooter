
import FileHint
import os
import pwd
import grp
import pprint

class Owner(FileHint.FileHint):
  def __init__(self):
    self.hint_name = './manifests/permissions'
    self.state_expression = r'^(\w*):(\w*) \d* (.*)$'
    self.rules = []

  def _filter_violations(self, path):
    for rule in self.rules:
      rule_path = os.path.join(path, rule[2])
      try:
        expected_user = rule[0]
        expected_group = rule[1]
        expected = "%s:%s" % (expected_user, expected_group)

        file_stat = os.stat(rule_path)
        current_user = self._uid_to_name(file_stat.st_uid)
        current_group = self._gid_to_name(file_stat.st_gid)
        current = "%s:%s" % (current_user, current_group);

        if current != expected:
          print "Expected %s to be owned by %s but was %s" % (
            rule_path,
            current,
            expected
          )
          yield (expected_user, expected_group, rule_path)
      except(OSError):
        continue

  def _uid_to_name(self, uid):
    return pwd.getpwuid(uid).pw_name

  def _name_to_uid(self, name):
    return pwd.getpwnam(name).pw_uid

  def _gid_to_name(self, gid):
    return grp.getgrgid(gid).gr_name

  def _name_to_gid(self, name):
    return grp.getgrnam(name).gr_gid

  def needs_fixing(self, path):
    for path in self._filter_violations(path):
      return True

    return False

  def fix(self, path):
    for change in self._filter_violations(path):
      os.chown(change[2], self._name_to_uid(change[0]), self._name_to_gid(change[1]))



