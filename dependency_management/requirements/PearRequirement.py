from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)
from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class PearRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``pear`` packages automatically and provide a function to check
    for the requirement.
    """

    REQUIREMENTS = {
        AnyOneOfRequirements([ExecutableRequirement('pear'),
                              DistributionRequirement(package='php-pear',
                                                      zypper='php5-pear')]),

    }

    def __init__(self, package, version=""):
        """
        Constructs a new ``PearRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = PearRequirement('FSM', '1.4.0')
        >>> pr.type
        'pear'
        >>> pr.package
        'FSM'
        >>> pr.version
        '1.4.0'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'pear', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.
        >>> PearRequirement('FSM').install_command()
        ['pear', 'install', 'FSM']

        >>> PearRequirement('FSM', '1.4.0').install_command()
        ['pear', 'install', 'FSM-1.4.0']

        :return: A list with the installation command parameters.
        """

        result = ['pear', 'install',
                  self.package + '-' + self.version if self.version
                  else self.package]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :return: True if dependency is installed, false otherwise.
        """

        return not run('pear info ' + self.package,
                       stdout=Capture(), stderr=Capture()).returncode
