"""
This script analyzes a codebase and generates reports by adding docstrings to Python scripts using AI. 
It utilizes OpenAI's language model to improve the readability and maintainability of the codebase by 
automatically generating docstrings for functions and classes in the scripts.

The script requires an OpenAI API key to function, which should be set in the environment variables.
"""

import os
import argparse
import logging
import codebaseai
from common import setup_logger, get_path, for_each_file



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
parser.add_argument("-M", "--llm_name", default="", help="default lmm.")
parser.add_argument("-P", "--python", default="T", help="Create also docstrings, not only create markdown files (T/F)")
args = parser.parse_args()

#initialize logger
logger = logging.getLogger(__name__)
setup_logger(args.log_file, args.log_level,args.log_silent)


TITLE = args.title
DEVELOPER = args.developer
MAIL = args.email
LINK = args.url
DESCRIPTION = args.description


def main():
    """
    Main function to add docstrings to Python scripts in a codebase using OpenAI.

    Side Effects:
        Logs the analysis process.
        Exits the program if the codebase directory does not exist.

    Raises:
        SystemExit: If the codebase directory does not exist.
    """
    CODEBASE_DIR = get_path(args.codebase_dir)
    OUTPUT_DIR = get_path(args.output_dir, create_if_not_exists=True)
    OUTPUT_CODE = get_path(OUTPUT_DIR / os.path.basename(os.path.abspath(CODEBASE_DIR)), create_if_not_exists=True)
    OUTPUT_DOCS = get_path(OUTPUT_CODE /"docs", create_if_not_exists=True)
    MODEL_NAME = codebaseai.get_model_name(args.llm_name, args.model_name)

    #initialize ai
    codebaseai.load_llm(args.llm_name)
    run_chain = codebaseai.run_chain()


    if args.python in ['T', 't']:
        logger.info(f"Analyzing scripts at: {CODEBASE_DIR}")
        logger.info(f"Scripts with docstrings will be saved to: {OUTPUT_DIR}")
        if not os.path.exists(OUTPUT_CODE):
            for script_path in for_each_file(CODEBASE_DIR):
                if script_path.name.endswith(".py"):
                    output_file_path = OUTPUT_CODE / script_path.relative_to(CODEBASE_DIR)
                    codebaseai.create_docstrings(script_path, output_file_path, run_chain, MODEL_NAME)

    logger.info("Creating mdocs file")
    config = {"title": f"{TITLE}", "description": f"{DESCRIPTION}", "developer": f"{DEVELOPER}", "mail": f"{MAIL}", "link": f"{LINK}"}
    codebaseai.process_mdocs(config, CODEBASE_DIR, OUTPUT_DOCS)
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