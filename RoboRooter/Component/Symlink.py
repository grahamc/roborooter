

import FileHint
import os

class Symlink(FileHint.FileHint):
  def __init__(self):
    self.hint_name = './manifests/symlinks'
    self.state_expression = r'^(.+)\s+(.+)$'
    self.rules = []

  def _filter_violations(self, path):
    for rule in self.rules:
      link_src = self._relativize_link(rule[0], rule[1])
      link_dest = os.path.join(path, rule[1])

      if not self._is_path_linking_to_location(link_src, link_dest):
        print("Expected %s to link to %s" % (link_src, link_dest))
        yield (link_src, link_dest)

  def _relativize_link(self, source, target):
      src_dir = os.path.dirname(source)
      src_file = os.path.basename(source)
      target_dir = os.path.dirname(target)

      relative_location = os.path.relpath(src_dir, target_dir)

      link_src = os.path.join(relative_location, src_file)

      return link_src


  def _is_path_linking_to_location(self, source, target):
    if not os.path.exists(target):
      return False

    if not os.path.islink(target):
      return False

    if os.readlink(target) != source:
      return False

    return True



  def fix(self, path):
    for change in self._filter_violations(path):
      os.symlink(change[0], change[1])



