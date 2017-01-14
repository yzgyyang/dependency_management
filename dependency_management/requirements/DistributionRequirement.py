from sarge import run, Capture

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class DistributionRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifices the
    proper type automatically.
    """

    """
    List of supported package manager with their command respectively
    """
    SUPPORTED_PACKAGE_MANAGERS = {
        'apt_get': 'apt-get',
        'dnf': 'dnf',
        'pacman': 'pacman',
        'portage': 'emerge',
        'xbps': 'xbps-install',
        'yum': 'yum',
        'zypper': 'zypper',
    }

    """
    List of commands that can be used to verify if the package is installed.
    """
    CHECKER_COMMANDS = {
        'apt_get': 'dpkg-query -l {}',
        'dnf': 'rpm -qa | grep ^{}',
        'pacman': 'pacman -Qs {}',
        'portage': 'equery list {}',
        'xbps': 'xbps-query {}',
        'yum': 'rpm -qa | grep ^{}',
        'zypper': 'rpm -qa | grep ^{}',
    }

    def __init__(self, **manager_commands):
        """
        Constructs a new ``DistributionRequirement``, using the
        ``PackageRequirement`` constructor.

        >>> dr = DistributionRequirement(apt_get='libclang', dnf='libclangg')
        >>> dr.package['apt_get']
        'libclang'
        >>> dr.package['dnf']
        'libclangg'

        :param manager_commands: comma separated (type='package') pairs.
        """
        self.package = manager_commands

    def get_available_package_manager(self):
        """
        Returns the available package manager that can be used to satisfy
        the requirement.

        Raises NotImplementedError if there's no supported package manager.

        :return: Supported package manager key
        """
        for manager in self.package.keys():
            try:
                executable = self.SUPPORTED_PACKAGE_MANAGERS[manager]
                if is_executable_exists(executable):
                    return manager
            except KeyError:
                raise NotImplementedError("{} is not supported".format(manager))
        raise NotImplementedError("This system doesn't have any of the "
                                  'supported package manager(s): '
                                  '{}'.format(','.join(self.package.keys())))

    def is_installed(self):
        """
        Check if the requirement is satisfied by calling various package
        managers that are mentioned.

        Raises NotImplementedError if executable is not defined when
        there's no supported package manager.

        :return: True if the dependency is installed, false otherwise
        """

        package_manager = self.get_available_package_manager()
        command = self.CHECKER_COMMANDS[package_manager]
        package = self.package[package_manager]
        return not run(command.format(package),
                       stdout=Capture(), stderr=Capture()).returncode
