"""Code used to execute Bash commands from Python."""
import subprocess  # nosec

from src.export_data.plantuml_compile import get_output_of_bash_command


def run_a_bash_command(await_compilation, bash_command, verbose):
    """Runs a bash commands from Python.

    :param await_compilation:
    :param bash_command:
    :param verbose:
    """
    if await_compilation:
        if verbose:
            subprocess.call(
                bash_command,
                shell=True,  # nosec
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        else:
            # pylint: disable=E1129
            # pylint: disable=R1732
            subprocess.call(
                bash_command,
                shell=True,  # nosec
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )
    else:
        if verbose:
            # pylint: disable=R1732
            subprocess.Popen(
                bash_command,
                shell=True,  # nosec
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        else:
            with subprocess.Popen(
                bash_command,
                shell=True,  # nosec
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            ) as process:
                get_output_of_bash_command(process)
