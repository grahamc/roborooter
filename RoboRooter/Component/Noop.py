
import random


class Noop(object):
    def __init__(self, applies=True):
        self.applies = applies
        self.state = random.random()

    def load_state(self, manifest):
        return True

    def applies_to_manifest(self, manifest):
        return self.applies

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class NoopFailing(Noop):
    def __init__(self):
        super(Noop, self).__init__()
        self.applies = False
