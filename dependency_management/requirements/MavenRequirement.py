import re

from sarge import run, Capture

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class MavenRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifices the proper
    type for ``java`` packages automatically and provide a function to check
    for the requirement.
    """

    REQUIREMENTS = {ExecutableRequirement('mvn')}

    def __init__(self, package, version: str,
                 repo="https://repo.maven.apache.org/maven2"):
        """
        Constructs a new ``MavenRequirement``, using the ``PackageRequirement``
        constructor.

        >>> mr = MavenRequirement('com.puppycrawl.tools:checkstyle', '6.15')
        >>> mr.type
        'mvn'
        >>> mr.package
        'com.puppycrawl.tools:checkstyle'
        >>> mr.version
        '6.15'
        >>> str(mr)
        'com.puppycrawl.tools:checkstyle 6.15'
        >>> mr.repo
        'https://repo.maven.apache.org/maven2'

        :param package: A string with the {groupId:artifactId} of
                        the package to be installed.
        :param version: A version string.
        :param repo:    The repository from which the package is to be
                        installed.
        """
        package_regex = '([^: /]*:[^: /]*)'
        package_match = (re.compile(package_regex)).match(package)

        if not package_match:
            raise ValueError(
                'The package must be of the form [groupId:artifactId]')

        PackageRequirement.__init__(self, 'mvn', package, version, repo)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> from pprint import pprint
        >>> r = MavenRequirement(
        ...     'com.puppycrawl.tools:checkstyle', '6.15',
        ...     'https://repo.maven.apache.org/maven2')
        >>> pprint(r.install_command())
        ['mvn',
         'dependency:get',
         '-DrepoUrl=https://repo.maven.apache.org/maven2/',
         '-Dartifact=com.puppycrawl.tools:checkstyle:6.15']


        :param return: A string with the installation command.
        """
        result = ['mvn', 'dependency:get',
                  '-DrepoUrl={}/'.format(self.repo),
                  '-Dartifact={}:{}'.format(self.package, self.version)
                  ]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        return not run('mvn dependency:get -Dartifact={}:{} --offline'.format(
                       self.package,
                       self.version), stdout=Capture(),
                       stderr=Capture()).returncode
