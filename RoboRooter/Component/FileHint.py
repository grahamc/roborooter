
class FileHint:
  def applies_to_manifest(self, manifest):
    return os.path.isfile(os.path.join(manifest.path, self.hint_name))

