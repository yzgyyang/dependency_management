import shutil
import unittest
import unittest.mock

import sarge

from dependency_management.requirements.BowerRequirement import BowerRequirement


@unittest.skipIf(shutil.which('bower') is None, "Bower is not installed.")
class BowerRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(BowerRequirement('bower')), 'bower')
        self.assertEqual(str(BowerRequirement('bower', '1.8')), 'bower 1.8')

    def test_installed_requirement(self):
        with unittest.mock.patch('dependency_management.requirements.' +
                                 'BowerRequirement.run') as mock:
            patched = unittest.mock.Mock(spec=sarge.Pipeline)
            patched.stdout = unittest.mock.Mock(spec=sarge.Capture)
            patched.returncode = 0
            patched.stdout.text = ' some_good_package#6.0'
            mock.return_value = patched
            self.assertTrue(BowerRequirement(
                'some_good_package').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(BowerRequirement('some_bad_package').is_installed())
