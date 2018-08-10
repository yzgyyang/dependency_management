from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PlatformRequirement import (
    PlatformRequirement)
from dependency_management.requirements.Command import (
    Command)


class AptRequirement(PlatformRequirement):
    """
    This class is a subclass of ``PlatformRequirement``. It specifies the proper
    type for ``apt`` packages and provide a function to check for the
    requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('apt-get')}
    CHECKER_COMMAND = 'dpkg-query -l {}'
    VERSION_COMMAND = "dpkg-query --showformat '${{Version}}' --show {}"
    VERSION_REGEX = ''

    def __init__(self, package, version=''):
        """
        Creates a new ``AptRequirement``, using the ``PlatformRequirement``
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
        result = ['apt-get', 'install', '--yes',
                  self.package + '=' + self.version if self.version
                  else self.package]
        return result
