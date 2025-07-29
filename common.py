import os
import sys
import pathlib
import logging

logger = logging.getLogger(__name__)

"""
Logger setup for the application.
"""
def setup_logger(log_file, log_level, log_to_stdout):
    # Configure logging
    logging.basicConfig(
        filename=log_file,
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    # Configure logging to output to console
    if log_to_stdout:
        root = logging.getLogger()
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

def get_path(directory, create_if_not_exists = False):
    """
    Get a pathlib.Path object for the specified directory. If the directory does not exist, it can be created.
    :param directory:
    :param create_if_not_exists:
    :return: Path object for the directory.
    """
    path = pathlib.Path(directory)
    if create_if_not_exists:
        if not os.path.exists(path):
            logger.info(f"Directory {path} does not exist, creating directory.")
            os.mkdir(path)
    else:
        if not os.path.exists(path):
            logger.error(f"Error: Directory {path} does not exist.")
            sys.exit(1)

    if not path.is_dir():
        logger.error(f"Error: {path} is not a directory.")
        sys.exit(1)
    return path

def for_each_file(directory, exclude= ['.git', '__pycache__', 'venv', 'node_modules', '.idea', '.vscode', '.pytest_cache', '.mypy_cache', '.env'], file_ext=None):
    """
    Walk through a directory and yield all files, excluding specified directories.

    Args:
        directory (str or Path): The directory to walk through.
        exclude (list): List of directories to exclude from the walk.
        file_ext (str): Optional file extension to filter files by. If None, all files are yielded.

    Yields:
    """

    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if file_ext is None or file.endswith(file_ext):
                yield pathlib.Path(os.path.join(root, file))
