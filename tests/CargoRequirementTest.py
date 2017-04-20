import shutil
import unittest
import unittest.mock

import sarge

from dependency_management.requirements.CargoRequirement import (
    CargoRequirement)


@unittest.skipIf(shutil.which('cargo') is None,
                 'cargo is not installed.')
class CargoRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(CargoRequirement('pulldown-cmark')),
                         'pulldown-cmark')
        self.assertEqual(str(CargoRequirement('pulldown-cmark', '0.0.14')),
                         'pulldown-cmark 0.0.14')

    def test_installed_requirement(self):
        with unittest.mock.patch('dependency_management.requirements.' +
                                 'CargoRequirement.run') as mock:
            patched = unittest.mock.Mock(spec=sarge.Pipeline)
            patched.returncode = 0
            mock.return_value = patched
            self.assertTrue(CargoRequirement('some_good_package').
                            is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(CargoRequirement('some_bad_package').is_installed())


@unittest.skipIf(shutil.which('cargo') is None,
                 'cargo is not installed.')
class CargoPulldownCmarkRequirementTestCase(unittest.TestCase):

    def test_install(self):
        r = CargoRequirement('pulldown-cmark', '0.0.14')
        r.install_package()
        self.assertTrue(r.is_installed())
