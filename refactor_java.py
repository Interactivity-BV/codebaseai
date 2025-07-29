import logging
import argparse
import os
import codebaseai
from common import setup_logger, get_path, for_each_file

"""
This script refactors Java code using AI. It processes Java files in a specified directory, 
removes comments, extracts methods, refactors them using an AI model, and restores comments 
before saving the refactored code to an output directory. It also logs the process and handles 
command-line arguments for configuration.
"""

# Parse command line arguments
parser = argparse.ArgumentParser(description="Refactor Java code using AI.")
parser.add_argument("-j", "--java_dir", required=True, help="The Java package(s) directory to refactor.")
parser.add_argument("-o", "--output_dir", required=True, help="The directory to store the refactored source code.")
parser.add_argument("-l", "--log_file", default='./analysis.log', help="The file to save the log.")
parser.add_argument("-L", "--log_level", default='INFO', help="The loglevel.")
parser.add_argument("-S", "--log_silent", help="Suppress the log to stdout.", action='store_false')
parser.add_argument("-m", "--model_name", default="", help="default model name.")
parser.add_argument("-M", "--llm_name", default="", help="default lmm.")
parser.add_argument("-p", "--prompt", default="./refactoring_prompt.txt", help="The refactor prompt")
args = parser.parse_args()

#initialize logger
logger = logging.getLogger(__name__)
setup_logger(args.log_file, args.log_level,args.log_silent)


if __name__ == "__main__":


    SRC_DIR = get_path(args.java_dir)
    OUTPUT_DIR = get_path(args.output_dir, create_if_not_exists=True)
    MODEL_NAME = codebaseai.get_model_name(args.llm_name, args.model_name)
    #initialize ai
    codebaseai.load_llm(args.llm_name)
    run_chain = codebaseai.run_chain()

    connection = codebaseai.create_connection(MODEL_NAME)
    with open(args.prompt, 'r', encoding='utf-8') as prompt_file:
        prompt_text = prompt_file.read()
    for file_path in for_each_file(SRC_DIR, file_ext=".java"):
            output_file_path = OUTPUT_DIR / os.path.relpath(file_path, SRC_DIR)

            if os.path.exists(output_file_path) and os.path.getmtime(file_path) < os.path.getmtime(output_file_path):
                logger.info(f"Skipping {file_path} as it is not newer than the existing output.")
            else:
                logger.info(f"Refactoring {file_path}.")
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                refactored_code = codebaseai.extract_and_refactor_methods(file_path, prompt_text, connection, run_chain, MODEL_NAME)
                with open(output_file_path, "w") as output_file:
                    output_file.write(refactored_code)
                    logger.info(f"Refactored code written to: {output_file_path}")
                codebaseai.run_command(f"astyle -n --style=java {output_file_path}", None, logger)
    logger.info("Refactoring completed.")