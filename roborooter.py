#!/usr/bin/env python

from RoboRooter.LoggerConfiguration import LoggerConfiguration
from RoboRooter.CommandLine import CommandLine
from RoboRooter.ConfigLoader import ConfigLoader
from RoboRooter.ManifestLoader import ManifestLoader
from RoboRooter.Component.Permission import Permission
from RoboRooter.Component.Owner import Owner
from RoboRooter.Component.DeviceFile import DeviceFile
from RoboRooter.Component.Content import Content
from RoboRooter.Component.Whitelist import Whitelist
from RoboRooter.Component.Symlink import Symlink
from RoboRooter.Component.RoboVersioning import RoboVersioning
import sys
import pprint
import logging

cli = CommandLine()
(options, args) = cli.parse()
LoggerConfiguration().configureByOptions(options)

config = ConfigLoader(options.config)
if options.minimum_version and int(options.minimum_version):
    config.override('minimum_version', options.minimum_version)

manifest_loader = ManifestLoader(config.get_config())
manifest_loader.add_component(Content())
manifest_loader.add_component(DeviceFile())
manifest_loader.add_component(Symlink())
manifest_loader.add_component(Permission())
manifest_loader.add_component(Owner())
manifest_loader.add_component(Whitelist())
manifest_loader.add_component(RoboVersioning())


def do_things_on_path(path):
    logger = logging.getLogger(__name__)
    manifest = manifest_loader.get_manifest_for_path(path)

    if manifest is None:
        logger.critical('No manifest found for %s', path)
        return None

    fixes = 1
    attempts = 0
    max_attempts = 1
    while fixes > 0 and attempts < 1:
        fixes = 0
        attempts += 1
        for comp in manifest.components:
            name = comp.__class__.__name__

            needs_fixing = comp.needs_fixing(path, process_all=options.dry_run)

            if needs_fixing:
                fixes += 1
                if not options.dry_run and options.actually_run:
                    comp.fix(path)

        if options.dry_run:
            logger.info(
                'Would have made %d fixes on attempt %d to path %s',
                fixes,
                attempts,
                path
            )
        else:
            logger.info(
                'Made %d fixes on attempt %d to path %s',
                fixes,
                attempts,
                path
            )

r = [do_things_on_path(x) for x in args]
