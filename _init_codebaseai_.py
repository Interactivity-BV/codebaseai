import os
import sys
import importlib
import logging
from pathlib import Path

# Create a logger object
logger = logging.getLogger(__name__)


LLM = 'open_ai'
LLM_MODEL = 'gtp-4o'

if 'LLM' in os.environ:
    LLM = os.environ['LLM']

#override model if set
if LLM_MODEL in os.environ :
    LLM_MODEL = os.environ['LLM_MODEL']

def get_model_name(llm, llm_model):
    if llm_model:
        return llm_model
    if LLM_MODEL in os.environ:
        return LLM_MODEL

    match llm:
        case 'open_ai' : return 'gtp-4o'
        case 'ollama' : return 'mistral'

def initialize_logger(log_file, log_level, log_silent):
    # Configure logging
    logging.basicConfig(
        filename=log_file,
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    # Configure logging to output to console
    if log_silent:
        root = logging.getLogger()
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)


def load_run_chain(llm_name):
    try:
        llm_module = importlib.import_module('ai_' + llm_name)
        logger.info(f"Using: module 'ai_{llm_name}'.")
        return llm_module.run_chain
    except:
        logger.error(f"Error: module 'ai_{llm_name}' not found.")
        sys.exit(1)

def get_directory_path_or_exit(directory, create_if_not_exists = False):
    path = Path(directory)
    if create_if_not_exists:
        if not os.path.exists(path):
            logger.info(f"Directory {path} does not exist, creating directory.")
            os.mkdir(path)
    else:
        if not os.path.exists(path):
            logger.error(f"Error: Directory {path} does not exist.")
            sys.exit(1)

    if not path.is_dir():
        logger.error(f"Error: {path} is not a directory.")
        sys.exit(1)
    return path
