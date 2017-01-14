import unittest
import shutil

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@unittest.skipIf(not is_executable_exists('apt-get'),
                 'APT is not available on this platform')
class APTDistributionRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(DistributionRequirement(apt_get='apt').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(apt_get='some_bad_package').is_installed())


@unittest.skipIf(not is_executable_exists('dnf'),
                 'DNF is not available on this platform')
class DNFDistributionRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(DistributionRequirement(dnf='dnf').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(dnf='some_bad_package').is_installed())


@unittest.skipIf(not is_executable_exists('pacman'),
                 'Pacman is not available on this platform')
class PacmanDistributionRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(
            DistributionRequirement(pacman='pacman').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(pacman='some_bad_package').is_installed())


@unittest.skipIf(not is_executable_exists('emerge'),
                 'Portage is not available on this platform')
class PortageDistributionRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(
            DistributionRequirement(portage='portage').is_installed())

    def test_not_installed_requirement(self):
        self.assertTrue(
            DistributionRequirement(portage='some_bad_package').is_installed())


@unittest.skipIf(not is_executable_exists('xbps-install'),
                 'XBPS is not available on this platform')
class XBPSDistributionRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(DistributionRequirement(xbps='xbps').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(xbps='some_bad_package').is_installed())


@unittest.skipIf(not is_executable_exists('yum'),
                 'YUM is not available on this platform')
class YUMDistributionRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(DistributionRequirement(yum='yum').is_installed() or
                        DistributionRequirement(yum='dnf-yum').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(yum='some_bad_package').is_installed())


@unittest.skipIf(not is_executable_exists('zypper'),
                 'Zypper is not available on this platform')
class ZypperDistributionRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(
            DistributionRequirement(zypper='zypper').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(zypper='some_bad_package').is_installed())


class ExpectedErrorsDistributionRequirementTestCase(unittest.TestCase):

    NO_SUPPORTED_PACKAGE_MANAGER_RE = ("This platform doesn't have any of the "
                                       'supported package manager')

    def test_no_supported_package_manager(self):
        self.assertRaisesRegex(NotImplementedError,
                               self.NO_SUPPORTED_PACKAGE_MANAGER_RE,
                               DistributionRequirement()
                               .get_available_package_manager())

    def test_platform_without_supported_package_manager(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertRaisesRegex(NotImplementedError,
                                   self.NO_SUPPORTED_PACKAGE_MANAGER_RE,
                                   DistributionRequirement(apt_get='apt',
                                                           dnf='dnf',
                                                           pacman='pacman',
                                                           portage='portage',
                                                           xbps='xbps',
                                                           yum='yum',
                                                           zypper='zypper')
                                   .get_available_package_manager())
        finally:
            shutil.which = _shutil_which
