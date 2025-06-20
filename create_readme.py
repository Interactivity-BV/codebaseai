import argparse
import logging
import pathlib
import codebaseai
from common import setup_logger, get_path, for_each_file

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
parser.add_argument("-M", "--llm_name", default="", help="default lmm.")

args = parser.parse_args()

#initialize logger
logger = logging.getLogger(__name__)
setup_logger(args.log_file, args.log_level,args.log_silent)

def main():
    """
    Main function to analyze the codebase and generate or update the README.md file.

    Side Effects:
        - Logs the analysis process and any errors encountered.
        - Calls the create_readme function to generate the README.md content.
    """
    CODEBASE_DIR = get_path(args.codebase_dir)
    OUTPUT_DOC = pathlib.Path(args.output)
    TITLE = args.title

    if not "README.md" in str(OUTPUT_DOC):
        OUTPUT_DOC /= 'README.md'

    MODEL_NAME = codebaseai.get_model_name(args.llm_name, args.model_name)

    #initialize ai
    codebaseai.load_llm(args.llm_name)
    run_chain = codebaseai.run_chain()

    logger.info(f"Analyzing codebase at: {CODEBASE_DIR}")
    logger.info(f"README.md: {OUTPUT_DOC}")

    input_text = f"$$$$$ Title:  {TITLE} $$$$$\n\n"
    readme_text = "$$$$$ NO EXISTING README.md, please create new one $$$$$\n"

    for file_path in for_each_file(CODEBASE_DIR):
        logger.info(f"Processing file: {file_path.name}")
        if file_path.name == "README.md":
            with open(file_path, "r") as readme_file:
                readme_text = f"\n$$$$$ Existing README.md $$$$$\n" + readme_file.read() + f"\n$$$$$ End of existing README.md $$$$$\n"
        if file_path.name == "LICENSE":
            with open(file_path, "r") as license_file:
                input_text += f"\n$$$$$ License file {file_path} $$$$$\n" + license_file.read() + f"\n$$$$$ End of license file {file_path} $$$$$\n"

        if file_path.name.endswith(".md") and file_path.name != "README.md":
            with open(file_path, "r") as doc_file:
                input_text += f"\n$$$$$ Documentation file {file_path} $$$$$\n" + doc_file.read() + f"\n$$$$$ End of documentation file {file_path} $$$$$\n"

        if file_path.name.endswith(".py"):
            with open(file_path, "r") as python_file:
                python_script = python_file.read()
                if "__main__" in python_script:
                    input_text += f"\n$$$$$ Python script {file_path} $$$$$\n" + python_script + f"\n$$$$$ End of Python script {file_path} $$$$$\n"
        if file_path.name == "requirements.txt":
            with open(file_path, "r") as req_file:
                input_text += f"\n$$$$$ Requirements file {file_path} $$$$$\n" + req_file.read() + f"\n$$$$$ End of requirements file {file_path} $$$$$\n"

        input_text += readme_text

    codebaseai.create_readme(input_text, OUTPUT_DOC, run_chain, MODEL_NAME)

if __name__ == "__main__":
    main()