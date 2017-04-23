from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class CargoRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``cargo`` packages automatically and provides a function to
    check for the requirement.
    """

    REQUIREMENTS = {
        ExecutableRequirement('cargo'),
        ExecutableRequirement('grep'),
    }

    def __init__(self, package, version=''):
        """
        Constructs a new ``CargoRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = CargoRequirement('pulldown-cmark', '0.0.14')
        >>> pr.type
        'cargo'
        >>> pr.package
        'pulldown-cmark'
        >>> pr.version
        '0.0.14'
        >>> str(pr)
        'pulldown-cmark 0.0.14'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'cargo', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> CargoRequirement('pulldown-cmark', '0.0.14').install_command()
        ['cargo', 'install', '--vers 0.0.14 pulldown-cmark']

        >>> CargoRequirement('pulldown-cmark').install_command()
        ['cargo', 'install', 'pulldown-cmark']

        :param return: A string with the installation command.
        """
        result = ['cargo', 'install', '--vers ' + self.version + ' ' +
                  self.package if self.version else self.package]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        cmd = 'cargo install --list | grep "^{}"'

        if not run(cmd.format(self.package), stdout=Capture(),
                   stderr=Capture()).returncode:
            return True

        return False
