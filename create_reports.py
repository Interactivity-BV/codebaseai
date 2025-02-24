"""
This script generates analysis reports based on the analysis of a codebase using AI. It processes reports generated by 
various tools like Vulture, Pylint, Radon CC, and Radon MI, and uses OpenAI to create summaries and suggestions for 
improvement. The script requires an OpenAI API key and uses environment variables for configuration.
"""

from langchain_core.prompts import ChatPromptTemplate

import os
import sys
import argparse
import logging
from ai import run_chain

# Parse command line arguments
parser = argparse.ArgumentParser(description="Create reports based on the analysis of a codebase using AI.")
parser.add_argument("-r", "--report_dir", required=True, help="The directory of reports by analyse_codebase.py.")
parser.add_argument("-o", "--output_dir", required=True, help="The directory to save the analysis reports generated by AI.")
parser.add_argument("-l", "--log_file", default='./analysis.log', help="The file to save the log.")
parser.add_argument("-m", "--model_name", default="gpt-4o", help="OpenAI model name.")
args = parser.parse_args()

# Configure logging
logging.basicConfig(
    filename=args.log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a logger object
logger = logging.getLogger(__name__)

REPORT_DIR = args.report_dir
if not REPORT_DIR.endswith('/'):
    REPORT_DIR += '/'
OUTPUT_DIR = args.output_dir
if not OUTPUT_DIR.endswith('/'):
    OUTPUT_DIR += '/'
MODEL_NAME = args.model_name

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_vulture_report(report):
    """
    Creates a summary report for Vulture analysis using AI.

    Args:
        report (str): The Vulture analysis report content.

    Returns:
        str: The AI-generated summary of the Vulture report.

    Side Effects:
        Writes the summary to a markdown file in the output directory.
    """
    prompt = ChatPromptTemplate.from_template("""
        Here is the output of a vulture analysis report that lists unused code, functions, and variables in a Python project.

        Please:
         - Summarize the unused functions, variables, and classes.
         - Identify any critical-looking unused code that might need further investigation.
         - Suggest which unused code can likely be removed safely and which might need a review for hidden dependencies
                                                

        Report:
         {input}
        """
    )
    
    output_file_path = os.path.join(OUTPUT_DIR, "vulture_analysis_summary_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, report, model_name=MODEL_NAME)
        output_file.write(ai_response)
    logger.info(f"Vulture analysis summary saved to {output_file_path}")
    return ai_response

def create_pylint_report(report):
    """
    Creates a summary report for Pylint analysis using AI.

    Args:
        report (str): The Pylint analysis report content.

    Returns:
        str: The AI-generated summary of the Pylint report.

    Side Effects:
        Writes the summary to a markdown file in the output directory.
    """
    prompt = ChatPromptTemplate.from_template("""
        Here is the output of a pylint analysis report that highlights code quality issues in a Python project.
                                              
        Please:

         - Summarize the most frequent and severe linting issues (e.g., errors, warnings, and convention violations).
         - Group the issues by type and explain their impact on code quality.
         - Suggest specific fixes or refactoring strategies for the most critical issues.
         - Provide an overall quality assessment of the codebase based on this report.

        Report:
         {input}
        """
    )
    output_file_path = os.path.join(OUTPUT_DIR, "pylint_report_summary_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, report) 
        output_file.write(ai_response)
    logger.info(f"Pylint analysis summary saved to {output_file_path}")
    return ai_response

def create_radon_cc_report(report):
    """
    Creates a summary report for Radon CC analysis using AI.

    Args:
        report (str): The Radon CC analysis report content.

    Returns:
        str: The AI-generated summary of the Radon CC report.

    Side Effects:
        Writes the summary to a markdown file in the output directory.
    """
    prompt = ChatPromptTemplate.from_template("""
        Here is the output of a radon cc analysis report that measures cyclomatic complexity for functions and methods in a Python project.

        Please:

         - Highlight the functions or methods with the highest complexity scores and explain their impact on maintainability.
         - Suggest ways to refactor or simplify the most complex functions/methods.
         - Provide a general summary of the codebase’s complexity and recommendations for improvement.
                                              

        Report:
         {input}
        """
    )
    output_file_path = os.path.join(OUTPUT_DIR, "radon_cc_report_summary_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, report)
        output_file.write(ai_response)
    logger.info(f"Radon cc analysis summary saved to {output_file_path}")
    return ai_response

def create_radon_mi_report(report):
    """
    Creates a summary report for Radon MI analysis using AI.

    Args:
        report (str): The Radon MI analysis report content.

    Returns:
        str: The AI-generated summary of the Radon MI report.

    Side Effects:
        Writes the summary to a markdown file in the output directory.
    """
    prompt = ChatPromptTemplate.from_template("""
        Here is the output of a radon mi analysis report that measures the maintainability index of each file in a Python project.

        Please:
         - List the files with the lowest maintainability index scores.
         - Identify common patterns or reasons for low scores.
         - Suggest specific improvements for increasing maintainability (e.g., reducing complexity, adding comments, splitting large files).
         - Provide an overall assessment of the codebase’s maintainability.
                                              

        Report:
         {input}
        """
    )
    output_file_path = os.path.join(OUTPUT_DIR, "radon_mi_report_summary_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, report) 
        output_file.write(ai_response)
    logger.info(f"Radon mi analysis summary saved to {output_file_path}")
    return ai_response

def create_full_report(report):
    """
    Creates a full summary report combining all analysis reports using AI.

    Args:
        report (str): The combined content of all analysis reports.

    Returns:
        str: The AI-generated full summary report.

    Side Effects:
        Writes the summary to a markdown file in the output directory.
    """
    prompt = ChatPromptTemplate.from_template("""
        Here is the output of a full analysis report that includes vulture, pylint, radon cc, and radon mi reports for a Python project.

        Please:

         - Summarize the key findings from each report.
         - Identify common issues across the reports and suggest high-level strategies for improvement.
         - Provide an overall assessment of the codebase’s quality, complexity, and maintainability.
                                              

        Report:
         {input}
        """
    )
    output_file_path = os.path.join(OUTPUT_DIR, "full_analysis_summary_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, report) 
        output_file.write(ai_response)
    logger.info(f"Full analysis summary saved to {output_file_path}")
    return ai_response

def create_report_with_openai():
    """
    Generates analysis reports using OpenAI.

    Side Effects:
        Processes each report file in the report directory and generates corresponding AI summaries.
        Writes the summaries to markdown files in the output directory.
    """
    logger.info("Generating analysis reports using OpenAI...")
    full_report = ""
    # Generate reports for each file in the report directory
    for report_file in os.listdir(REPORT_DIR):
        logger.info(f"Processing report: {report_file}")
        if report_file.endswith(".txt"):
            report_path = os.path.join(REPORT_DIR, report_file)
            with open(report_path, "r") as f:
                report = f.read()
                if "vulture_report.txt" in report_file:
                    full_report += "Vulture Report:\n" + create_vulture_report(report) + "\n\n"
                elif "pylint_report.txt" in report_file:
                    full_report += "Pylint Report:\n" + create_pylint_report(report) + "\n\n"
                elif "radon_cc_report.txt" in report_file:
                    full_report += "Radon cc Report:\n" + create_radon_cc_report(report) + "\n\n" 
                elif "radon_mi_report.txt" in report_file:
                    full_report += "Radon mi Report:\n" + create_radon_mi_report(report) + "\n\n"
    if len(full_report) > 0:
        create_full_report(full_report)
    logger.info(f"Reports generated")

def main():
    """
    Main function to create analysis reports using OpenAI.

    Side Effects:
        Checks the existence of the report directory and initiates the report generation process.
        Logs errors and information messages.
    """
    if not os.path.exists(REPORT_DIR):
        logger.error(f"Error: Directory {REPORT_DIR} does not exist.")
        sys.exit(1)

    logger.info(f"Analyzing reports at: {REPORT_DIR}")
    logger.info(f"AI reports will be saved to: {OUTPUT_DIR}")
    create_report_with_openai()

if __name__ == "__main__":
    main()