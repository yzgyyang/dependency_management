from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PlatformRequirement import (
    PlatformRequirement)
from dependency_management.requirements.Command import (
    Command)


class BrewRequirement(PlatformRequirement):
    """
    This class is a subclass of ``PlatformRequirement``. It specifies the proper
    type for ``Brew`` packages and provide a function to check for the
    requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('brew')}
    VERSION_COMMAND = 'brew list --versions {}'
    CHECKER_COMMAND = VERSION_COMMAND
    VERSION_REGEX = r'\s(?P<version>[^\s]+)$'

    def __init__(self, package, version=''):
        """
        Creates a new ``BrewRequirement``, using the ``PlatformRequirement``
        constructor.

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PlatformRequirement.__init__(
            self, package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        :param return: A list with the installation command parameters.
        """
        result = ['brew', 'install',
                  self.package + '@' + self.version if self.version
                  else self.package]
        return result
