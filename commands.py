import subprocess


def run_command(command, output_file, logger):
    """
    Runs a shell command and writes its output to a file.

    Args:
        command (str): The shell command to execute.
        output_file (str): The file path where the command's output will be written.

    Side Effects:
        Writes the command output to the specified file.
        Logs information, warnings, or errors based on the command execution result.

    Raises:
        subprocess.CalledProcessError: If the command execution fails.
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