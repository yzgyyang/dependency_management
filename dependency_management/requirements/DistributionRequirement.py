from sarge import run, Capture

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class NoArgsNotImplementedError(NotImplementedError, TypeError):
    pass


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
    _available_managers = None

    """
    List of commands that can be used to verify if the package is installed.
    """
    CHECKER_COMMANDS = {
        'apt_get': 'dpkg-query -l {}',
        'dnf': 'rpm -qa | grep "^{}"',
        'pacman': 'pacman -Qs {}',
        'portage': 'equery list {}',
        'xbps': 'xbps-query {}',
        'yum': 'rpm -qa | grep "^{}"',
        'zypper': 'rpm -qa | grep "^{}"',
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
        self._managers = None
        self._manager = None

        if not manager_commands:
            raise NoArgsNotImplementedError(
                'No package managers specified')
        self.package = manager_commands

    def __str__(self):
        """
        Just return package name based on available package manager.
        """
        return self.package[self.get_available_package_manager()]

    def get_available_package_manager(self):
        """
        Returns the available package manager that can be used to satisfy
        the requirement.

        Raises NotImplementedError if there's no supported package manager.

        :return: Supported package manager key
        """
        if not self._manager:
            self._manager = next(self.get_package_managers())
        return self._manager

    def get_package_managers(self):
        """
        Yield package managers that can satisfy requirement.

        :raises NotImplementedError:
             There are no package managers for requirement.
        """
        found = False
        available_managers = self.available_package_managers
        supported_managers = self.SUPPORTED_PACKAGE_MANAGERS.keys()
        for manager in self.package.keys():
            if manager in available_managers:
                found = True
                yield manager
            elif manager not in supported_managers:
                raise NotImplementedError("{} is not supported".format(manager))
        if found:
            return

        raise NotImplementedError("This platform doesn't have any of the "
                                  'specified package manager(s): '
                                  '{}'.format(','.join(self.package.keys())))

    @property
    def package_managers(self):
        """
        Return package managers that can satisfy requirement.

        :raises NotImplementedError:
             There are no package managers for requirement.
        """
        if self._managers is None:
            self._managers = list(
                self.get_package_managers())
        return self._managers

    @property
    def available_package_managers(self):
        """
        Return all available package managers.

        :raises NotImplementedError:
             There are no package managers for requirement.
        """
        if self._available_managers is None:
            self._available_managers = list(
                self.get_all_available_package_managers())
        return self._available_managers

    @classmethod
    def get_all_available_package_managers(self):
        """
        Yield the available package managers.

        :raises NotImplementedError:
            There are no supported package managers.
        """
        found = False
        for manager, exe in self.SUPPORTED_PACKAGE_MANAGERS.items():
            if is_executable_exists(exe):
                found = True
                yield manager
        if found:
            return

        raise NotImplementedError(
            "This platform doesn't have any of the supported package "
            'manager(s): {}'
            .format(', '.join(self.SUPPORTED_PACKAGE_MANAGERS)))

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
