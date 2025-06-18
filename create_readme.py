import os
import argparse
import logging
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from _init_codebaseai_ import LLM, initialize_logger, load_run_chain, get_directory_path_or_exit, get_model_name


"""
This script analyzes a codebase and creates or updates a README.md file using AI. 
It extracts information from various files in the codebase and uses an AI model to generate a comprehensive README.md.
"""

# Parse command line arguments
parser = argparse.ArgumentParser(description="Create / update README based on the analysis of a codebase using AI.")
parser.add_argument("-c", "--codebase_dir", required=True, help="The directory of the codebase (module level) to analyze.")
parser.add_argument("-o", "--output", required=True, help="The location of the README file.")
parser.add_argument("-t", "--title", default="Repository documentation", help="Title of the documentation")
parser.add_argument("-l", "--log_file", default='./analysis.log', help="The file to save the log.")
parser.add_argument("-L", "--log_level", default='INFO', help="The loglevel.")
parser.add_argument("-S", "--log_silent", help="Suppress the log to stdout.", action='store_false')
parser.add_argument("-m", "--model_name", default="", help="default model name.")
parser.add_argument("-M", "--llm_name", default=LLM, help="default lmm.")

args = parser.parse_args()

#initialize logger
initialize_logger(args.log_file, args.log_level,args.log_silent)
logger = logging.getLogger(__name__)

run_chain = load_run_chain(args.llm_name)
CODEBASE_DIR = get_directory_path_or_exit(args.codebase_dir)
OUTPUT_DOC = Path(args.output)

if not "README.md" in str(OUTPUT_DOC):
    OUTPUT_DOC /= 'README.md'

TITLE = args.title
MODEL_NAME = get_model_name(args.llm_name, args.model_name)


def create_readme(input):
    """
    Generates or updates a README.md file based on the provided input using an AI model.

    Args:
        input (str): The input text containing information extracted from the codebase.

    Returns:
        str: The AI-generated README.md content.

    Side Effects:
        - Writes the generated README.md content to the specified output file.
        - Logs the success or failure of the README.md creation.

    Raises:
        - Logs an error if the AI response is empty.
    """
    prompt = ChatPromptTemplate.from_template("""
    A README.md serves as the main entry point for users and developers to understand and use the project. It should be clear, structured, and 
    informative.

    Please provide the README.md for the project. If the project already has a README.md, please update it: add and correct it when necessary. 
    Keep information present in the README when still relevant, and remove or update outdated information. Feel free to add links and additional 
    sections which you think are missing from the README. Suggestions for sections include: 
    - Project Title & Description
    - Installation Instructions
    - Usage Guide
    - Features
    - Modules Overview
    - Configuration & Customization
    - Testing & Debugging
    - Contributing Guide (for open-source projects)
    - License & Author Information
    
    The files you can use as a reference are listed below, using $$$$$ as a separator:
    
    {input}
        """
    )

    ai_response = ""
    ai_response = run_chain(prompt, input, MODEL_NAME)
    if ai_response.startswith("```"):
        ai_response = ai_response[9:].strip()
    if ai_response.endswith("```"):
        ai_response = ai_response[:-3]

    if len(ai_response.strip()) > 0:
        with open(OUTPUT_DOC, "w") as output_file:
            output_file.write(ai_response)
        logger.info(f"README.md created in {OUTPUT_DOC}")
    else:
        logger.error("AI response was empty file")
    return ai_response

def main():
    """
    Main function to analyze the codebase and generate or update the README.md file.

    Side Effects:
        - Logs the analysis process and any errors encountered.
        - Calls the create_readme function to generate the README.md content.
    """

    logger.info(f"Analyzing codebase at: {CODEBASE_DIR}")
    logger.info(f"README.md: {OUTPUT_DOC}")

    input_text = f"$$$$$ Title:  {TITLE} $$$$$\n\n"
    readme_text = "$$$$$ NO EXISTING README.md, please create new one $$$$$\n"

    exclude = ['.git', '__pycache__', 'venv', 'node_modules', '.idea', '.vscode', '.pytest_cache', '.mypy_cache', '.env']
    for root, dirs, files in os.walk(CODEBASE_DIR,topdown=True):

        dirs[:] = [d for d in dirs if d not in exclude]

        for file in files:
            script_path = os.path.join(root, file)
            if file == "README.md":
                with open(script_path, "r") as readme_file:
                    readme_text = f"\n$$$$$ Existing README.md $$$$$\n" + readme_file.read() + f"\n$$$$$ End of existing README.md $$$$$\n"
            if file == "LICENSE":
                with open(script_path, "r") as license_file:
                    input_text += f"\n$$$$$ License file {file} $$$$$\n" + license_file.read() + f"\n$$$$$ End of license file {file} $$$$$\n"

            if file.endswith(".md") and file != "README.md":
                with open(script_path, "r") as doc_file:
                    input_text += f"\n$$$$$ Documentation file {script_path} $$$$$\n" + doc_file.read() + f"\n$$$$$ End of documentation file {script_path} $$$$$\n"

            if file.endswith(".py"):
                with open(script_path, "r") as python_file:
                    python_script = python_file.read()
                    if "__main__" in python_script:
                        input_text += f"\n$$$$$ Python script {script_path} $$$$$\n" + python_script + f"\n$$$$$ End of Python script {script_path} $$$$$\n"
            if file == "requirements.txt":
                with open(script_path, "r") as req_file:
                    input_text += f"\n$$$$$ Requirements file {file} $$$$$\n" + req_file.read() + f"\n$$$$$ End of requirements file {file} $$$$$\n"

        input_text += readme_text

    create_readme(input_text)

if __name__ == "__main__":
    main()