import shutil
import unittest
import unittest.mock

import sarge

from dependency_management.requirements.JuliaRequirement import (
    JuliaRequirement)


@unittest.skipIf(shutil.which('julia') is None, 'Julia is not installed.')
class JuliaRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(JuliaRequirement('Lint')), 'Lint')
        self.assertEqual(str(JuliaRequirement('Lint', '0.5')), 'Lint 0.5')

    def test_installed_requirement(self):
        with unittest.mock.patch('dependency_management.requirements.' +
                                 'JuliaRequirement.run') as mock:
            patched = unittest.mock.Mock(spec=sarge.Pipeline)
            patched.returncode = 0
            mock.return_value = patched
            self.assertTrue(JuliaRequirement(
                'some_good_package').is_installed())

    def test_not_registered_requirement(self):
        self.assertFalse(JuliaRequirement("some_bad_package").is_installed())

    def test_registered_but_not_installed_requirement(self):
        # FIXME Make this test more reliable, because `ACME` can be an
        # FIXME installed package.
        self.assertFalse(JuliaRequirement("ACME").is_installed())
