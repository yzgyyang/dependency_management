import unittest

from dependency_management.Dependant import Dependant
from dependency_management.requirements.PackageRequirement import \
    PackageRequirement
from dependency_management.requirements.PipRequirement import PipRequirement


class SomeDependant(PackageRequirement):
    """
    This is not only a dependant but also usable as a requirement so we can
    test recursive requirements without hugely complicated mocking.
    """
    REQUIREMENTS = [PipRequirement('this-isnt-there')]

    def is_installed(self):
        return True


class AnotherDependant(Dependant):
    REQUIREMENTS = [SomeDependant('some-manager', 'some-package')]


class DependantTestCase(unittest.TestCase):

    def test_no_requirements(self):
        self.assertEqual(
            [],
            list(PipRequirement.missing_requirements())
        )

    def test_missing_requirements(self):
        self.assertEqual(
            SomeDependant.REQUIREMENTS,
            list(SomeDependant.missing_requirements())
        )

    def test_recursive_requirements(self):
        self.assertEqual(
            SomeDependant.REQUIREMENTS + AnotherDependant.REQUIREMENTS,
            list(AnotherDependant.missing_requirements())
        )
