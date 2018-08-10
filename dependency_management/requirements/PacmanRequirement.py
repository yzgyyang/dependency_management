from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PlatformRequirement import (
    PlatformRequirement)
from dependency_management.requirements.Command import (
    Command)


class PacmanRequirement(PlatformRequirement):
    """
    This class is a subclass of ``PlatformRequirement``. It specifies the proper
    type for ``Pacman`` packages and provide a function to check for the
    requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('pacman')}
    CHECKER_COMMAND = 'pacman -Qs {}'
    VERSION_COMMAND = 'pacman -Qiq {}'
    VERSION_REGEX = r'Version\s+:\s(?P<version>.+)'

    def __init__(self, package, version=''):
        """
        Creates a new ``PacmanRequirement``, using the ``PlatformRequirement``
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
        result = ['pacman', '-S', '--noconfirm', self.package]
        return result
