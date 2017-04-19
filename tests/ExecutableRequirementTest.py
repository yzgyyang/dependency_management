import unittest

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)


class ExecutableRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(ExecutableRequirement("python").is_installed() or
                        ExecutableRequirement("python3").is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(ExecutableRequirement("some_bad_exec").is_installed())
