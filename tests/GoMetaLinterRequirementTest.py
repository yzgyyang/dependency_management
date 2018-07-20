import shutil
import unittest

from dependency_management.requirements.GoMetaLinterRequirement import (
    GoMetaLinterRequirement)


@unittest.skipIf(shutil.which('gometalinter.v2') is None,
                 'GoMetaLinter is not installed or not in PATH.')
class GoMetaLinterRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(GoMetaLinterRequirement('gotype')), 'gotype')

    def test_install_command(self):
        self.assertEqual(GoMetaLinterRequirement('gotype').install_command(),
                         [shutil.which('gometalinter.v2'), '--install'])

    def test_install_command_unavailable_package(self):
        with self.assertRaises(ValueError):
            GoMetaLinterRequirement('some_bad_package').install_command()


@unittest.skipIf(shutil.which('gometalinter.v2') is None,
                 'GoMetaLinter is not installed or not in PATH.')
class GoMetaLinterInstallTestCase(unittest.TestCase):
    def test_install(self):
        self.assertFalse(GoMetaLinterRequirement('gotype').is_installed())
        self.assertEqual(GoMetaLinterRequirement('gotype').install_package(),
                         0)
        self.assertTrue(GoMetaLinterRequirement('gotype').is_installed())
        self.assertTrue(GoMetaLinterRequirement('errcheck').is_installed())
