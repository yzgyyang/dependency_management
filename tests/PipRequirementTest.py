import unittest
import sys

from dependency_management.requirements.PipRequirement import PipRequirement
from sarge import get_both


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

    def test_upgrade_requirement(self):
        p = PipRequirement('vanity', '1.2.5')
        p.install_package()
        old_ver = get_both(
            sys.executable + ' -m pip show vanity')[0].split('\n')[1]
        p.upgrade_package()
        new_ver = get_both(
            sys.executable + ' -m pip show vanity')[0].split('\n')[1]
        self.assertGreater(new_ver, old_ver)

    def test_upgrade_on_already_latest_version(self):
        p = PipRequirement('vanity')
        p.install_package()
        old_ver = get_both(
            sys.executable + ' -m pip show vanity')[0].split('\n')[1]
        p.upgrade_package()
        new_ver = get_both(
            sys.executable + ' -m pip show vanity')[0].split('\n')[1]
        self.assertEqual(new_ver, old_ver)

    def test_uninstall_requirement(self):
        p = PipRequirement('colorit')
        p.install_package()
        self.assertTrue(p.is_installed())
        p.uninstall_package()
        self.assertFalse(p.is_installed())
