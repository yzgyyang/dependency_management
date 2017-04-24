import shutil
import unittest
import unittest.mock

import sarge

from dependency_management.requirements.LuarocksRequirement import (
    LuarocksRequirement)


@unittest.skipIf(shutil.which('luarocks') is None,
                 'luarocks is not installed.')
class LuarocksRequirementTestCase(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(LuarocksRequirement('luarocks')), 'luarocks')
        self.assertEqual(str(LuarocksRequirement('luarocks', '2.4.2')),
                         'luarocks 2.4.2')

    def test_installed_requirement(self):
        with unittest.mock.patch('dependency_management.requirements.' +
                                 'LuarocksRequirement.run') as mock:
            patched = unittest.mock.Mock(spec=sarge.Pipeline)
            patched.returncode = 0
            mock.return_value = patched
            self.assertTrue(LuarocksRequirement('some_good_package').
                            is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(LuarocksRequirement('some_bad_package').is_installed())


@unittest.skipIf(shutil.which('luarocks') is None,
                 'luarocks is not installed.')
class LuarocksLuacheckRequirementTestCase(unittest.TestCase):

    def test_install(self):
        r = LuarocksRequirement('luacheck', '0.19.1')
        r.install_package()
        self.assertTrue(r.is_installed())
