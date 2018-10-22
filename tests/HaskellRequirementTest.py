import shutil
import unittest

import sarge

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.HaskellRequirement import (
    HaskellRequirement)


@unittest.skipIf(shutil.which('cabal') is None, 'Cabal is not installed.')
class HaskellCabalRequirementTestCase(unittest.TestCase):

    def _mock_test(self, package: str = None, version=''):
        _shutil_which = shutil.which
        hr = HaskellRequirement(package, version)
        old_managers = hr._available_managers
        hr._manager = None

        hr._available_managers = None

        def fake_which(exe):
            if exe == 'cabal':
                return True

        try:
            shutil.which = fake_which

            # Force caching of package manager
            hr.get_available_package_manager()
            return hr
        finally:
            # Reverse changes
            hr._available_managers = old_managers
            shutil.which = _shutil_which

    def test__str__(self):
        r = self._mock_test('random')
        self.assertEqual(str(r), 'random')
        self.assertEqual(r._manager, 'cabal')

    def test_installed_requirement(self):
        r = self._mock_test('array')
        self.assertTrue(r.is_installed())
        self.assertEqual(r._manager, 'cabal')

    def test_not_installed_requirement(self):
        r = self._mock_test('some_bad_package')
        self.assertFalse(r.is_installed())
        self.assertEqual(r._manager, 'cabal')

    def test_installed_requirement_version(self):
        r = self._mock_test('array', '0')
        self.assertTrue(r.is_installed())
        self.assertEqual(r._manager, 'cabal')

    def test_not_installed_requirement_because_version(self):
        r = self._mock_test('array', '1000000')
        self.assertFalse(r.is_installed())
        self.assertEqual(r._manager, 'cabal')

    def test_not_installed_requirement_with_version(self):
        r = self._mock_test('some_bad_package', '1')
        self.assertFalse(r.is_installed())
        self.assertEqual(r._manager, 'cabal')


@unittest.skipIf(shutil.which('stack') is None, 'Stack is not installed.')
class HaskellStackRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(HaskellRequirement(
            'random', '')), 'random')

    def test_installed_requirement(self):
        self.assertTrue(HaskellRequirement('array', '').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(
            HaskellRequirement('some_bad_package', '').is_installed())

    def test_installed_requirement_version(self):
        self.assertTrue(HaskellRequirement(
            'array', '0').is_installed())

    def test_not_installed_requirement_because_version(self):
        self.assertFalse(HaskellRequirement('array',
                                            '1000000').is_installed())

    def test_not_installed_requirement_with_version(self):
        self.assertFalse(HaskellRequirement('some_bad_package', '1')
                         .is_installed())


class ExpectedErrorsHaskellRequirementTestCase(unittest.TestCase):

    NO_SUPPORTED_PACKAGE_MANAGER_RE = ("This platform doesn't have any of the "
                                       'supported package manager')

    def _mock_test(self, managers, exc=None, message=None):
        _shutil_which = shutil.which
        hr = HaskellRequirement('something_random')
        old_managers = hr._available_managers

        hr._manager = None
        hr._available_managers = None

        def fake_which(exe):
            if exe in managers:
                return True
        try:
            shutil.which = fake_which

            if not exc:
                # Force caching of all package managers
                hr.available_package_managers
                return hr

            with self.assertRaisesRegex(
                    exc,
                    message):
                hr.get_available_package_manager()
        finally:
            # Reverse changes
            hr._available_managers = old_managers
            shutil.which = _shutil_which

    def test_platform_without_supported_package_manager(self):
        self._mock_test([], NotImplementedError,
                        self.NO_SUPPORTED_PACKAGE_MANAGER_RE)

    def test_platform_with_multiple_package_manager(self):
        managers = HaskellRequirement.SUPPORTED_PACKAGE_MANAGERS
        r = self._mock_test(managers)
        self.assertCountEqual(r.available_package_managers, managers)
