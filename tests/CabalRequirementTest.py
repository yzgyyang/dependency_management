import shutil
import unittest

from dependency_management.requirements.CabalRequirement import (
   CabalRequirement)


@unittest.skipIf(shutil.which('cabal') is None, 'Cabal is not installed.')
class CabalRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(CabalRequirement('cabal')), 'cabal')
        self.assertEqual(str(CabalRequirement('cabal', '1.24')), 'cabal 1.24')

    def test_installed_requirement(self):
        self.assertTrue(CabalRequirement('cabal').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(CabalRequirement('some_bad_package').is_installed())
