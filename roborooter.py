#!/usr/bin/env python

from optparse import OptionParser
from RoboRooter.ConfigLoader import ConfigLoader
from RoboRooter.ManifestLoader import ManifestLoader
from RoboRooter.Component.Permission import Permission
from RoboRooter.Component.Owner import Owner
from RoboRooter.Component.DeviceFile import DeviceFile
from RoboRooter.Component.Content import Content
from RoboRooter.Component.Whitelist import Whitelist
from RoboRooter.Component.Symlink import Symlink
import sys
import pprint
import logging


parser = OptionParser()
parser.add_option('-c', '--config', dest='config',
                  default='/etc/roborooter.ini',
                  help='load roborooter config from CONFIG')
parser.add_option('-v', '--verbose',
                  action='count',
                  default=False, dest="verbose")
parser.add_option('-q', '--quiet',
                  action='count',
                  default=False, dest="quiet")


(options, args) = parser.parse_args()

# Calculate log level
log_level = 3
if options.verbose is not False:
    log_level += options.verbose
if options.quiet is not False:
    log_level -= options.quiet

if log_level >= 5:
    logging.setLevel(logging.DEBUG)
elif log_level == 4:
    logging.setLevel(logging.INFO)
elif log_level == 3:
    logging.setLevel(logging.WARNING)
elif log_level == 2:
    logging.setLevel(logging.ERROR)
elif log_level <= 1:
    logging.setLevel(logging.CRITICAL)
else:
    msg = 'Could not determine log level from integer %d' % log_level
    raise ValueError(msg)

pprint.pprint(log_level)


pprint.pprint((options, args))
sys.exit(1)
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
