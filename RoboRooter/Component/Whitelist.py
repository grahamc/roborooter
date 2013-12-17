
import FileHint
import hashlib
import shutil
import os

class Whitelist(FileHint.FileHint):
    def __init__(self):
        self.hint_name = './manifests/whitelist'
        self.state_expression = r'^(.+)$'
        self.rules = []

        self.files = []
        self.directories = []

    def load_state(self, manifest):
        self._load_state_via_regex(manifest)

        for rule in self.rules:
            path = rule[0]
            if path[-1] == '/':
                self.directories.append(path)
            else:
                self.files.append(path)

    def _filter_violations(self, root_path, rel='./'):
        path = os.path.join(root_path, rel)
        for entry in os.listdir(path):
            scoped_path = os.path.join('./', os.path.normpath(os.path.join(rel, entry)))
            absolute_path = os.path.join('./', os.path.normpath(os.path.join(root_path, rel, entry)))
            if os.path.isfile(absolute_path):
                if scoped_path in self.files:
                    continue
                else:
                    print "Would remove %s" % (absolute_path)
                    yield absolute_path
            elif os.path.isdir(absolute_path):
                if scoped_path in self.directories:
                    continue
                else:
                    for yield_path in self._filter_violations(root_path, scoped_path):
                        yield yield_path



    def fix(self, path):
        for change in self._filter_violations(path):
            os.remove(change)

