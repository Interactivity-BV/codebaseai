from codebaseai import logger
from run_command import run_command


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