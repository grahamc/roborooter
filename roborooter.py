#!/usr/bin/env python

from RoboRooter import ConfigLoader
from RoboRooter import ManifestLoader
from RoboRooter import Component
import pprint


config = ConfigLoader('./example/roborooter.ini')
manifest_loader = ManifestLoader(config.get_config())
manifest_loader.add_component(Component.Permission())
manifest = manifest_loader.get_manifest_by_version(1)
pprint.pprint(manifest.components)

