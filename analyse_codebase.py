"""
This script analyzes a codebase using various tools to assess code quality, complexity, and maintainability.
It utilizes tools such as Vulture, Pylint, and Radon to generate reports on unused code, code quality, and
code complexity. The results are saved in specified output directories for further review.
"""

import os
import sys
import argparse
import logging
from commands import run_command
from _init_codebaseai_ import LLM, initialize_logger, get_directory_path_or_exit, get_model_name


# Parse command line arguments
parser = argparse.ArgumentParser(description="Analyze a codebase using various tools.")
parser.add_argument("-c", "--codebase_dir", required=True, help="The directory of the codebase to analyze.")
parser.add_argument("-o", "--output_dir", required=True, help="The directory to save the analysis reports.")
parser.add_argument("-l", "--log_file", default='./analysis.log', help="The file to save the log.")
parser.add_argument("-L", "--log_level", default='INFO', help="The loglevel.")
parser.add_argument("-S", "--log_silent", help="Suppress the log to stdout.", action='store_false')

args = parser.parse_args()

#initialize logger
initialize_logger(args.log_file, args.log_level,args.log_silent)
logger = logging.getLogger(__name__)


# Define the codebase directory to analyze and the output directory
CODEBASE_DIR = get_directory_path_or_exit(args.codebase_dir)
OUTPUT_DIR = get_directory_path_or_exit(args.output_dir, create_if_not_exists=True)


def analyze_with_vulture():
    """
    Finds unused code using Vulture.

    Side Effects:
        Generates a report on unused code and saves it to the output directory.
        Logs the process of running Vulture.
    """
    logger.info("Running vulture...")
    output_file = OUTPUT_DIR / "vulture_report.txt"
    command = f"vulture {CODEBASE_DIR.resolve()}"
    return_code = run_command(command, output_file, logger)
    if return_code == 3 :
        logger.warning("Vulture found unused code")

def analyze_with_pylint():
    """
    Checks code quality with Pylint.

    Side Effects:
        Generates a code quality report and saves it to the output directory.
        Logs the process of running Pylint.
    """
    logger.info("Running pylint...")
    output_file = OUTPUT_DIR / "pylint_report.txt"
    command = f"pylint {CODEBASE_DIR} --output-format=text --exit-zero "
    run_command(command, output_file, logger)

def analyze_with_radon():
    """
    Analyzes code complexity and maintainability using Radon.

    Side Effects:
        Generates reports on cyclomatic complexity and maintainability index.
        Saves the reports to the output directory.
        Logs the process of running Radon.
    """
    logger.info("Running radon cc (Cyclomatic Complexity)...")
    cc_output = OUTPUT_DIR / "radon_cc_report.txt"
    command_cc = f"radon cc {CODEBASE_DIR} -a -s"
    run_command(command_cc, cc_output, logger)

    logger.info("Running radon mi (Maintainability Index)...")
    mi_output = OUTPUT_DIR / "radon_mi_report.txt"
    command_mi = f"radon mi {CODEBASE_DIR} -s"
    run_command(command_mi, mi_output, logger)

def main():
    """
    Main function to run all analysis tools.

    Side Effects:
        Checks the existence of the codebase directory.
        Runs Vulture, Pylint, and Radon analyses.
        Logs the overall process and results of the analysis.
        Exits the program if the codebase directory does not exist.
    """
    if not os.path.exists(CODEBASE_DIR):
        logger.error(f"Error: Directory {CODEBASE_DIR} does not exist.")
        sys.exit(1)

    logger.info(f"Analyzing codebase at: {CODEBASE_DIR}")
    logger.info(f"Reports will be saved to: {OUTPUT_DIR}")

    # Run analysis tools
    analyze_with_vulture()
    analyze_with_pylint()
    analyze_with_radon()

    logger.info(f"Code analysis completed. Check the reports in the '{OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    main()