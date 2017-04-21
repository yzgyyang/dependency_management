from dependency_management.requirements.PipRequirement import PipRequirement


class PythonImportRequirement(PipRequirement):
    """
    This class is a subclass of ``PipRequirement``. It specifies the python
    package requirement and provide functions to import modules.
    """

    def __init__(self,
                 package,
                 version="",
                 imports: list=None):
        """
        Constructs a new ``PythonImportRequirement`` using the
        ``PipRequirement``

        :param package:
                A string with the name of the package to be installed.
        :param version:
                A version string. Leave empty to specify latest version.
        :param imports:
                A list of module attributes(dotted path representation) to be
                imported. Leave empty to specify package name as required
                import.
        """
        if not imports:
            self.imports = [package]
        else:
            self.imports = imports
        PipRequirement.__init__(self, package, version)

    def _create_import_attributes(self):
        """
        Imports the specified module attributes and provide them as instance
        attributes.

        :raises ImportError: Module is not present/installed.
        """
        for to_import in self.imports:
            sub_package = to_import.split('.')[-1]
            path = '.'.join(to_import.split('.')[:-1])
            if path:
                exec('from ' + path + ' import ' + sub_package)
                setattr(self, sub_package, eval(sub_package))
            else:
                exec('import ' + sub_package)
                setattr(self, sub_package, eval(sub_package))

    def is_importable(self):
        """
        Checks if the requirement is importable

        :return:
            True if package is installed and the module attributes are
            imported
        """
        try:
            self._create_import_attributes()
            return True
        except ImportError:
            return False
