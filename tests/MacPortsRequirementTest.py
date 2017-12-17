import unittest
import unittest.mock

import sarge

from dependency_management.requirements.MacPortsRequirement import (
    MacPortsRequirement)


class MacPortsRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(MacPortsRequirement('figlet')), 'figlet')

    def test_installed_requirement(self):
        with unittest.mock.patch('dependency_management.requirements.' +
                                 'MacPortsRequirement.run') as mock:
            patched = unittest.mock.Mock(spec=sarge.Pipeline)
            patched.returncode = 0
            mock.return_value = patched
            self.assertTrue(MacPortsRequirement(
                'some_good_package').is_installed())

    def test_not_installed_requirement(self):
        with unittest.mock.patch('dependency_management.requirements.' +
                                 'MacPortsRequirement.run') as mock:
            patched = unittest.mock.Mock(spec=sarge.Pipeline)
            patched.returncode = 1
            mock.return_value = patched
            self.assertFalse(MacPortsRequirement(
                'some_bad_package').is_installed())
