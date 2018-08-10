from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PlatformRequirement import (
    PlatformRequirement)
from dependency_management.requirements.Command import (
    Command)


class PortageRequirement(PlatformRequirement):
    """
    This class is a subclass of ``PlatformRequirement``. It specifies the proper
    type for ``python`` packages automatically and provide a function to check
    for the requirement.
    """
    REQUIREMENTS = {ExecutableRequirement('apt-get')}
    CHECKER_COMMAND = 'equery list {}'
    VERSION_COMMAND = "equery -q list --format='$version' {}"
    VERSION_REGEX = ''

    def __init__(self, package, version=''):
        """
        Creates a new ``PortageRequirement``, using the ``PlatformRequirement``
        constructor.

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PlatformRequirement.__init__(self, package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        :param return: A list with the installation command parameters.
        """
        result = ['equery',
                  '=' + self.package + '-' + self.version if self.version
                  else self.package]
        return result
