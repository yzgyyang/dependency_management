from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class ComposerRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``Composer`` packages automatically and provides a function to
    check for the requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('composer')}

    def __init__(self, package, version=""):
        """
        Constructs a new ``ComposerRequirement``, using the
        ``PackageRequirement`` constructor.

        >>> pr = ComposerRequirement('phpstan/phpstan', '0.6.4')
        >>> pr.type
        'composer'
        >>> pr.package
        'phpstan/phpstan'
        >>> pr.version
        '0.6.4'
        >>> str(pr)
        'phpstan/phpstan 0.6.4'

        :param package:
            A string with the name of the package to be installed.
        :param version:
            A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'composer', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> ComposerRequirement('phpstan/phpstan', '0.6.4').install_command()
        ['composer', 'require', 'phpstan/phpstan:0.6.4']

        >>> ComposerRequirement('phpstan/phpstan').install_command()
        ['composer', 'require', 'phpstan/phpstan']

        :param return: A string with the installation command.
        """
        result = ['composer', 'require', self.package + ":" + self.version
                  if self.version else self.package]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        for cmd in ('composer show ' + self.package,
                    'composer global show ' + self.package):

            if not run(cmd, stdout=Capture(), stderr=Capture()).returncode:
                return True

        return False
