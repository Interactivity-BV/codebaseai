"""
This script analyzes a codebase and generates reports by adding docstrings to Python scripts using AI. 
It utilizes OpenAI's language model to improve the readability and maintainability of the codebase by 
automatically generating docstrings for functions and classes in the scripts.

The script requires an OpenAI API key to function, which should be set in the environment variables.
"""


import os
import sys
import argparse
import re
from commands import run_command
import logging
from ai import run_chain
from langchain_core.prompts import ChatPromptTemplate
import json

# Parse command line arguments
parser = argparse.ArgumentParser(description="Create reports based on the analysis of a codebase using AI.")
parser.add_argument("-c", "--codebase_dir", required=True, help="The directory of the codebase to analyze.")
parser.add_argument("-o", "--output_dir", required=True, help="The directory to save the analysis reports.")
parser.add_argument("-t", "--title", default="Repository documentation", help="Title of the documentation")
parser.add_argument("-d", "--developer", default="Personal", help="Name of the developer / owner")
parser.add_argument("-e", "--email", default="", help="E-mail address")
parser.add_argument("-u", "--url", default="", help="URL of the website / repository")
parser.add_argument("-m", "--meta", default="AI-generated documentation", help="Short description / metadata on the documentation")
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


CODEBASE_DIR = args.codebase_dir
if not CODEBASE_DIR.endswith('/'):
    CODEBASE_DIR += '/'
OUTPUT_DIR = args.output_dir
if not OUTPUT_DIR.endswith('/'):
    OUTPUT_DIR += '/'
OUTPUT_DOCS = OUTPUT_DIR + "/docs/"

TITLE = args.title
DEVELOPER = args.developer
MAIL = args.email
LINK = args.url
DESCRIPTION = args.meta


# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DOCS, exist_ok=True)


def create_docstrings(script):
    """
    Creates docstrings for a given Python script using OpenAI's language model.

    Args:
        script (str): The path to the Python script file.

    Returns:
        str: The AI-generated script with added docstrings.

    Side Effects:
        Writes the modified script with docstrings to the output directory.
        Logs the process of creating docstrings.

    Raises:
        FileNotFoundError: If the script file does not exist.
    """
    prompt = ChatPromptTemplate.from_template("""
        This is a Python script, most likely without proper docstrings. Please add docstrings to the functions and classes in the script to 
        improve readability and maintainability. Output should be a Python script with proper docstrings, so leave out backticks and other formatting.
                                              
        Please:
        - add a docstring at the beginning of the script that describes its purpose.
        - add docstrings to all functions and classes in the script.
        - describe the purpose, inputs, and outputs of each function/class in the docstring.
        - follow the PEP 257 docstring conventions.
        - describe any side effects or exceptions raised by the functions/classes.
        - indicate (serious) issues, debug statements, or future work in the docstrings.        

        Python:
         {input}
        """
    )

    cleaned_path = re.sub(r"^(\.\./|\.\/)+", "", script)

    output_file_path = os.path.join(OUTPUT_DIR, cleaned_path)
    if os.path.exists(output_file_path) and os.path.getmtime(script) <= os.path.getmtime(output_file_path):
        logger.info(f"Skipping {script} as it is not newer than the existing output.")
        return ""
    ai_response = ""
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(script, "r") as file:
        script = file.read()
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, script)
        if ai_response.startswith("```"):
            ai_response = ai_response[9:].strip()
        if ai_response.endswith("```"):
            ai_response = ai_response[:-3]

        output_file.write(ai_response)
    logger.info(f"Docstrings created in {output_file_path}")
    return ai_response

def create_mdocs_report(documentation):
    prompt = ChatPromptTemplate.from_template("""
        Here is the output of a mdocs analysis of the docstrings in this module.
        Summarize the key functionalities and workflows described in this documentation.md. 
        Highlight the main modules, their responsibilities, and how they interact. 
        Additionally, point out any unique features or design patterns used.

        Documentation:
         {input}
        """
    )
    
    output_file_path = os.path.join(OUTPUT_DOCS, "documentation_summary_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, documentation)
        output_file.write(ai_response)
    logger.info(f"Documentation summary saved to {output_file_path}")
    return ai_response

def create_mdocs_onboarding(documentation):
    prompt = ChatPromptTemplate.from_template("""
        Here is the output of a mdocs analysis of the docstrings in this module.
        Create an onboarding guide for new developers based on the documentation.md. 
        Explain the codebase structure, key modules to focus on, and the typical development workflow.

        Documentation:
         {input}
        """
    )
    
    output_file_path = os.path.join(OUTPUT_DOCS, "documentation_onboarding_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, documentation)
        output_file.write(ai_response)
    logger.info(f"Documentation onboarding saved to {output_file_path}")
    return ai_response



def process_mdocs():
    config = {"title": f"{TITLE}", "description": f"{DESCRIPTION}", "developer": f"{DEVELOPER}", "mail": f"{MAIL}", "link": f"{LINK}"}
    mdocs_settings_path = os.path.join(CODEBASE_DIR, "mdocs_settings.json")
    with open(mdocs_settings_path, "w") as settings_file:
        json.dump(config, settings_file, indent=4)
    run_command(f"mdocs {OUTPUT_DIR}", output_file=None, logger=logger)
    run_command(f"mv {CODEBASE_DIR}documentation.md {OUTPUT_DOCS}", output_file=None, logger=logger)



def main():
    """
    Main function to add docstrings to Python scripts in a codebase using OpenAI.

    Side Effects:
        Logs the analysis process.
        Exits the program if the codebase directory does not exist.

    Raises:
        SystemExit: If the codebase directory does not exist.
    """
    if not os.path.exists(CODEBASE_DIR):
        logger.error(f"Error: Directory {CODEBASE_DIR} does not exist.")
        sys.exit(1)

    logger.info(f"Analyzing scripts at: {CODEBASE_DIR}")
    logger.info(f"Scripts with docstrings will be saved to: {OUTPUT_DIR}")
    for root, dirs, files in os.walk(CODEBASE_DIR):
        for file in files:
            if file.endswith(".py"):
                script_path = os.path.join(root, file)
                create_docstrings(script_path)
    logger.info("Creating mdocs file")
    process_mdocs()
    documentation_path = os.path.join(OUTPUT_DOCS, "documentation.md")
    if os.path.exists(documentation_path):
        with open(documentation_path, "r") as doc_file:
            documentation = doc_file.read()
        logger.info("Creating report")
        create_mdocs_report(documentation)
        logger.info("Creating onboarding")
        create_mdocs_onboarding(documentation)
    else:
        logger.error(f"Error: {documentation_path} does not exist.")


if __name__ == "__main__":
    main()

