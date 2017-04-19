from dependency_management.Helper import is_executable_exists
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class ExecutableRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the
    proper type automatically.
    """

    def __init__(self, executable):
        """
        Constructs a new ``ExecutableRequirement``, using the
        ``PackageRequirement`` constructor.

        >>> er = ExecutableRequirement('python')
        >>> er.executable
        'python'
        """

        self.executable = executable
        PackageRequirement.__init__(self, 'exec', executable, '')

    def is_installed(self):
        """
        Check if the requirement is satisfied by checking if the executable
        exists in PATH.

        :return: True if the executable exists in PATH, false otherwise.
        """
        return is_executable_exists(self.executable)
