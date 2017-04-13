import unittest
import shutil

import sarge

from dependency_management.requirements.MavenRequirement import MavenRequirement


@unittest.skipIf(shutil.which('mvn') is None, "Maven is not installed.")
class MavenRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(
            str(MavenRequirement('com.puppycrawl.tools:checkstyle', '6.15')),
            'com.puppycrawl.tools:checkstyle 6.15')
        self.assertEqual(
            str(MavenRequirement('net.sourceforge.pmd:pmd', '5.0.1')),
            'net.sourceforge.pmd:pmd 5.0.1')
        self.assertEqual(
            str(MavenRequirement('org.languagetool:languagetool-core', '3.6')),
            'org.languagetool:languagetool-core 3.6')

    def test_installed_requirement(self):
        with unittest.mock.patch('dependency_management.requirements.' +
                                 'MavenRequirement.run') as mock:
            patched = unittest.mock.Mock(spec=sarge.Pipeline)
            patched.returncode = 0
            mock.return_value = patched
            self.assertTrue(MavenRequirement(
                'some_good_package:package', '1.0').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(MavenRequirement(
            'some_bad_package:package', '1.0').is_installed())

    def test_wrong_package_format(self):
        with self.assertRaises(ValueError) as log:
            MavenRequirement('some_good_package', '1.0')
            self.assertEqual(str(log.exception),
                             'The package must be of the form '
                             '[groupId:artifactId]')

    def test_no_version(self):
        with self.assertRaises(TypeError) as log:
            MavenRequirement('some_good_package:package')
            self.assertEqual(str(log.exception),
                             '__init__() missing 1 required positional '
                             "argument: 'version'")


class MavenCheckstyleRequirementTestCase(unittest.TestCase):

    def test_install(self):
        r = MavenRequirement('com.puppycrawl.tools:checkstyle', '6.15')
        sarge.run(r.install_command())
        self.assertTrue(r.is_installed())
