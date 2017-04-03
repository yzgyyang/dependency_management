import unittest
import shutil
import logging
from dependency_management.requirements.MavenRequirement import MavenRequirement


@unittest.skipIf(shutil.which('mvn') is None, "Maven is not installed.")
class MavenRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(
            str(MavenRequirement('com.puppycrawl.tools:checkstyle')),
            'com.puppycrawl.tools:checkstyle')
        self.assertEqual(
            str(MavenRequirement('com.puppycrawl.tools:checkstyle', '6.15')),
            'com.puppycrawl.tools:checkstyle 6.15')

    def test_installed_requirement(self):
        with MavenRequirement('com.puppycrawl.tools:checkstyle', '6.15'):
            self.assertTrue(MavenRequirement('com.puppycrawl.tools:checkstyle',
                                             '6.15').is_installed())

        with MavenRequirement('net.sourceforge.pmd:pmd', '5.0.1'):
            self.assertTrue(MavenRequirement('net.sourceforge.pmd:pmd',
                                             '5.0.1').is_installed())

        with MavenRequirement('org.languagetool:languagetool-core', '3.6'):
            self.assertTrue(MavenRequirement('org.languagetool:languagetool'
                                             '-core', '3.6').is_installed())

    def test_not_installed_requirement(self):
        with MavenRequirement('com.puppycrawl.tools:checkstyle', '6.15'):
            self.assertTrue(MavenRequirement('bad_groupId:bad_artifactId',
                                             '0.0').is_installed())

    def test_wrong_package_format(self):
        logger = logging.getLogger()

        with self.assertLogs(logger, 'ERROR') as log:
            with MavenRequirement('com.puppycrawl.tools.checkstyle', '6.15'):
                self.assertEqual(len(log.output), 1)
                self.assertIn(log.output[0],
                              'ERROR:root:The package must be of the form'
                              ' [groupId:artifactId]')

    def test_no_version(self):
        logger = logging.getLogger()

        with self.assertLogs(logger, 'ERROR') as log:
            with MavenRequirement('com.puppycrawl.tools:checkstyle'):
                self.assertEqual(len(log.output), 1)
                self.assertIn(log.output[0],
                              'ERROR:root:Please specify the version'
                              ' of the package')
