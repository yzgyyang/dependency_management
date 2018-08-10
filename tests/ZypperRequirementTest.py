import unittest

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.ZypperRequirement import (
    ZypperRequirement)


@unittest.skipIf(not is_executable_exists('zypper'),
                 'Zypper is not available on this platform')
class ZypperRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(ZypperRequirement('name1')),
                         'name1')
        self.assertEqual(str(ZypperRequirement('name1', '1.2.3')),
                         'name1 1.2.3')

    def test_install_command_with_version(self):
        self.assertEqual(
            ['zypper', '--non-interactive', 'install', 'name-19.2'],
            ZypperRequirement('name', '19.2').install_command())

    def test_install_command_without_version(self):
        self.assertEqual(['zypper', '--non-interactive', 'install', 'name'],
                         ZypperRequirement('name').
                         install_command())

    def test_installed_requirement(self):
        self.assertTrue(ZypperRequirement('zypper').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            ZypperRequirement('some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(ZypperRequirement('zypper', '0')
                        .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(ZypperRequirement('some_bad_package', '1')
                         .is_installed())

    def test_install_package(self):
        p = ZypperRequirement('qemu')
        self.assertEqual(p.install_package(), 0)
        self.assertTrue(p.is_installed())
