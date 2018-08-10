import unittest

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.BrewRequirement import (
    BrewRequirement)


@unittest.skipIf(not is_executable_exists('brew'),
                 'Brew is not available on this platform')
class BrewRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(BrewRequirement('name1')),
                         'name1')
        self.assertEqual(str(BrewRequirement('name1', '1.2.3')),
                         'name1 1.2.3')

    def test_install_command_with_version(self):
        self.assertEqual(
            ['brew', 'install', 'name@19.2'],
            BrewRequirement('name', '19.2').install_command())

    def test_install_command_without_version(self):
        self.assertEqual(['brew', 'install', 'name'],
                         BrewRequirement('name').install_command())

    def test_installed_requirement(self):
        self.assertTrue(BrewRequirement('python3').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            BrewRequirement('some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(BrewRequirement('python3', '0')
                        .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(BrewRequirement('some_bad_package', '1')
                         .is_installed())

    def test_install_package(self):
        p = BrewRequirement('postgresql')
        self.assertEqual(p.install_package(), 0)
        self.assertTrue(p.is_installed())
