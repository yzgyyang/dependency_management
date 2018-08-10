import unittest

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.DnfRequirement import (
    DnfRequirement)


@unittest.skipIf(not is_executable_exists('dnf'),
                 'Dnf is not available on this platform')
class DnfRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(DnfRequirement('name1')),
                         'name1')
        self.assertEqual(str(DnfRequirement('name1', '1.2.3')),
                         'name1 1.2.3')

    def test_install_command_with_version(self):
        self.assertEqual(
            ['dnf', 'install', '--assumeyes', 'name-19.2'],
            DnfRequirement('name', '19.2').install_command())

    def test_install_command_without_version(self):
        self.assertEqual(['dnf', 'install', '--assumeyes', 'name'],
                         DnfRequirement('name').install_command())

    def test_installed_requirement(self):
        self.assertTrue(DnfRequirement('dnf').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DnfRequirement('some_bad_package').is_installed())
        self.assertFalse(
            DnfRequirement('dnf', '100000').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(DnfRequirement('dnf', '0')
                        .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(DnfRequirement('some_bad_package', '1')
                         .is_installed())

    def test_install_package(self):
        p = DnfRequirement('tito')
        self.assertEqual(p.install_package(), 0)
        self.assertTrue(p.is_installed())
