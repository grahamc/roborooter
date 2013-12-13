#!/usr/bin/env python

from RoboRooter.ConfigLoader import ConfigLoader
from RoboRooter.ManifestLoader import ManifestLoader
from RoboRooter.Component.Permission import Permission
from RoboRooter.Component.Owner import Owner
import pprint


config = ConfigLoader('./example/roborooter.ini')
manifest_loader = ManifestLoader(config.get_config())
manifest_loader.add_component(Permission())
manifest = manifest_loader.get_manifest_by_version(1)

perm = Permission()
perm.load_state(manifest)

owner = Owner()
owner.load_state(manifest)

pprint.pprint(perm.needs_fixing('./example/target'))
pprint.pprint(owner.needs_fixing('./example/target'))
perm.fix('./example/target')
owner.fix('./example/target')



