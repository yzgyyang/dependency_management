import shutil
import unittest

from dependency_management.requirements.PearRequirement import PearRequirement


@unittest.skipIf(shutil.which('pear') is None, "pear is not installed.")
class PearRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(
            str(PearRequirement('FSM')), 'FSM')
        self.assertEqual(
            str(PearRequirement('FSM', '1.4.0')), 'FSM 1.4.0')

    def test_install(self):
        r = PearRequirement('FSM')
        self.assertEqual(r.install_package(), 0)
        self.assertTrue(PearRequirement('FSM').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(PearRequirement('some_bad_package').is_installed())
