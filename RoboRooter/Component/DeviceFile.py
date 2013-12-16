
import FileHint
import os
import stat

class DeviceFile(FileHint.FileHint):
  def __init__(self):
    self.hint_name = './manifests/devices'
    self.state_expression = r'^(.+)\s+(.+)$'
    self.rules = []

  def _filter_violations(self, path):
    for rule in self.rules:
      src_device = rule[0]
      target_device = os.path.join(path, rule[1])
      expected = self._extract_device_id(src_device)
      current = self._extract_device_id(target_device)
      if (expected != current):
        print("Expected %s to have device ID %s but was %s" % (target_device, expected, current))
        yield (src_device, target_device)

  def _extract_device_id(self, path):
    try:
      dev_stat = os.lstat(path)
      return dev_stat.st_rdev
    except:
      return None

  def _extract_device_mode(self, path):
    try:
      dev_stat = os.lstat(path)
      mode = 0
      if stat.S_ISBLK(dev_stat.st_mode):
        mode = stat.S_IFBLK
      elif stat.S_ISCHR(dev_stat.st_mode):
        mode = stat.S_IFCHR
      else:
        print("File is not a block or char: %s" % (path))
        raise IOError

      return mode
    except:
      return None


  def needs_fixing(self, path):
    for path in self._filter_violations(path):
      return True

    return False

  def fix(self, path):
    for change in self._filter_violations(path):
      if os.path.exists(change[1]):
        os.unlink(change[1])

      if not os.path.isdir(os.path.dirname(change[1])):
        os.makedirs(os.path.dirname(change[1]))

      print("Creating node at %s from %s" % (change[1], change[0]))
      dev_id = self._extract_device_id(change[0])
      dev_mode = self._extract_device_mode(change[0])
      os.mknod(change[1], dev_mode, dev_id)

