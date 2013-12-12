#!/usr/bin/env python

from RoboRooter import ConfigLoader
import pprint


config = ConfigLoader('./example/roborooter.ini')
pprint.pprint(config.sources_path())


