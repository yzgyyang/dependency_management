import shutil
import unittest

import sarge

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@unittest.skipIf(not is_executable_exists('apt-get'),
                 'APT is not available on this platform')
class APTDistributionRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(DistributionRequirement(apt_get='apt')), 'apt')

    def test_installed_requirement(self):
        self.assertTrue(DistributionRequirement(apt_get='apt').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(apt_get='some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(DistributionRequirement(version='0', apt_get='apt')
                        .is_installed())

    def test_not_installed_requirement_because_version(self):
        self.assertFalse(DistributionRequirement(version='1000000',
                                                 apt_get='apt').is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(DistributionRequirement(version='1',
                                                 apt_get='some_bad_package')
                         .is_installed())


@unittest.skipIf(not is_executable_exists('brew'),
                 'Brew is not available on this platform')
class BrewDistributionRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(DistributionRequirement(brew='python3')),
                         'python3')

    def test_installed_requirement(self):
        self.assertTrue(DistributionRequirement(brew='python3').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(brew='some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(DistributionRequirement(version='0', brew='python3')
                        .is_installed())

    def test_not_installed_requirement_because_version(self):
        self.assertFalse(DistributionRequirement(version='1000000',
                                                 brew='python3').is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(DistributionRequirement(version='1',
                                                 brew='some_bad_package')
                         .is_installed())


@unittest.skipIf(not is_executable_exists('dnf'),
                 'DNF is not available on this platform')
class DNFDistributionRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(DistributionRequirement(dnf='dnf')), 'dnf')

    def test_installed_requirement(self):
        self.assertTrue(DistributionRequirement(dnf='dnf').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(dnf='some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(DistributionRequirement(version='0', dnf='dnf')
                        .is_installed())

    def test_not_installed_requirement_because_version(self):
        self.assertFalse(DistributionRequirement(version='1000000', dnf='dnf')
                         .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(DistributionRequirement(version='1',
                                                 dnf='some_bad_package')
                         .is_installed())


@unittest.skipIf(not is_executable_exists('pacman'),
                 'Pacman is not available on this platform')
class PacmanDistributionRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(DistributionRequirement(pacman='pacman')),
                         'pacman')

    def test_installed_requirement(self):
        self.assertTrue(
            DistributionRequirement(pacman='pacman').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(pacman='some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(DistributionRequirement(version='0', pacman='pacman')
                        .is_installed())

    def test_not_installed_requirement_because_version(self):
        self.assertFalse(DistributionRequirement(version='1000000',
                                                 pacman='pacman')
                         .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(DistributionRequirement(version='1',
                                                 pacman='some_bad_package')
                         .is_installed())


@unittest.skipIf(not is_executable_exists('pkg'),
                 'PKG is not available on this platform')
class PKGDistributionRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(DistributionRequirement(pkg='pkg')),
                         'pkg')

    def test_installed_requirement(self):
        self.assertTrue(
            DistributionRequirement(pkg='pkg').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(pkg='some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(DistributionRequirement(version='0', pkg='pkg')
                        .is_installed())

    def test_not_installed_requirement_because_version(self):
        self.assertFalse(DistributionRequirement(version='1000000',
                                                 pkg='pkg')
                         .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(DistributionRequirement(version='1',
                                                 pkg='some_bad_package')
                         .is_installed())


@unittest.skipIf(not is_executable_exists('emerge'),
                 'Portage is not available on this platform')
class PortageDistributionRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(DistributionRequirement(portage='portage')),
                         'portage')

    def test_installed_requirement(self):
        self.assertTrue(
            DistributionRequirement(portage='portage').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(portage='some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(DistributionRequirement(version='0', portage='portage')
                        .is_installed())

    def test_not_installed_requirement_because_version(self):
        self.assertFalse(DistributionRequirement(version='1000000',
                                                 portage='portage')
                         .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(DistributionRequirement(version='1',
                                                 portage='some_bad_package')
                         .is_installed())


@unittest.skipIf(not is_executable_exists('xbps-install'),
                 'XBPS is not available on this platform')
class XBPSDistributionRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(DistributionRequirement(xbps='xbps')), 'xbps')

    def test_installed_requirement(self):
        self.assertTrue(DistributionRequirement(xbps='xbps').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(xbps='some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(DistributionRequirement(version='0', xbps='xbps')
                        .is_installed())

    def test_not_installed_requirement_because_version(self):
        self.assertFalse(DistributionRequirement(version='1000000', xbps='xbps')
                         .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(DistributionRequirement(version='1',
                                                 xbps='some_bad_package')
                         .is_installed())


@unittest.skipIf(not is_executable_exists('yum'),
                 'YUM is not available on this platform')
class YUMDistributionRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(DistributionRequirement(yum='yum')), 'yum')

    def test_installed_requirement(self):
        self.assertTrue(DistributionRequirement(yum='yum').is_installed() or
                        DistributionRequirement(yum='dnf-yum').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(yum='some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(DistributionRequirement(version='0', yum='yum')
                        .is_installed() or
                        DistributionRequirement(version='0', yum='dnf-yum')
                        .is_installed())

    def test_not_installed_requirement_because_version(self):
        self.assertFalse(DistributionRequirement(version='1000000', yum='yum')
                         .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(DistributionRequirement(version='1',
                                                 yum='some_bad_package')
                         .is_installed())


@unittest.skipIf(not is_executable_exists('zypper'),
                 'Zypper is not available on this platform')
class ZypperDistributionRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(DistributionRequirement(zypper='zypper')),
                         'zypper')

    def test_installed_requirement(self):
        self.assertTrue(
            DistributionRequirement(zypper='zypper').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            DistributionRequirement(zypper='some_bad_package').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(DistributionRequirement(version='0', zypper='zypper')
                        .is_installed())

    def test_not_installed_requirement_because_version(self):
        self.assertFalse(DistributionRequirement(version='1000000',
                                                 zypper='zypper')
                         .is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(DistributionRequirement(version='1',
                                                 zypper='some_bad_package')
                         .is_installed())


class DistributionDiffstatRequirementTestCase(unittest.TestCase):

    def test_install(self):
        r = DistributionRequirement('diffstat')
        self.assertEqual(r.install_package(), 0)
        self.assertTrue(r.is_installed())


class ExpectedErrorsDistributionRequirementTestCase(unittest.TestCase):

    NO_SUPPORTED_PACKAGE_MANAGER_RE = ("This platform doesn't have any of the "
                                       'supported package manager')
    NO_SPECIFIED_PACKAGE_MANAGER_RE = (
        "This platform doesn't have any of the "
        'specified package manager')

    def _mock_test(self, managers, commands, exc=None, message=None):
        _shutil_which = shutil.which
        dr = DistributionRequirement(**commands)
        old_managers = dr._available_managers
        dr._manager = None

        if isinstance(managers, dict):
            allowed_exes = managers.values()
            dr._available_managers = managers.keys()
        else:
            allowed_exes = list(exe for manager, exe
                                in dr.SUPPORTED_PACKAGE_MANAGERS.items()
                                if manager in managers)
            dr._available_managers = None

        def fake_which(exe):
            if exe in allowed_exes:
                return True

        try:
            shutil.which = fake_which

            if not exc:
                # Force caching of all package managers
                dr.package_managers
                return dr

            with self.assertRaisesRegex(
                    exc,
                    message):
                dr.get_available_package_manager()
        finally:
            dr._available_managers = old_managers
            shutil.which = _shutil_which

    def test_no_manager_commands(self):
        with self.assertRaisesRegex(
                NotImplementedError,
                'No package managers specified'):
            DistributionRequirement()

        with self.assertRaisesRegex(
                TypeError,
                'No package managers specified'):
            DistributionRequirement()

    def test_platform_without_supported_package_manager(self):
        pm_packages = DistributionRequirement.SUPPORTED_PACKAGE_MANAGERS
        self._mock_test([], pm_packages, NotImplementedError,
                        self.NO_SUPPORTED_PACKAGE_MANAGER_RE)

    def test_platform_without_specified_package_manager(self):
        self._mock_test(['dnf'], {'yum': 'yum'}, NotImplementedError,
                        self.NO_SPECIFIED_PACKAGE_MANAGER_RE)

    def test_platform_with_multiple_package_manager(self):
        managers = DistributionRequirement.SUPPORTED_PACKAGE_MANAGERS
        r = self._mock_test(managers.keys(), managers)
        self.assertCountEqual(r.package_managers, managers.keys())

    def test_no_supported_package_manager(self):
        self._mock_test({'dummy': 'dummy'}, {'foo': 'bar'},
                        NotImplementedError,
                        'foo is not supported')
