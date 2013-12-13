#!/usr/bin/env python

from RoboRooter.ConfigLoader import ConfigLoader
from RoboRooter.ManifestLoader import ManifestLoader
from RoboRooter.Component.Permission import Permission
from RoboRooter.Component.Owner import Owner
from RoboRooter.Component.Content import Content
import pprint
import os


config = ConfigLoader('./example/roborooter.ini')
manifest_loader = ManifestLoader(config.get_config())
manifest_loader.add_component(Permission())
manifest = manifest_loader.get_manifest_by_version(1)

perm = Permission()
perm.load_state(manifest)

owner = Owner()
owner.load_state(manifest)

content = Content()
content.set_origin(os.path.join(manifest.path, './sources/'))
content.load_state(manifest)

path = './example/target/'

if content.needs_fixing(path):
  content.fix('./example/target')
else:
  print "Content does not resolving."

if perm.needs_fixing(path):
  perm.fix('./example/target')
else:
  print "Permissions do not resolving."


if owner.needs_fixing(path):
  owner.fix('./example/target')
else:
  print "Ownership do not resolving."

