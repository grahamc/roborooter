
import unittest
import logging
from RoboRooter.ConfigLoader import ConfigLoader


class test_ConfigLoader(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=100)
        self.root_path = 'test/test_RoboRooter/fixtures-ConfigLoader/'
        self.empty_config = ConfigLoader(
            '%s/empty.ini' % self.root_path
        ).get_config()
        self.full_config = ConfigLoader(
            '%s/full.ini' % self.root_path
        ).get_config()
        self.relative_config = ConfigLoader(
            '%s/relative.ini' % self.root_path
        ).get_config()

    # Defaults
    def test_default_sources_path(self):
        self.assertEqual(
            self.empty_config['sources_path'],
            '/usr/local/roborooter/'
        )

    def test_default_minimum_version(self):
        self.assertEqual(
            self.empty_config['minimum_version'],
            1
        )

    def test_default_default_version(self):
        self.assertEqual(
            self.empty_config['default_version'],
            1
        )

    # Parsed version
    def test_parsed_minimum_version(self):
        self.assertEqual(
            self.full_config['minimum_version'],
            5
        )

    def test_parsed_default_version(self):
        self.assertEqual(
            self.full_config['default_version'],
            123
        )

    # Relative / absolute configuration paths
    def test_parsed_sources_path_absolute(self):
        self.assertEqual(
            self.full_config['sources_path'],
            '/path/to/sources'
            )

    def test_parsed_sources_path_relative(self):
        self.assertEqual(
            self.relative_config['sources_path'],
            '%s./path/to/sources' % self.root_path
            )

    # Handle the where the default version is less than the minimum version
    def test_minimum_version_above_default_version(self):
        with self.assertRaises(ValueError):
            ConfigLoader(
                '%s/default_version_below_minimum.ini' % self.root_path
            )
