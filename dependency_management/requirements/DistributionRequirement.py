from collections import Counter

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

    def __init__(self, package: str=None, version='', repo='',
                 **package_overrides):
        """
        Constructs a new ``DistributionRequirement``, using the
        ``PackageRequirement`` constructor.

        When a ``package`` name is provided, it is used as the
        package attribute, even when override package names are
        provided for specific package managers.

        >>> dr = DistributionRequirement(package='clang',
        ...                              apt_get='libclang',
        ...                              dnf='libclangg')
        >>> dr.package
        'clang'
        >>> dr.packages['apt_get']
        'libclang'
        >>> dr.packages['dnf']
        'libclangg'

        When no ``package`` name is provided, the override package name
        for the local host's package manager is used if possible,
        otherwise the most common override is used.

        >>> dr = DistributionRequirement(unknown1='libclangg',
        ...                              unknown2='libclang',
        ...                              unknown3='libclang')
        >>> dr.package
        'libclang'
        >>> dr.packages['unknown1']
        'libclangg'
        >>> dr.packages['unknown2']
        'libclang'
        >>> dr.packages['unknown3']
        'libclang'

        :param package: A string with the name of the package to be installed.
        :param version: A version string.  Unused.
        :param repo:    The repository from which the package is to be
                        installed.  Unused.
        :param kwargs: Override package names for supported package managers.
        """
        self._managers = None
        self._manager = None
        self.packages = package_overrides

        if not package and not package_overrides:
            raise NoArgsNotImplementedError(
                'No package managers specified')

        if package:
            defaults = {(pm, package)
                        for pm in self.SUPPORTED_PACKAGE_MANAGERS.keys()
                        if pm not in package_overrides}
            self.packages.update(defaults)

        else:
            package = self._get_best_package_name()

        PackageRequirement.__init__(self, 'distribution', package, version)

    def _get_best_package_name(self):
        package_names = Counter(self.packages.values())

        if len(package_names) == 1:
            return package_names.most_common()[0][0]

        try:
            return self.packages[self.get_available_package_manager()]
        except NotImplementedError:
            return package_names.most_common()[0][0]

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
        for manager in self.packages.keys():
            if manager in available_managers:
                found = True
                yield manager
            elif manager not in supported_managers:
                raise NotImplementedError("{} is not supported".format(manager))
        if found:
            return

        raise NotImplementedError("This platform doesn't have any of the "
                                  'specified package manager(s): '
                                  '{}'.format(','.join(self.packages.keys())))

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
        package = self.packages[package_manager]
        return not run(command.format(package),
                       stdout=Capture(), stderr=Capture()).returncode
