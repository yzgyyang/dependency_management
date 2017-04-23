from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


class AnyOneOfRequirements(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It determines which
    requirements can be used to resolve the dependency.
    """

    def __init__(self, requirements: list):
        """
        Constructs a new ``AnyOneOfRequirements``.

        Requirements are ordered by priority.

        >>> from dependency_management.requirements.ExecutableRequirement \\
        ...     import ExecutableRequirement
        >>> aor = AnyOneOfRequirements([ExecutableRequirement("python"),
        ...                             ExecutableRequirement("python3")])
        >>> str(aor)
        'ExecutableRequirement(python) ExecutableRequirement(python3)'
        """
        self.requirements = requirements
        self._packages_str = " ".join(sorted(
                                      ["%s(%s)" %
                                       (requirement.__class__.__name__,
                                        str(requirement))
                                       for requirement in self.requirements]))
        PackageRequirement.__init__(self, "any-one-of", self._packages_str)

    def is_installed(self):
        """
        Check if any one of the requirements are satisfied.

        :return: True if any of the requirements are satisfied, false otherwise
        """
        for requirement in self.requirements:
            if requirement.is_installed():
                return True
        return False
