import re

from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class BowerRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``bower`` packages automatically and provide a function to check
    for the requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('bower')}

    def __init__(self, package, version=""):
        """
        Constructs a new ``BowerRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = BowerRequirement('mdast-lint', '6.0')
        >>> pr.type
        'bower'
        >>> pr.package
        'mdast-lint'
        >>> pr.version
        '6.0'
        >>> str(pr)
        'mdast-lint 6.0'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'bower', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> BowerRequirement('mdast-lint', '6.0').install_command()
        ['bower', 'install', 'mdast-lint#6.0']

        >>> BowerRequirement('mdast-lint').install_command()
        ['bower', 'install', 'mdast-lint']

        :param return: A string with the installation command.
        """
        result = ['bower', 'install', self.package + "#" + self.version
                  if self.version else self.package]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        bower = run('bower list', stdout=Capture(), stderr=Capture())

        if not re.search(' ' + self.package + '#', bower.stdout.text) is None:
            return True

        return False
