import unittest

from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)


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
                                  ExecutableRequirement("python3")])
            .is_installed())

    def test_installed_mixed_with_not_installed_requirements(self):
        self.assertTrue(
            AnyOneOfRequirements([ExecutableRequirement("python"),
                                  ExecutableRequirement("python2"),
                                  ExecutableRequirement("python3"),
                                  ExecutableRequirement("some_bad_exec")])
            .is_installed())

    def test_not_installed_requirements(self):
        self.assertFalse(
            AnyOneOfRequirements([ExecutableRequirement("some_bad_exec"),
                                  ExecutableRequirement("some_terrible_exec"),
                                  ExecutableRequirement("some_nasty_exec")])
            .is_installed())
