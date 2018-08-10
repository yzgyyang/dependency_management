import unittest

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.AptRequirement import (
    AptRequirement)


@unittest.skipIf(not is_executable_exists('apt-get'),
                 'Apt is not available on this platform')
class AptRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(AptRequirement('name1')),
                         'name1')
        self.assertEqual(str(AptRequirement('name1', '1.2.3')),
                         'name1 1.2.3')

    def test_install_command_with_version(self):
        self.assertEqual(
            ['apt-get', 'install', '--yes', 'name=19.2'],
            AptRequirement('name', '19.2').install_command())

    def test_install_command_without_version(self):
        self.assertEqual(['apt-get', 'install', '--yes', 'name'],
                         AptRequirement('name').install_command())

    def test_installed_requirement(self):
        self.assertTrue(AptRequirement('apt').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            AptRequirement('some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(AptRequirement('apt', '1.6.1')
                        .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(AptRequirement('some_bad_package', '1')
                         .is_installed())

    def test_install_package(self):
        p = AptRequirement('vim')
        self.assertEqual(p.install_package(), 0)
        self.assertTrue(p.is_installed())
