import unittest

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.YumRequirement import (
    YumRequirement)


@unittest.skipIf(not is_executable_exists('yum'),
                 'Yum is not available on this platform')
class YumRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(YumRequirement('name1')),
                         'name1')
        self.assertEqual(str(YumRequirement('name1', '1.2.3')),
                         'name1 1.2.3')

    def test_install_command_with_version(self):
        self.assertEqual(
            ['yum', 'install', '--assumeyes', 'name-19.2'],
            YumRequirement('name', '19.2').install_command())

    def test_install_command_without_version(self):
        self.assertEqual(['yum', 'install', '--assumeyes', 'name'],
                         YumRequirement('name').install_command())

    def test_installed_requirement(self):
        self.assertTrue(YumRequirement('yum').is_installed() or
                        YumRequirement('dnf-yum').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            YumRequirement('some_bad_package').is_installed())

    def test_installing_requirement_version(self):
        p = YumRequirement('httpd')
        self.assertEqual(p.install_package(), 0)
        self.assertTrue(p.is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(YumRequirement('some_bad_package', '1')
                         .is_installed())
