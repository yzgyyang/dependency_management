from sarge import run, Capture

from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)
from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class GoRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``go`` packages automatically and provide a function to check
    for the requirement.
    """

    REQUIREMENTS = {
        AnyOneOfRequirements([
            DistributionRequirement(
                'go',
                apt_get='golang',
                dnf='golang',
                yum='golang',
            ),
            ExecutableRequirement('go'),
        ])
    }

    def __init__(self, package, version="", flag=""):
        """
        Constructs a new ``GoRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = GoRequirement('github.com/golang/lint/golint', '')
        >>> pr.type
        'go'
        >>> pr.package
        'github.com/golang/lint/golint'
        >>> pr.version
        ''

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        :param flag:    A string that specifies any additional flags, that
                        are passed to the manager. (WARNING: deprecated)

        """
        if version:
            raise NotImplementedError(
                'Setting version is not implemented by GoRequirement')
        PackageRequirement.__init__(self, 'go', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> GoRequirement(
        ...     'github.com/golang/lint/golint', '' , '-u' ).install_command()
        ['go', 'get', '-u', 'github.com/golang/lint/golint']

        :param return: A string with the installation command.
        """
        return ['go', 'get', '-u', self.package]

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        return not run('go list ' + self.package,
                       stdout=Capture(),
                       stderr=Capture()).returncode
