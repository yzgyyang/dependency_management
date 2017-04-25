import functools

from coala_utils.decorators import generate_eq, generate_repr
from sarge import run, Capture

from dependency_management.Dependant import Dependant


@generate_eq("type", "package", "version", "repo")
@generate_repr()
class PackageRequirement(Dependant):
    """
    This class helps keeping track of bear requirements. It should simply
    be appended to the REQUIREMENTS tuple inside the Bear class.

    Two ``PackageRequirements`` should always be equal if they have the same
    type, package and version:

    >>> pr1 = PackageRequirement('pip', 'coala_decorators', '0.1.0')
    >>> pr2 = PackageRequirement('pip', 'coala_decorators', '0.1.0')
    >>> pr1 == pr2
    True
    """

    REQUIREMENTS = {}

    def __init__(self, type: str, package: str, version="", repo=""):
        """
        Constructs a new ``PackageRequirement``.

        >>> pr = PackageRequirement('pip', 'colorama', '0.1.0')
        >>> pr.type
        'pip'
        >>> pr.package
        'colorama'
        >>> pr.version
        '0.1.0'
        >>> str(pr)
        'colorama 0.1.0'

        :param type:    A string with the name of the manager (pip, npm, etc).
        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        :param repo:    The repository from which the package is to be
                        installed.
        """
        super().__init__()

        self.type = type
        self.package = package
        self.version = version
        self.repo = repo

        self.is_installed = functools.lru_cache()(
            self.is_installed)

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
        p = run(" ".join(self.install_command()), stdout=Capture(),
                stderr=Capture())
        self.is_installed.cache_clear()
        return p.returncode

    def install_command(self):
        """
        Returns a string with the installation command, to be used by
        "install_package()".

        >>> PackageRequirement('pip', 'pip').install_package()
        Traceback (most recent call last):
        ...
        NotImplementedError

        :raises NotImplementedError: Method is not implemented
        """
        raise NotImplementedError

    def is_installed(self):
        """
        Check if the requirement is satisfied.

        >>> PackageRequirement('pip', \
                               'numpy', \
                               '1.12.1').is_installed()
        Traceback (most recent call last):
        ...
        NotImplementedError

        :return: Returns True if satisfied, False if not.
        :raises NotImplementedError: Method is not implemented
        """
        raise NotImplementedError

    def get_installed_version(self):
        """
        Returns a string with the installed verion of the package.

        >>> PackageRequirement('pip', 'pip').get_installed_version()
        Traceback (most recent call last):
        ...
        NotImplementedError

        :raises NotImplementedError: Method is not implemented
        """
        raise NotImplementedError
