import shutil


def is_executable_exists(executable):
    """
    Checks if executable exists in $PATH

    :return: True if executable eixsts in $PATH, false otherwise
    """
    return shutil.which(executable) is not None
