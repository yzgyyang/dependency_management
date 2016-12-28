import shutil
import unittest
from dependency_management.requirements.RscriptRequirement import (
    RscriptRequirement)


@unittest.skipIf(shutil.which('R') is None, "R is not installed.")
class RscriptRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(RscriptRequirement('base').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(RscriptRequirement('some_bad_package').is_installed())
