from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class GemRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``ruby`` packages automatically and provide a function to check
    for the requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('gem')}

    def __init__(self, package, version="", require=""):
        """
        Constructs a new ``GemRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = GemRequirement('setuptools', '19.2', 'flag')
        >>> pr.type
        'gem'
        >>> pr.package
        'setuptools'
        >>> pr.version
        '19.2'
        >>> pr.require
        'flag'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        :param require: A string that specifies any additional flags, that
                        would be used with ``require``.
        """
        PackageRequirement.__init__(self, 'gem', package, version)
        self.require = require

    def install_command(self):
        """
        Creates the installation command for the instance of the class.
        >>> GemRequirement('rubocop').install_command()
        ['gem', 'install', 'rubocop']

        >>> GemRequirement('scss_lint', '', 'false').install_command()
        ['gem', 'install', 'scss_lint']

        >>> GemRequirement('rake', '10.5.0').install_command()
        ['gem', 'install', 'rake:10.5.0']

        :param return: A string with the installation command.
        """

        gem = self.package
        if self.version:
            gem += ':' + self.version
        result = ['gem', 'install', gem]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        cmd = 'gem list -i ' + self.package

        return not run(cmd, stdout=Capture(), stderr=Capture()).returncode
