#!/usr/bin/env python

from RoboRooter.ConfigLoader import ConfigLoader
from RoboRooter.ManifestLoader import ManifestLoader
from RoboRooter.Component.Permission import Permission
import pprint


config = ConfigLoader('./example/roborooter.ini')
manifest_loader = ManifestLoader(config.get_config())
manifest_loader.add_component(Permission())
manifest = manifest_loader.get_manifest_by_version(1)

pprint.pprint(manifest.components)

