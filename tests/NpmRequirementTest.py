import shutil
import unittest
import unittest.mock

import sarge

from dependency_management.requirements.NpmRequirement import NpmRequirement


@unittest.skipIf(shutil.which('npm') is None, "Npm is not installed.")
class NpmRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(NpmRequirement('npm')), 'npm')
        self.assertEqual(str(NpmRequirement('npm', '4.5')), 'npm 4.5')

    def test_installed_requirement(self):
        with unittest.mock.patch('dependency_management.requirements.' +
                                 'NpmRequirement.run') as mock:
            patched = unittest.mock.Mock(spec=sarge.Pipeline)
            patched.returncode = 0
            mock.return_value = patched
            self.assertTrue(NpmRequirement('some_good_package').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(NpmRequirement('some_bad_package').is_installed())
