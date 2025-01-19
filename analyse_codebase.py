import os
import subprocess
import sys
import argparse
import logging

# Parse command line arguments
parser = argparse.ArgumentParser(description="Analyze a codebase using various tools.")
parser.add_argument("-c", "--codebase_dir", required=True, help="The directory of the codebase to analyze.")
parser.add_argument("-o", "--output_dir", required=True, help="The directory to save the analysis reports.")
parser.add_argument("-l", "--log_file", default=os.path.join(os.path.dirname(__file__), 'analysis.log'), help="The file to save the log.")
args = parser.parse_args()



# Configure logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), args.log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a logger object
logger = logging.getLogger(__name__)

# Define the codebase directory to analyze and the output directory
CODEBASE_DIR = args.codebase_dir
OUTPUT_DIR = args.output_dir
if not OUTPUT_DIR.endswith('/'):
    OUTPUT_DIR += '/'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_command(command, output_file):
    """
    Runs a shell command and writes its output to a file.
    """
    try:
        with open(output_file, "w") as f:
            subprocess.run(command, shell=True, check=True, stdout=f, stderr=subprocess.STDOUT)
        logger.info(f"Report generated: {output_file}")
    except subprocess.CalledProcessError as e:

        if e.returncode == 3:
            logger.warning(f"Warning: Command '{command}' failed with exit status 3 (Invalid argument).")
        elif e.returncode == 30:
            logger.warning(f"Warning: Command '{command}' failed with exit status 30 (Timeout).")
        else:
            logger.error(f"Error while running command: {command}\n{e}")

def analyze_with_vulture():
    """
    Finds unused code using vulture.
    """
    logger.info("Running vulture...")
    output_file = os.path.join(OUTPUT_DIR, "vulture_report.txt")
    command = f"vulture {CODEBASE_DIR}"
    run_command(command, output_file)

def analyze_with_pylint():
    """
    Checks code quality with pylint.
    """
    logger.info("Running pylint...")
    output_file = os.path.join(OUTPUT_DIR, "pylint_report.txt")
    command = f"pylint {CODEBASE_DIR} --output-format=text"
    run_command(command, output_file)

def analyze_with_radon():
    """
    Analyzes code complexity and maintainability using radon.
    """
    logger.info("Running radon cc (Cyclomatic Complexity)...")
    cc_output = os.path.join(OUTPUT_DIR, "radon_cc_report.txt")
    command_cc = f"radon cc {CODEBASE_DIR} -a -s"
    run_command(command_cc, cc_output)

    logger.info("Running radon mi (Maintainability Index)...")
    mi_output = os.path.join(OUTPUT_DIR, "radon_mi_report.txt")
    command_mi = f"radon mi {CODEBASE_DIR} -s"
    run_command(command_mi, mi_output)

def main():
    """
    Main function to run all analysis tools.
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
