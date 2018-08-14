import unittest

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.PkgRequirement import (
    PkgRequirement)


@unittest.skipIf(not is_executable_exists('pkg'),
                 'Pkg is not available on this platform')
class PkgRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(PkgRequirement('name1')),
                         'name1')
        self.assertEqual(str(PkgRequirement('name1', '1.2.3')),
                         'name1 1.2.3')

    def test_install_command_with_version(self):
        self.assertEqual(
            ['pkg', 'install', '--yes', 'name'],
            PkgRequirement('name', '19.2').install_command())

    def test_install_command_without_version(self):
        self.assertEqual(['pkg', 'install', '--yes', 'name'],
                         PkgRequirement('name').install_command())

    def test_installed_requirement(self):
        self.assertTrue(PkgRequirement('pkg').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            PkgRequirement('some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(PkgRequirement('python3', '0')
                        .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(PkgRequirement('some_bad_package', '1')
                         .is_installed())

    def test_install_package(self):
        p = PkgRequirement('htop')
        self.assertEqual(p.install_package(), 0)
        self.assertTrue(p.is_installed())
