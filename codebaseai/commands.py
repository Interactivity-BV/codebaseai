"""
This script provides a utility function to execute shell commands, handle their output, and log the execution details.

The main function, `run_command`, is designed to run a specified shell command, capture its output in a designated file, 
and log the process using a provided logger. It includes handling for specific exit codes with warnings and logs errors 
for other types of failures.
"""

import subprocess

def run_command(command, output_file, logger):
    """
    Executes a shell command and writes its output to a specified file, while logging the process.

    Args:
        command (str): The shell command to be executed.
        output_file (str): The path to the file where the command's output will be written.
        logger (logging.Logger): A logger instance used to log information, warnings, or errors.

    Side Effects:
        - Writes the command output to the specified file.
        - Logs information, warnings, or errors based on the command execution result.

    Raises:
        subprocess.CalledProcessError: Raised if the command execution fails.

    Notes:
        - If the command fails with exit status 3, a warning is logged indicating an invalid argument.
        - If the command fails with exit status 30, a warning is logged indicating a timeout.
        - Other non-zero exit statuses result in an error being logged.
        - Future work could include handling additional specific exit codes or improving error handling.
    """
    try:
        if output_file:
            with open(output_file, "w") as f:
                subprocess.run(command, shell=True, check=True, stdout=f, stderr=subprocess.STDOUT)
            logger.info(f"Output file generated: {output_file}")
        else:
            subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 3:
            logger.warning(f"Warning: Command '{command}' failed with exit status 3 (Invalid argument).")
        elif e.returncode == 30:
            logger.warning(f"Warning: Command '{command}' failed with exit status 30 (Timeout).")
        else:
            logger.error(f"Error while running command: {command}\n{e}")
