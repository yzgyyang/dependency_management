import shutil
import unittest

from dependency_management.requirements.RscriptRequirement import (
    RscriptRequirement)


@unittest.skipIf(shutil.which('R') is None, "R is not installed.")
class RscriptRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(RscriptRequirement('base')), 'base')
        self.assertEqual(str(RscriptRequirement('base', '3.5')), 'base 3.5')

    def test_installed_requirement(self):
        self.assertTrue(RscriptRequirement('base').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(RscriptRequirement('some_bad_package').is_installed())
