import shutil
import unittest

from dependency_management.requirements.RscriptRequirement import (
    RscriptRequirement)


@unittest.skipIf(shutil.which('R') is None, "R is not installed.")
class RscriptRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(RscriptRequirement('base')), 'base')

    def test_installed_requirement(self):
        self.assertTrue(RscriptRequirement('base').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(RscriptRequirement('some_bad_package').is_installed())

    def test_not_implemented_error(self):
        """
        Test the 'NotImplementedError' raised if version provided
        """
        with self.assertRaisesRegex(NotImplementedError,
                                    r'^Setting version '):
            RscriptRequirement('base', '3.5')
