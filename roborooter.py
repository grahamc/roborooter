#!/usr/bin/env python

from RoboRooter.ConfigLoader import ConfigLoader
from RoboRooter.ManifestLoader import ManifestLoader
from RoboRooter.Component.Permission import Permission
from RoboRooter.Component.Owner import Owner
from RoboRooter.Component.DeviceFile import DeviceFile
from RoboRooter.Component.Content import Content
from RoboRooter.Component.Whitelist import Whitelist
from RoboRooter.Component.Symlink import Symlink


config = ConfigLoader('./example/roborooter.ini')
manifest_loader = ManifestLoader(config.get_config())
manifest_loader.add_component(Content())
manifest_loader.add_component(DeviceFile())
manifest_loader.add_component(Symlink())
manifest_loader.add_component(Permission())
manifest_loader.add_component(Owner())
manifest_loader.add_component(Whitelist())
manifest = manifest_loader.get_manifest_by_version(1)

path = './example/target/'

fixes = 1
attempts = 0
max_attempts = 1
while fixes > 0 and attempts < 1:
  fixes = 0
  attempts += 1
  for comp in manifest.components:
    name = comp.__class__.__name__

    needs_fixing = comp.needs_fixing(path)
    print "%s: %s" % (name, needs_fixing)

    if needs_fixing:
      fixes += 1
      comp.fix(path)
  print "Made %d fixes on attempt %d" % (fixes, attempts)


