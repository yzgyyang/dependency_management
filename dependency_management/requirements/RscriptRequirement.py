from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class RscriptRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``R`` packages automatically and provide a function to check
    for the requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('R')}

    def __init__(self,
                 package,
                 version="",
                 flag="",
                 repo="http://cran.rstudio.com"):
        """
        Constructs a new ``RscriptRequirement``, using the
        ``PackageRequirement`` constructor.

        >>> pr = RscriptRequirement(
        ...         'formatR', version='1.4', flag='-e',
        ...         repo="http://cran.rstudio.com")
        >>> pr.type
        'R'
        >>> pr.package
        'formatR'
        >>> pr.version
        '1.4'
        >>> str(pr)
        'formatR 1.4'
        >>> pr.flag
        '-e'
        >>> pr.repo
        'http://cran.rstudio.com'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        :param flag:    A string that specifies any additional flags, that
                        are passed to the type.
        :param repo:    The repository from which the package is to be
                        installed.
        """
        PackageRequirement.__init__(self, 'R', package, version, repo)
        self.flag = flag

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> RscriptRequirement(
        ...     'formatR', '' , '-e',
        ...     'http://cran.rstudio.com').install_command()
        ['R', '-e', '"install.packages("formatR", repo="http://cran.rstudio.com", dependencies=TRUE)"']

        :param return: A list with the installation command.
        """
        install = '"install.packages(\"{}\", repo=\"{}\", dependencies=TRUE)"'
        result = ['R', '-e', install.format(self.package, self.repo)]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        return not run(
                ('R -e \'library(\"{}\", quietly=TRUE)\''.format(self.package)),
                stdout=Capture(),
                stderr=Capture()).returncode
