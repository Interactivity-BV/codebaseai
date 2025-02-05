"""
This script analyzes a codebase and generates reports by adding docstrings to Python scripts using AI. 
It utilizes OpenAI's language model to improve the readability and maintainability of the codebase by 
automatically generating docstrings for functions and classes in the scripts.

The script requires an OpenAI API key to function, which should be set in the environment variables.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import os
import sys
import argparse
import logging
import re
from dotenv import load_dotenv

# Parse command line arguments
parser = argparse.ArgumentParser(description="Create reports based on the analysis of a codebase using AI.")
parser.add_argument("-c", "--codebase_dir", required=True, help="The directory of the codebase to analyze.")
parser.add_argument("-o", "--output_dir", required=True, help="The directory to save the analysis reports.")
parser.add_argument("-l", "--log_file", default=os.path.join(os.path.dirname(__file__), 'analysis.log'), help="The file to save the log.")
args = parser.parse_args()

load_dotenv()

# Configure logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), args.log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a logger object
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    sys.exit(1)

CODEBASE_DIR = args.codebase_dir
if not CODEBASE_DIR.endswith('/'):
    CODEBASE_DIR += '/'
OUTPUT_DIR = args.output_dir
if not OUTPUT_DIR.endswith('/'):
    OUTPUT_DIR += '/'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

llmOpenAI = ChatOpenAI(temperature=0.1, model_name="gpt-4o", streaming=True, api_key=OPENAI_API_KEY)

def run_chain(prompt, input_data):
    """
    Runs a chain of runnables with the given input data.

    Args:
        prompt (ChatPromptTemplate): The prompt template to use for generating docstrings.
        input_data (str): The Python script content to process.

    Returns:
        str: The response from the AI model containing the script with added docstrings.

    Raises:
        Exception: If there is an error in invoking the chain.
    """
    chain = (
        {"python_script": RunnablePassthrough()}
        | prompt  
        | llmOpenAI
        | StrOutputParser()
    )
    response = chain.invoke(input_data)
    return response

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
         {python_script}
        """
    )

    cleaned_path = re.sub(r"^(\.\./|\.\/)+", "", script)

    output_file_path = os.path.join(OUTPUT_DIR, cleaned_path)
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

if __name__ == "__main__":
    main()

