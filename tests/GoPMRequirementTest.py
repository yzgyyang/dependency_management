import shutil
import unittest

from dependency_management.requirements.GoPMRequirement import GoPMRequirement


@unittest.skipIf(shutil.which('gopm') is None, "Gopm is not installed.")
class GoRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(GoPMRequirement('fmt')), 'fmt')

    def test_installed_requirement(self):
        self.assertTrue(GoPMRequirement('fmt').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(GoPMRequirement('some_bad_package').is_installed())
