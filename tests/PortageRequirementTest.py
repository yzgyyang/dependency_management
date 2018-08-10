import unittest

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.PortageRequirement import (
    PortageRequirement)


@unittest.skipIf(not is_executable_exists('emerge'),
                 'Portage is not available on this platform')
class PortageRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(PortageRequirement('name1')),
                         'name1')
        self.assertEqual(str(PortageRequirement('name1', '1.2.3')),
                         'name1 1.2.3')

    def test_install_command_with_version(self):
        self.assertEqual(
            ['equery', '=name-19.2'],
            PortageRequirement('name', '19.2').install_command())

    def test_install_command_without_version(self):
        self.assertEqual(['equery', 'name'],
                         PortageRequirement('name').install_command())

    def test_installed_requirement(self):
        self.assertTrue(
            PortageRequirement('portage').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            PortageRequirement('some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(PortageRequirement('portage', '0')
                        .is_installed())

    def test_not_installed_requirement_because_version(self):
        self.assertFalse(PortageRequirement('portage', '1000000')
                         .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(PortageRequirement('some_bad_package', '1')
                         .is_installed())

    def test_uninstall_requirement(self):
        p = PortageRequirement('app-portage/eix')
        self.assertEqual(p.install_package(), 0)
        self.assertTrue(p.is_installed())
        p.uninstall_package()
        self.assertFalse(p.is_installed())
