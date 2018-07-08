import os
import sys
from platform import system
from tempfile import TemporaryDirectory
import unittest

from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)


class ExecutableRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(ExecutableRequirement("python").is_installed() or
                        ExecutableRequirement("python3").is_installed() or
                        ExecutableRequirement(sys.executable).is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(ExecutableRequirement("some_bad_exec").is_installed())

    @unittest.skipIf(system() != 'Windows', 'Windows-specific test.')
    def test_installed_batch_requirements(self):
        for batchfile in ('some_executable.bat', 'some_executable.cmd'):
            uut = ExecutableRequirement(batchfile)

            self.assertFalse(uut.is_installed())

            with TemporaryDirectory() as tmp:
                # Create batch file.
                open(os.path.join(tmp, batchfile), 'w').close()

                # Add batch to path. sys.path doesn't work, changes in this
                # list aren't picked up.
                old_path = os.environ['PATH']
                os.environ['PATH'] = tmp + ';' + old_path

                self.assertTrue(uut.is_installed())

                # Remove again from path.
                os.environ['PATH'] = old_path
