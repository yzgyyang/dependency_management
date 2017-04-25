import unittest

from dependency_management.requirements.PythonImportRequirement import (
                        PythonImportRequirement)


class PythonImportRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(PythonImportRequirement('setuptools')),
                         'setuptools')
        self.assertEqual(str(PythonImportRequirement('setuptools', '19.2')),
                         'setuptools 19.2')
        self.assertEqual(str(PythonImportRequirement('setuptools',
                                                     '19.2',
                                                     ['setuptools.setup'])),
                         'setuptools 19.2')

    def test_default_imports(self):
        c = PythonImportRequirement('radon')
        self.assertEqual(c.imports, ['radon'])

    def test_import_success(self):
        c = PythonImportRequirement(
            'simplejson', '', ['simplejson.dumps'])
        c.install_package()
        self.assertTrue(c.is_importable())
        self.assertTrue(hasattr(c, 'dumps'))

        r = PythonImportRequirement('radon',
                                    '1.4.0',
                                    ['radon.complexity.cc_visit'])
        r.install_package()
        self.assertTrue(r.is_importable())
        self.assertTrue(hasattr(r, 'cc_visit'))

        y = PythonImportRequirement('pyyaml',
                                    '',
                                    ['yaml.dump'])
        y.install_package()
        self.assertTrue(y.is_importable())
        self.assertTrue(hasattr(y, 'dump'))

    def test_import_fail(self):
        uut = PythonImportRequirement('some_bad_package',
                                      '',
                                      ['some_bad_package.no_mod'])
        self.assertFalse(uut.is_importable())
        self.assertFalse(hasattr(uut, 'no_mod'))

    def test_import_more_than_one_submodule_success(self):
        r = PythonImportRequirement('radon',
                                    '1.4.0',
                                    ['radon.complexity', 'radon.visitors'])
        r.install_package()
        self.assertTrue(r.is_importable())
        self.assertTrue(hasattr(r, 'complexity'))
        self.assertTrue(hasattr(r, 'visitors'))

    def test_import_more_than_one_submodule_fail(self):
        rad = PythonImportRequirement('radon',
                                      '1.4.0',
                                      ['radon.complexity', 'radon.bad_module'])
        rad.install_package()
        self.assertFalse(rad.is_importable())
        self.assertTrue(hasattr(rad, 'complexity'))
        self.assertFalse(hasattr(rad, 'bad_module'))

    def test_import_module_success(self):
        s = PythonImportRequirement('colorit', '', ['colorit.bold'])
        s.install_package()
        s._create_import_attributes()
        self.assertTrue(hasattr(s, 'bold'))

    def test_import_module_raises(self):
        y = PythonImportRequirement('pyyaml', '', ['yaml.bad_mod'])
        with self.assertRaises(ImportError,
                               msg="cannot import name 'bad_mod'"):
            y._create_import_attributes()
        self.assertFalse(hasattr(y, 'bad_mod'))

    def test_import_package_success(self):
        a = PythonImportRequirement('autoflake', '', ['autoflake'])
        a.install_package()
        a._create_import_attributes()
        self.assertTrue(hasattr(a, 'autoflake'))

    def test_import_package_raises(self):
        h = PythonImportRequirement('some_bad_package',
                                    '',
                                    ['some_bad_package'])
        with self.assertRaises(ImportError,
                               msg="No module named 'hello'"):
            h._create_import_attributes()
        self.assertFalse(hasattr(h, 'some_bad_package'))
