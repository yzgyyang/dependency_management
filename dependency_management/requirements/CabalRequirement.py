from dependency_management.requirements.PackageRequirement import (
   PackageRequirement)
from sarge import run, Capture


class CabalRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, It specifies the proper
    type for ``cabal`` packages automatically and provides a function to check
    for the requirement.
    """

    def __init__(self, package, version=''):
        """
        Constructs a new ``CabalRequirement``, using the ``PackageRequirement``
        constructor.

        >>> cr = CabalRequirement('zoom', '0.1')
        >>> cr.type
        'cabal'
        >>> cr.package
        'zoom'
        >>> cr.version
        '0.1'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'cabal', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> CabalRequirement('foo', '3').install_command()
        ['cabal', 'install', 'foo-3']
        >>> CabalRequirement('foo').install_command()
        ['cabal', 'install', 'foo']

        :param return: A list with the installation command parameters.
        """
        result = ['cabal', 'install',
                  self.package + '-' + self.version if self.version
                  else self.package]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        return not run('cabal info' + self.package,
                       stdout=Capture(),
                       stderr=Capture()).returncode
