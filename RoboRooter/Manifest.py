
import copy
import logging


class Manifest(object):
    def __init__(self, version, path):
        self.version = version
        self.logger = logging.getLogger(__name__)
        self.path = path
        self.components = []

    def add_components(self, components):
        [self.add_component(component) for component in components]

    def add_component(self, component):
        if not component.applies_to_manifest(self):
            self.logger.warning(
                'Attempted to add %s component, but it does not apply to %s',
                component.__class__.__name__,
                self.path
            )
            return False

        self.logger.debug(
            'Added %s component to %s',
            component.__class__.__name__,
            self.path
        )


        local_component = copy.copy(component)
        local_component.load_state(self)
        self.components.append(local_component)

        return True
