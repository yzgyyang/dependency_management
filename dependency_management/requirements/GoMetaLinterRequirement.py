from sarge import run, Capture

from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.GoRequirement import (
    GoRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class GoMetaLinterRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It simply requires
    GoMetaLinter which installs multiple Go linter dependencies.
    """

    REQUIREMENTS = {
        AnyOneOfRequirements([
            GoRequirement('gopkg.in/alecthomas/gometalinter.v2'),
            ExecutableRequirement('gometalinter.v2'),
        ])
    }

    _available_linter = {
        'deadcode',
        'dupl',
        'errcheck',
        'gas',
        'gochecknoglobals',
        'gochecknoinits',
        'goconst',
        'gocyclo',
        'goimports',
        'golint',
        'gosimple',
        'gotype',
        'gotypex',
        'ineffassign',
        'interfacer',
        'lll',
        'maligned',
        'megacheck',
        'misspell',
        'nakedret',
        'safesql',
        'staticcheck',
        'structcheck',
        'unconvert',
        'unparam',
        'unused',
        'varcheck',
    }

    _install_command = None
    _is_installed = None

    def __init__(self, package='', version=''):
        """
        Constructs a new ``GoMetaLinterRequirement``, using the
        ``PackageRequirement`` constructor.

        >>> pr = GoMetaLinterRequirement('gotype')
        >>> pr.type
        'gometalinter'
        >>> pr.package
        'gotype'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        if package not in GoMetaLinterRequirement._available_linter:
            raise ValueError(
                package + ' is not available with Go Meta Linter.'
            )
        PackageRequirement.__init__(self, 'gometalinter', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> GoMetaLinterRequirement('gotype').install_command()
        ['/root/go/bin/gometalinter.v2', '--install']

        :param return: An array with the installation command.
        """
        if GoMetaLinterRequirement._install_command is not None:
            return GoMetaLinterRequirement._install_command

        env = run('go env GOPATH', stdout=Capture(), stderr=Capture())
        gopath = env.stdout.text.rstrip()
        GoMetaLinterRequirement._install_command = [
            gopath + '/bin/gometalinter.v2', '--install']
        return GoMetaLinterRequirement._install_command

    def install_package(self):
        """
        Runs the install command for the package given in a sub-process, and
        update the cached _is_install result.

        :param return: Returns exit code of running the install command
        """
        p = run(' '.join(self.install_command()),
                stdout=Capture(),
                stderr=Capture())
        GoMetaLinterRequirement._is_installed = not p.returncode
        return p.returncode

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        if GoMetaLinterRequirement._is_installed is not None:
            return GoMetaLinterRequirement._is_installed

        env = run('go env GOPATH', stdout=Capture(), stderr=Capture())
        gopath = env.stdout.text.rstrip()
        p = run([gopath + '/bin/gometalinter.v2', '--enable-all'],
                stdout=Capture(),
                stderr=Capture())
        GoMetaLinterRequirement._is_installed = not p.returncode
        return GoMetaLinterRequirement._is_installed
