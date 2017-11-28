from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class GoPMRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``gopm`` packages automatically and provide a function to check
    for the requirement.
    """

    REQUIREMENTS = {ExecutableRequirement("gopm")}

    def __init__(self, package, version=""):
        """
        Constructs a new ``GoPMRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = GoPMRequirement('github.com/hyperhq/runv')
        >>> pr.type
        'gopm'
        >>> pr.package
        'github.com/hyperhq/runv'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'gopm', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> GoPMRequirement('github.com/hyperhq/runv').install_command()
        ['gopm', 'get', 'github.com/hyperhq/runv']

        :param return: An array with the installation command.
        """

        result = ["gopm", "get", self.package]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """

        return not run('go list ' + self.package,
                       stdout=Capture(),
                       stderr=Capture()).returncode
