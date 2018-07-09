import logging
from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)
from dependency_management.requirements.HaskellRequirement import (
    HaskellRequirement)


class CabalRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, It specifies the proper
    type for ``cabal`` packages automatically and provides a function to check
    for the requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('cabal')}

    def __init__(self, package, version=''):
        """
         **This class is deprecated!** Use `HaskellRequirement` class instead.
        Constructs a new ``CabalRequirement``, using the ``PackageRequirement``
        constructor.

        >>> cr = CabalRequirement('zoom', '0.1')
        >>> cr.type
        'cabal'
        >>> cr.package
        'zoom'
        >>> cr.version
        '0.1'
        >>> str(cr)
        'zoom 0.1'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        logging.debug('CabalRequirement has been deprecated! '
                      'Use HaskellRequirement instead. ')

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
        suffix = self.package
        if self.version:
            suffix += '-' + self.version
        command = list(HaskellRequirement._INSTALL_COMMANDS['cabal'])
        command.append(suffix)
        return command

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        results = run(HaskellRequirement.CHECKER_COMMANDS['cabal']
                                        .format(self.package),
                      stdout=Capture(),
                      stderr=Capture())
        return not results.returncode
