import shutil
import unittest

from sarge import Capture
from sarge import run

from dependency_management.requirements.CpanRequirement import CpanRequirement


@unittest.skipIf(shutil.which('cpanm') is None
                 or shutil.which('perldoc') is None,
                 "cpanm or perldoc is not installed.")
class CpanRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(CpanRequirement('Text::CSV')), 'Text::CSV')
        self.assertEqual(
            str(CpanRequirement('Text::CSV', '1.95')), 'Text::CSV 1.95')

    def test_installed_requirement(self):
        self.assertTrue(CpanRequirement('App::Prove').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(CpanRequirement('some_bad_package').is_installed())
