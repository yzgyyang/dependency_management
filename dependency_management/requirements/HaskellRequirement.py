from distutils.version import LooseVersion
import re

from sarge import run, Capture

from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class NoArgsNotImplementedError(NotImplementedError, TypeError):
    pass


class HaskellRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the
    proper type automatically.
    """

    """
    List of supported package manager in order of preference for use.
    """
    SUPPORTED_PACKAGE_MANAGERS = ['stack', 'cabal']
    _available_managers = None

    REQUIREMENTS = {
        AnyOneOfRequirements(
            list(
                ExecutableRequirement(name)
                for name in SUPPORTED_PACKAGE_MANAGERS
            )
        ),
    }

    """
    List of commands that can be used to verify if the package is installed.
    """
    CHECKER_COMMANDS = {
        'cabal': 'cabal info "{}"',
        'stack': 'stack exec ghc-pkg -- list',
    }
    """
    List of commands that need to be searched later for package.
    """
    CHECKER_SEARCH = {
        'cabal': False,
        'stack': True,
    }

    """
    List of commands that can be used to install a package.
    """
    _INSTALL_COMMANDS = {
        'cabal': ('cabal', 'install'),
        'stack': ('stack', 'install'),
    }

    """
    List of regex patterns to used with CHECKER_COMMAND to extract the version
    """
    VERSION_EXTRACTION_REGEX = {
        'cabal': r'Versions\sinstalled:\s(?P<version>[^\s]+)(?:\s|,|$)',
        'stack': r'-(?P<version>[^\s]+)(?:\s|$)'
    }

    def __init__(self, package: str = None, version=''):
        """
        Constructs a new ``HaskellRequirement``, using the
        ``PackageRequirement`` constructor.

        >>> hr = HaskellRequirement('random')
        >>> hr.package
        'random'

        :param package: A string with the name of the package to be installed.
        :param version: A version string.
        """
        self._manager = None

        PackageRequirement.__init__(self, 'haskell', package, version)

    def get_available_package_manager(self):
        """
        Returns the available package manager that can be used to satisfy
        the requirement.

        Raises NotImplementedError if there's no supported package manager.

        :return: Supported package manager
        """
        if not self._manager:
            self._manager = self.available_package_managers[0]
        return self._manager

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
        for manager in self.SUPPORTED_PACKAGE_MANAGERS:
            if is_executable_exists(manager):
                found = True
                yield manager
        if found:
            return

        raise NotImplementedError(
            "This platform doesn't have any of the supported package "
            'manager(s): {}'
            .format(', '.join(self.SUPPORTED_PACKAGE_MANAGERS)))

    def get_installed_version(self):
        """
        Return the version if the package is installed, an empty string
        otherwise.
        """
        package_manager = self.get_available_package_manager()
        package = self.package

        results = run(self.CHECKER_COMMANDS[package_manager].format(package),
                      stdout=Capture(), stderr=Capture())

        output = results.stdout.text
        regex = self.VERSION_EXTRACTION_REGEX[package_manager]

        if self.CHECKER_SEARCH[package_manager]:
            output = re.search(re.escape(package) + regex, output)
            if output is None:
                return ''

        elif results.returncode:
            return ''

        res = re.search(regex, str(output))
        if res:
            output = res.group('version')

        return output.rstrip()

    def is_installed(self):
        """
        Check if the requirement is satisfied by calling various package
        managers that are mentioned.

        Raises NotImplementedError if executable is not defined when
        there's no supported package manager.

        :return: True if the dependency is installed, false otherwise
        """

        package_manager = self.get_available_package_manager()
        package = self.package
        version = self.version

        if version:
            installed_version = self.get_installed_version()
            if installed_version:
                return LooseVersion(installed_version) >= LooseVersion(version)
            else:
                return False

        results = run(self.CHECKER_COMMANDS[package_manager].format(package),
                      stdout=Capture(), stderr=Capture())
        regex = self.VERSION_EXTRACTION_REGEX[package_manager]

        if self.CHECKER_SEARCH[package_manager]:
            output = re.search(re.escape(package) + regex, results.stdout.text)
            return output is not None

        else:
            return not results.returncode

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> HaskellRequirement('foo', '').install_command()
        ['stack', 'install', 'foo']
        >>> HaskellRequirement('foo', '3').install_command()
        ['stack', 'install', 'foo-3']

        :param return: A list with the installation command.
        """
        package_manager = self.get_available_package_manager()
        suffix = self.package
        if self.version:
            suffix += '-' + self.version

        command = list(self._INSTALL_COMMANDS[package_manager])

        command.append(suffix)

        return command
