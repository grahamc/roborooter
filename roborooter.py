#!/usr/bin/env python

from RoboRooter import ConfigLoader
from RoboRooter import ManifestLoader
import pprint


config = ConfigLoader('./example/roborooter.ini')
manifest_loader = ManifestLoader(config)
pprint.pprint(manifest_loader.get_manifest_versions())

