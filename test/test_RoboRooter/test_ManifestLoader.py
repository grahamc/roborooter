
import unittest
import os

import RoboRooter.ManifestLoader as ManifestLoader
import RoboRooter.Manifest as Manifest

class test_ManifestLoader(unittest.TestCase):
  def setUp(self):
    self.loader = ManifestLoader(
        {'sources_path': './test/test_RoboRooter/fixtures-ManifestLoader'}
        )
  def test_get_manifest_versions(self):
    self.assertEqual(
        self.loader.get_manifest_versions(),
        [1, 2, 123232434234]
      )

  def test_get_manifest_by_version_invalid_returns_None(self):
    manifest = self.loader.get_manifest_by_version('abc123')
    self.assertEqual(manifest, None)

  def test_get_manifest_by_version_valid_returns_Manifest(self):
    manifest = self.loader.get_manifest_by_version(1)
    self.assertIsInstance(manifest, Manifest)

  def test_get_manifest_by_version_manifest_has_version(self):
    manifest = self.loader.get_manifest_by_version(1)
    self.assertEqual(manifest.version, 1)

  def test_get_manifest_by_version_manifest_has_path(self):
    manifest = self.loader.get_manifest_by_version(1)
    self.assertEqual(manifest.path, './test/test_RoboRooter/fixtures-ManifestLoader/1')

  def test_add_component_with_none_fails(self):
    with self.assertRaises(ValueError):
      self.loader.add_component(None)

  def test_add_component_with_component_accepts(self):
    self.assertEqual(
        self.loader.add_component(True),
        True
      )
