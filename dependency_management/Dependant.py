class Dependant:
    """
    An object with dependencies. Put them into the class level ``REQUIREMENTS``
    attribute please.
    """

    @classmethod
    def missing_requirements(cls):
        """
        Yields all requirement objects that are unsatisfied.

        :return: An iterator over missing requirements.
        """
        for req in cls.REQUIREMENTS:
            ireqs = req.missing_requirements()
            try:
                yield next(ireqs)
            except StopIteration:  # No missing deps of requirement
                if not req.is_installed():
                    yield req
            else:
                yield from ireqs
                yield req
