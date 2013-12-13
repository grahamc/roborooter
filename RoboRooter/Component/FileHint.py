
import re
import os.path

class FileHint(object):
  def applies_to_manifest(self, manifest):
    return os.path.isfile(os.path.join(manifest.path, self.hint_name))

  def load_state(self, manifest):
    self._load_state_via_regex(manifest)

  def _load_state_via_regex(self, manifest):
    prog = re.compile(self.state_expression)
    filename = os.path.join(manifest.path, self.hint_name)
    for line in open(filename, 'r'):
      matches = prog.match(line)
      if matches:
        self.rules.append(matches.groups())
