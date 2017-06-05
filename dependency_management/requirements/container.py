from collections import Iterable, OrderedDict


class RequirementSet(Iterable):
    """An abstract class all requirement sets should subclass."""


class AddressableRequirementSet(OrderedDict, RequirementSet):
    """
    A requirement set where members can be accessed by member type and name.

    >>> from dependency_management.requirements import PackageRequirement
    >>> class FakeRequirement(PackageRequirement.PackageRequirement):
    ...     def __repr__(self):
    ...         return '%s(%s)' % (
    ...             type(self).__name__,
    ...             ','.join((self.package, self.version, self.repo)))
    ...
    >>> rs = AddressableRequirementSet()
    >>> r = FakeRequirement('npm', 'eslint')
    >>> rs.add(r)
    >>> len(rs)
    1
    >>> rs
    AddressableRequirementSet([('npm.eslint', FakeRequirement(eslint,,))])

    Functionally identical to a set with identity of each member
    determined by the package type and name.

    >>> rs.add(r)
    >>> len(rs)
    1
    >>> r2 = FakeRequirement('npm', 'eslint')
    >>> rs.add(r2)
    >>> len(rs)
    1
    >>> r2 = FakeRequirement('npm', 'eslint2')
    >>> rs.add(r2)
    >>> len(rs)
    2
    >>> list(rs.keys())
    ['npm.eslint', 'npm.eslint2']

    Members can be provided to the constructor.

    >>> rs = AddressableRequirementSet(
    ...     FakeRequirement('npm', 'eslint'),
    ...     FakeRequirement('npm', 'eslint2'),
    ... )
    >>> list(rs.keys())
    ['npm.eslint', 'npm.eslint2']

    Existing sets can have additional members added.

    >>> r3 = FakeRequirement('pip', 'coala-utils')
    >>> rs.add(r3)
    >>> len(rs)
    3
    >>> list(rs.keys())
    ['npm.eslint', 'npm.eslint2', 'pip.coala-utils']

    Members can be addressed using keys.

    >>> rs['pip.coala-utils'] is r3
    True
    >>> rs['pip.foo']
    Traceback (most recent call last):
        ...
    KeyError: 'pip.foo'

    Members can also be addressed using dot notation.

    >>> rs.pip.coala_utils is r3
    True

    >>> rs.pip2.foo
    Traceback (most recent call last):
        ...
    AttributeError: pip2
    >>> rs.pip.foo
    Traceback (most recent call last):
        ...
    AttributeError: pip.foo
    """

    def __init__(self, *requirements):
        super().__init__()
        for requirement in requirements:
            self.add(requirement)

    def add(self, requirement):
        """
        Add a requirement to the set.

        :param requirement: PackageRequirement to add
        """
        key = requirement.type + '.' + requirement.package
        self[key] = requirement

    def __getattr__(self, attr1):
        # Do not interfere with OrderedDict attr resolution on Python 3.4
        if attr1.startswith('_OrderedDict'):  # pragma Python 3.5,3.6: no cover
            return self.__getattribute__(attr1)

        if not any(name.startswith(attr1 + '.') or
                   name.startswith(attr1.replace('_', '-') + '.')
                   for name in self.keys()):
            raise AttributeError(attr1)

        class _DotAddressableWrapper:
            def __getattr__(self2, attr2):
                name = attr1 + '.' + attr2
                if name not in self and name.replace('_', '-') not in self:
                    raise AttributeError(name)
                return self.get(name, self.get(name.replace('_', '-')))

        return _DotAddressableWrapper()
