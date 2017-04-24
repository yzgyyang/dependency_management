import shutil
import unittest

from dependency_management.requirements.GoRequirement import GoRequirement


@unittest.skipIf(shutil.which('go') is None, "Go is not installed.")
class GoRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(GoRequirement('fmt')), 'fmt')

    def test_installed_requirement(self):
        self.assertTrue(GoRequirement('fmt').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(GoRequirement('some_bad_package').is_installed())
