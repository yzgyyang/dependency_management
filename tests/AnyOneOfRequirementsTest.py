import sys
import unittest

from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class AlwaysErrorRequirement(PackageRequirement):
    """
    Requirement class for testing purposes only.
    This class will always raise `NotImplementedError`
    """

    def __init__(self, package, version='', flag=''):
        PackageRequirement.__init__(self, 'test', package, version)

    def is_installed(self):
        raise NotImplementedError('Requirement for testing only.')


class AnyOneOfRequirementsTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(
            str(AnyOneOfRequirements([ExecutableRequirement("python"),
                                      ExecutableRequirement("python2"),
                                      ExecutableRequirement("python3")])),
            "ExecutableRequirement(python) ExecutableRequirement(python2) "
            "ExecutableRequirement(python3)")

    def test_installed_requirements(self):
        self.assertTrue(
            AnyOneOfRequirements([ExecutableRequirement("python"),
                                  ExecutableRequirement("python2"),
                                  ExecutableRequirement("python3"),
                                  ExecutableRequirement(sys.executable)])
            .is_installed())

    def test_installed_mixed_with_not_installed_requirements(self):
        self.assertTrue(
            AnyOneOfRequirements([ExecutableRequirement("python"),
                                  ExecutableRequirement("python2"),
                                  ExecutableRequirement("python3"),
                                  ExecutableRequirement(sys.executable),
                                  ExecutableRequirement("some_bad_exec")])
            .is_installed())

    def test_not_installed_requirements(self):
        self.assertFalse(
            AnyOneOfRequirements([ExecutableRequirement("some_bad_exec"),
                                  ExecutableRequirement("some_terrible_exec"),
                                  ExecutableRequirement("some_nasty_exec")])
            .is_installed())

    def test_skip_requirement(self):
        self.assertTrue(
            AnyOneOfRequirements([AlwaysErrorRequirement('some_terrible_exec'),
                                  AlwaysErrorRequirement('some_nasty_exec'),
                                  AlwaysErrorRequirement('test'),
                                  ExecutableRequirement(sys.executable)])
            .is_installed())
