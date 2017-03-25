import unittest
import unittest.mock
import sarge
import shutil
from dependency_management.requirements.ComposerRequirement import (
    ComposerRequirement)


@unittest.skipIf(shutil.which('composer') is None,
                 "Composer is not installed.")
class ComposerRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        with unittest.mock.patch('dependency_management.requirements.' +
                                 'ComposerRequirement.run') as mock:
            patched = unittest.mock.Mock(spec=sarge.Pipeline)
            patched.returncode = 0
            mock.return_value = patched
            self.assertTrue(ComposerRequirement(
                'some_good_package').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(ComposerRequirement(
            'some_bad_package').is_installed())
