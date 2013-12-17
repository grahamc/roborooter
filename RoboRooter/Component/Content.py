
import FileHint
import hashlib
import shutil
import os

class Content(FileHint.FileHint):
  def __init__(self):
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
      rule_path = os.path.join(path, rule[1])
      origin_path = os.path.join(self.origin, rule[1])

      try:
        expected = rule[0]
        current = self._calculate_md5(rule_path)
        if current != expected:
          print "Expected %s hash to match %s but was %s" % (
            rule_path,
            expected,
            current
          )
          yield (origin_path, rule_path)
      except(OSError):
        continue

  def fix(self, path):
    for change in self._filter_violations(path):
      if not os.path.isdir(os.path.dirname(change[1])):
        os.makedirs(os.path.dirname(change[1]))
      shutil.copyfile(change[0], change[1])

  def _calculate_md5(self, filename):
    md5 = hashlib.md5()
    try:
      with open(filename, 'r') as f:
        for chunk in iter(lambda: f.read(256*128), b''):
          md5.update(chunk)
    except(IOError):
      return None

    return md5.hexdigest()

