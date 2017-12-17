from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class MacPortsRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``MacPorts`` packages automatically and provide a function to check
    for the requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('port')}

    def __init__(self, package):
        """
        Constructs a new ``MacPortsRequirement``,
        using the ``PackageRequirement`` constructor.
        Note that MacPorts does not intend for packages older than the newest
        version to be installed.

        >>> pr = MacPortsRequirement('figlet')
        >>> pr.package
        'figlet'

        :param package: A string with the name of the package to be installed.
        """
        PackageRequirement.__init__(self, 'MacPorts', package)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> MacPortsRequirement('figlet').install_command()
        ['port', 'install', 'figlet']

        :return: A list with the installation command parameters.
        """
        result = ['port', 'install', self.package]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :return: True if dependency is installed, False otherwise.
        """
        cmd = 'port installed ' + self.package
        return not run(cmd, stdout=Capture(), stderr=Capture()).returncode
