from sarge import run, Capture


class Command:
    """
    Helper class for executing commands
    """

    REQUIREMENTS = {}

    @staticmethod
    def execute(command):
        """
        Runs the install command for the package given in a sub-process.

        :param return: Returns exit code of running the install command
        """
        if isinstance(command, list):
            command = " ".join(command)

        p = run(command, stdout=Capture(),
                stderr=Capture())
        return p
