
import unittest
from RoboRooter.Manifest import Manifest
from RoboRooter.Component.Noop import Noop

class test_Manifest(unittest.TestCase):
  def test_version(self):
    manifest = Manifest(1, None)
    self.assertEqual(manifest.version, 1)

  def test_path(self):
    manifest = Manifest(None, '/foo/bar')
    self.assertEqual(manifest.path, '/foo/bar')

  def test_add_component(self):

    passing_noop_1 = Noop(True)
    passing_noop_2 = Noop(True)
    manifest = Manifest(None, None)
    manifest.add_component(passing_noop_1)
    manifest.add_component(passing_noop_2)

    self.assertEqual(manifest.components, [passing_noop_1, passing_noop_2])

  def test_add_components(self):
    passing_noop = Noop(True)
    manifest = Manifest(None, None)
    manifest.add_components([passing_noop, Noop(False)])

    self.assertEqual(manifest.components, [passing_noop])

