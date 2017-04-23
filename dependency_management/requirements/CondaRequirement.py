from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class CondaRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``conda`` packages automatically and provides a function to check
    for the requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('conda'),
                    ExecutableRequirement('grep')}

    def __init__(self, package, version='', repo=''):
        """
        Constructs a new ``CondaRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = CondaRequirement('scipy', '0.15.0')
        >>> pr.type
        'conda'
        >>> pr.package
        'scipy'
        >>> pr.version
        '0.15.0'
        >>> str(pr)
        'scipy 0.15.0'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        :param repo: The repository from which the package is to be installed.
        """
        PackageRequirement.__init__(self, 'conda', package, version, repo)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> CondaRequirement('scipy', '0.15.0').install_command()
        ['conda', 'install', '--yes', 'scipy=0.15.0']

        >>> CondaRequirement('scipy').install_command()
        ['conda', 'install', '--yes', 'scipy']

        >>> CondaRequirement('bottleneck', '0.8.0', 'pandas').install_command()
        ['conda', 'install', '--yes', '-c', 'pandas', 'bottleneck=0.8.0']

        :param return: A string with the installation command.
        """
        conda_install = ['conda', 'install', '--yes']
        conda_package_version = [self.package + '=' + self.version if
                                 self.version else self.package]
        if self.repo:
            result = conda_install + ['-c', self.repo] + conda_package_version
        else:
            result = conda_install + conda_package_version
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        cmd = 'conda list {} | grep "^{}"'

        if not run(cmd.format(self.package, self.package), stdout=Capture(),
                   stderr=Capture()).returncode:
            return True

        return False
