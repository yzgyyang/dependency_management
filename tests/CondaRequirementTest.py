import shutil
import unittest
import unittest.mock

import sarge

from dependency_management.requirements.CondaRequirement import (
    CondaRequirement)


@unittest.skipIf(shutil.which('conda') is None,
                 'conda is not installed.')
class CondaRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(CondaRequirement('scipy')),
                         'scipy')
        self.assertEqual(str(CondaRequirement('scipy', '0.15.0')),
                         'scipy 0.15.0')

    def test_installed_requirement(self):
        with unittest.mock.patch('dependency_management.requirements.' +
                                 'CondaRequirement.run') as mock:
            patched = unittest.mock.Mock(spec=sarge.Pipeline)
            patched.returncode = 0
            mock.return_value = patched
            self.assertTrue(CondaRequirement('some_good_package').
                            is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(CondaRequirement('some_bad_package').is_installed())


@unittest.skipIf(shutil.which('conda') is None,
                 'conda is not installed.')
class CondaLockfileRequirementTestCase(unittest.TestCase):

    def test_install(self):
        r = CondaRequirement('lockfile', '0.12.2')
        self.assertEqual(r.install_package(), 0)
        self.assertTrue(r.is_installed())
