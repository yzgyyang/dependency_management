import unittest

from dependency_management.requirements.PlatformRequirement import (
    PlatformRequirement)


class SomeRequirement(PlatformRequirement):
    """
    Testing PlatformRequirement without hugely complicated mocking.
    """
    VERSION_COMMAND = 'echo "version:1.2"'
    VERSION_REGEX = r'version:(?P<version>.*)'

    def __init__(self, package, version=''):
        PlatformRequirement.__init__(
            self, package, version)


class PlatformRequirementTestCase(unittest.TestCase):

    def test_is_installed_with_regex(self):
        p = SomeRequirement('name', '1.1')
        self.assertTrue(p.is_installed())
        p = SomeRequirement('name', '1.3')
        self.assertFalse(p.is_installed())
