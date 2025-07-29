"""
This script analyzes a codebase and generates reports by adding docstrings to Python scripts using AI. 
It utilizes OpenAI's language model to improve the readability and maintainability of the codebase by 
automatically generating docstrings for functions and classes in the scripts.

The script requires an OpenAI API key to function, which should be set in the environment variables.
"""

import os
import argparse
import re

from commands import run_command
import logging
from langchain_core.prompts import ChatPromptTemplate
import json
from pathlib import Path

from _init_codebaseai_ import LLM, initialize_logger, load_run_chain, get_directory_path_or_exit, get_model_name

# Parse command line arguments
parser = argparse.ArgumentParser(description="Create reports based on the analysis of a codebase using AI.")
parser.add_argument("-c", "--codebase_dir", required=True, help="The directory of the codebase (module level) to analyze.")
parser.add_argument("-o", "--output_dir", required=True, help="The directory to save the analysis reports.")
parser.add_argument("-t", "--title", default="Repository documentation", help="Title of the documentation")
parser.add_argument("-d", "--developer", default="Personal", help="Name of the developer / owner")
parser.add_argument("-e", "--email", default="", help="E-mail address")
parser.add_argument("-u", "--url", default="", help="URL of the website / repository")
parser.add_argument("-D", "--description", default="AI-generated documentation", help="Short description on the documentation")
parser.add_argument("-l", "--log_file", default='./analysis.log', help="The file to save the log.")
parser.add_argument("-L", "--log_level", default='INFO', help="The loglevel.")
parser.add_argument("-S", "--log_silent", help="Suppress the log to stdout.", action='store_false')
parser.add_argument("-m", "--model_name", default="", help="default model name.")
parser.add_argument("-M", "--llm_name", default=LLM, help="default lmm.")
parser.add_argument("-P", "--python", default="T", help="Create also docstrings, not only create markdown files (T/F)")

args = parser.parse_args()

#initialize logger
initialize_logger(args.log_file, args.log_level,args.log_silent)
logger = logging.getLogger(__name__)

run_chain = load_run_chain(args.llm_name)
CODEBASE_DIR = get_directory_path_or_exit(args.codebase_dir)
OUTPUT_DIR = get_directory_path_or_exit(args.output_dir, create_if_not_exists=True)
OUTPUT_CODE = Path(os.path.join(OUTPUT_DIR, os.path.basename(os.path.abspath(CODEBASE_DIR))))
OUTPUT_DOCS = Path(os.path.join(OUTPUT_CODE,"docs"))

# Ensure output directory exists
os.makedirs(OUTPUT_DOCS, exist_ok=True)

TITLE = args.title
DEVELOPER = args.developer
MAIL = args.email
LINK = args.url
DESCRIPTION = args.description
MODEL_NAME = get_model_name(args.llm_name, args.model_name)


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
        improve readability and maintainability. Output should be a Python script with proper docstrings, so leave out backticks, other formatting and notes.
                                              
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

    output_file_path = OUTPUT_CODE / str(os.path.relpath(script, CODEBASE_DIR))
    logger.info(f"Reading {script} writing {output_file_path}")

    if os.path.exists(output_file_path) and os.path.getmtime(script) < os.path.getmtime(output_file_path):
        logger.info(f"Skipping {script} as it is not newer than the existing output.")
        return
    else:
        logger.info(f"Processing {script} to create docstrings.")

    ai_response = ""
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(script, "r") as file:
        script = file.read()

    if len(script.strip()) == 0:
        logger.info(f"Skipping empty file: {output_file_path} ")
        return

    #Try capturing only python
    RE = re.compile(r"```(?:python)(.*?)```", re.DOTALL | re.IGNORECASE)

    #query llm
    ai_response = run_chain(prompt, script, MODEL_NAME)

    #capture Python code from response
    python_ai_response = RE.search(ai_response).group(1)

    #write output file
    with open(output_file_path, "w") as output_file:
        if python_ai_response :
            output_file.write(python_ai_response)
        else:
            logger.warn("There was no python block in the ai response, writing the entire response to {output_file}")
            output_file.write(ai_response)
    logger.info(f"Docstrings created in {output_file_path}")


def create_mdocs_report(documentation):
    """
    Generates a summary report of the documentation using AI.

    Args:
        documentation (str): The documentation content to summarize.

    Returns:
        str: The AI-generated summary of the documentation.

    Side Effects:
        Writes the summary to a file in the output directory.
        Logs the process of creating the summary.
    """
    prompt = ChatPromptTemplate.from_template("""
        Here is the output of a mdocs analysis of the docstrings in this module.
        Summarize the key functionalities and workflows described in this documentation.md. 
        Highlight the main modules, their responsibilities, and how they interact. 
        Additionally, point out any unique features or design patterns used.

        Documentation:
         {input}
        """
    )
    
    output_file_path = OUTPUT_DOCS / "documentation_summary_ai.md"
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, documentation, MODEL_NAME)
        output_file.write(ai_response)
    logger.info(f"Documentation summary saved to {output_file_path}")
    return ai_response

def create_mdocs_onboarding(documentation):
    """
    Creates an onboarding guide for new developers based on the documentation.

    Args:
        documentation (str): The documentation content to use for the onboarding guide.

    Returns:
        str: The AI-generated onboarding guide.

    Side Effects:
        Writes the onboarding guide to a file in the output directory.
        Logs the process of creating the onboarding guide.
    """
    prompt = ChatPromptTemplate.from_template("""
        Here is the output of a mdocs analysis of the docstrings in this module.
        Create an onboarding guide for new developers based on the documentation.md. 
        Explain the codebase structure, key modules to focus on, and the typical development workflow.

        Documentation:
         {input}
        """
    )
    
    output_file_path = OUTPUT_DOCS / "documentation_onboarding_ai.md"
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, documentation, MODEL_NAME)
        output_file.write(ai_response)
    logger.info(f"Documentation onboarding saved to {output_file_path}")
    return ai_response

def process_mdocs():
    """
    Processes the mdocs settings and generates the documentation file.

    Side Effects:
        Writes the mdocs settings to a JSON file.
        Executes shell commands to generate and move the documentation file.
        Logs the process of generating the documentation.
    """
    config = {"title": f"{TITLE}", "description": f"{DESCRIPTION}", "developer": f"{DEVELOPER}", "mail": f"{MAIL}", "link": f"{LINK}"}
    mdocs_settings_path = CODEBASE_DIR /"mdocs_settings.json"
    logger.info(f"Writing mdocs settings file to {mdocs_settings_path}")
    with open(mdocs_settings_path, "w") as settings_file:
        json.dump(config, settings_file, indent=4)

    documentation_path = CODEBASE_DIR / "documentation.md"
    documentation_target_path = OUTPUT_DOCS / "documentation.md"
    logger.info(f"mdocs running on {CODEBASE_DIR.resolve()}")
    run_command(f"cd {CODEBASE_DIR.resolve()} && mdocs .", output_file=None, logger=logger)
    run_command(f"mv {documentation_path.resolve()} {documentation_target_path.resolve()}", output_file=None, logger=logger)

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


    exclude = ['.git', '__pycache__', 'venv', 'node_modules', '.idea', '.vscode', '.pytest_cache', '.mypy_cache', '.env']
    if args.python in ['T', 't']:
        logger.info(f"Analyzing scripts at: {CODEBASE_DIR}")
        logger.info(f"Scripts with docstrings will be saved to: {OUTPUT_DIR}")
        for root, dirs, files in os.walk(CODEBASE_DIR, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude]
            for file in files:
                if file.endswith(".py"):
                    script_path = Path(os.path.join(root, file))
                    create_docstrings(script_path)

    logger.info("Creating mdocs file")
    process_mdocs()
    documentation_path = OUTPUT_DOCS / "documentation.md"
    if os.path.exists(documentation_path):
        with open(documentation_path, "r") as doc_file:
            documentation = doc_file.read()
        logger.info("Creating report")
        codebaseai.create_mdocs_report(documentation, output_docs=OUTPUT_DOCS, run_chain=run_chain, model_name=MODEL_NAME)
        logger.info("Creating onboarding")
        codebaseai.create_mdocs_onboarding(documentation, output_docs=OUTPUT_DOCS, run_chain=run_chain, model_name=MODEL_NAME)
    else:
        logger.error(f"Error: {documentation_path} does not exist.")

if __name__ == "__main__":
    main()