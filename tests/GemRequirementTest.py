import os
import shutil
import unittest

from sarge import run, Capture

from dependency_management.requirements.GemRequirement import GemRequirement


GEM_INSTALLED_PACKAGE = os.environ.get(
    'GEM_INSTALLED_PACKAGE', 'rdoc')

cmd = 'gem list -i ' + GEM_INSTALLED_PACKAGE


@unittest.skipIf(shutil.which('gem') is None or bool(run(cmd,
                                                         stdout=Capture(),
                                                         stderr=Capture())
                                                     .returncode),
                 "Gem is not installed.")
class GemRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(GemRequirement('ruby')), 'ruby')
        self.assertEqual(str(GemRequirement('ruby', '2.4.1')), 'ruby 2.4.1')

    def test_installed_requirement(self):
        self.assertTrue(GemRequirement(GEM_INSTALLED_PACKAGE).is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(GemRequirement('some_bad_package').is_installed())
