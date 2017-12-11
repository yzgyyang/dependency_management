from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class CpanRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``perl`` packages automatically and provide a function to check
    for the requirement.
    """

    REQUIREMENTS = {
        ExecutableRequirement('cpanm'),
        ExecutableRequirement('perldoc'),
    }

    def __init__(self, package, version=""):
        """
        Constructs a new ``CpanRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = CpanRequirement('Text::CSV', '1.95')
        >>> pr.type
        'cpan'
        >>> pr.package
        'Text::CSV'
        >>> pr.version
        '1.95'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'cpan', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.
        >>> CpanRequirement('Text::CSV').install_command()
        ['cpanm', 'install', 'Text::CSV']

        >>> CpanRequirement('Text::CSV', '1.93').install_command()
        ['cpanm', 'install', 'Text::CSV@1.93']

        :return: A list with the installation command parameters.
        """

        module = self.package
        if self.version:
            module += '@' + self.version
        result = ['cpanm', 'install', module]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :return: True if dependency is installed, false otherwise.
        """
        cmd = 'perldoc -l ' + self.package

        return not run(cmd, stdout=Capture(), stderr=Capture()).returncode
