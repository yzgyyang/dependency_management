import re
import logging

from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class MavenRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifices the proper
    type for ``java`` packages automatically and provide a function to check
    for the requirement.
    """

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
        >>> mr.repo
        'https://repo.maven.apache.org/maven2'

        :param package: A string with the {groupId:artifactId} of
                        the package to be installed.
        :param version: A version string.
        :param repo:    The repository from which the package to
                        be installed is from.
        """
        package_regex = '([^: /]*:[^: /]*)'
        package_match = (re.compile(package_regex)).match(package)

        if not package_match:
            logging.error(
                'The package must be of the form [groupId:artifactId]')
            return

        if version is None:
            logging.error('Please specify the version of the package')
            return

        PackageRequirement.__init__(self, 'mvn', package, version)
        self.repo = repo

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> MavenRequirement(
        ...     'com.puppycrawl.tools:checkstyle', '6.15',
        ...     'https://repo.maven.apache.org/maven2').install_command()
        'mvn org.apache.maven.plugins:maven-dependency-plugin:2.1:get \
                       -DrepoUrl=https://repo.maven.apache.org/maven2/ \
                       -Dartifact=com.puppycrawl.tools:checkstyle:6.15'

        :param return: A string with the installation command.
        """
        result = ('mvn org.apache.maven.plugins:maven-dependency'
                  '-plugin:2.1:get \
                       -DrepoUrl={}/ \
                       -Dartifact={}:{}'.format(self.repo, self.package,
                                                self.version))
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
