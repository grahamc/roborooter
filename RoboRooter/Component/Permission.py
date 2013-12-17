
import FileHint
import os

class Permission(FileHint.FileHint):
    def __init__(self):
        self.hint_name = './manifests/permissions'
        self.state_expression = r'^\w*:\w* (\d*) (.*)$'
        self.rules = []

    def _filter_violations(self, path):
        for rule in self.rules:
            rule_path = os.path.join(path, rule[1])
            try:
                expected = int(rule[0], 8)
                current = os.stat(rule_path).st_mode & 0777
                if current != expected:
                    print "Expected %s to have %o but was %o" % (
                        rule_path,
                        expected,
                        current
                    )
                    yield (expected, rule_path)
            except(OSError):
                continue


    def fix(self, path):
        for change in self._filter_violations(path):
            os.chmod(change[1], change[0])



