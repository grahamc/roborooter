
import unittest
from RoboRooter.Manifest import Manifest
from RoboRooter.Component.Noop import Noop
from RoboRooter.Component.Noop import NoopFailing


class test_Manifest(unittest.TestCase):
    def test_version(self):
        manifest = Manifest(1, None)
        self.assertEqual(manifest.version, 1)

    def test_path(self):
        manifest = Manifest(None, '/foo/bar')
        self.assertEqual(manifest.path, '/foo/bar')

    def test_add_component(self):

        passing_noop = Noop
        manifest = Manifest(None, None)
        manifest.add_component(passing_noop)

        self.assertIsInstance(manifest.components[0], Noop)

    def test_add_components(self):
        passing_noop = Noop
        manifest = Manifest(None, None)
        manifest.add_components([passing_noop, NoopFailing])

        self.assertEqual(1, len(manifest.components))
        self.assertIsInstance(manifest.components[0], Noop)
