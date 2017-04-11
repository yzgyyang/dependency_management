import unittest
import sys

from dependency_management.requirements.PipRequirement import PipRequirement


class PipRequirementTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import pip
        del pip

    def test__str__(self):
        self.assertEqual(str(PipRequirement('setuptools')), 'setuptools')
        self.assertEqual(str(PipRequirement('setuptools', '19.2')),
                         'setuptools 19.2')

    def test_install_command_with_version(self):
        self.assertEqual(
            [sys.executable, '-m', 'pip', 'install', 'setuptools==19.2'],
            PipRequirement('setuptools', '19.2').install_command())

    def test_install_command_without_version(self):
        self.assertEqual([sys.executable, '-m', 'pip', 'install', 'setuptools'],
                         PipRequirement('setuptools').install_command())

    def test_installed_requirement(self):
        self.assertTrue(PipRequirement('pip').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(PipRequirement('some_bad_package').is_installed())
