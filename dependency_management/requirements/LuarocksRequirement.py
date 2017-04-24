from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class LuarocksRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``luarocks`` packages automatically and provide a function to
    check for the requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('luarocks')}

    def __init__(self, package, version=''):
        """
        Constructs a new ``Luarocks``, using the ``PackageRequirement``
        constructor.

        >>> pr = LuarocksRequirement('luasocket', '3.0rc1')
        >>> pr.type
        'luarocks'
        >>> pr.package
        'luasocket'
        >>> pr.version
        '3.0rc1'
        >>> str(pr)
        'luasocket 3.0rc1'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'luarocks', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> LuarocksRequirement('luacheck', '0.19.1').install_command()
        ['luarocks', 'install', 'luacheck 0.19.1']

        >>> LuarocksRequirement('luacheck').install_command()
        ['luarocks', 'install', 'luacheck']

        :param return: A string with the installation command.
        """
        result = ['luarocks', 'install', self.package + ' ' + self.version
                  if self.version else self.package]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        cmd = 'luarocks show ' + self.package

        if not run(cmd, stdout=Capture(), stderr=Capture()).returncode:
            return True

        return False
