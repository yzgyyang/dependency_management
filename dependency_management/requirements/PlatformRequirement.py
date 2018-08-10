from distutils.version import LooseVersion
import re

from coala_utils.decorators import generate_eq, generate_repr

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.Command import Command


@generate_eq("package", "version")
@generate_repr()
class PlatformRequirement:
    """
    This class helps keeping track of bear distribution requirements.
    """

    REQUIREMENTS = {}

    def __init__(self, package: str, version=''):
        """
        :param package: A string with the name of the package to be installed.
        :param version: Version string. Leave empty to specify latest version.
        """
        self.package = package
        self.version = version

    def __str__(self):
        """
        Just return package name, followed by version if given.
        """
        if self.version:
            return " ".join((self.package, self.version))

        return self.package

    def install_package(self):
        """
        Runs the install command for the package given in a sub-process.

        :param return: Returns exit code of running the install command
        """
        p = Command.execute(self.install_command())
        return p.returncode

    def install_command(self):
        """
        Returns a string with the installation command, to be used by
        "install_package()".

        >>> PlatformRequirement('apt', 'package_name').install_package()
        Traceback (most recent call last):
        ...
        NotImplementedError

        :raises NotImplementedError: Method is not implemented
        """
        raise NotImplementedError

    def is_installed(self):
        """
        Check if the requirement is satisfied.

        :return: Returns True if satisfied, False if not.
        """
        if not self.version:
            result = Command.execute(self.CHECKER_COMMAND.format(self.package))
            return not result.returncode

        result = Command.execute(self.VERSION_COMMAND.format(self.package))
        if result.returncode:
            return False
        output = result.stdout.text
        version = output.rstrip()
        if self.VERSION_REGEX:
            res = re.search(self.VERSION_REGEX, output)
            version = res.group('version').rstrip()
        return LooseVersion(version) >= LooseVersion(self.version)
