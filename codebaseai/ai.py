import os
import sys
import importlib
import logging

logger = logging.getLogger(__name__)
llm_module = None

def load_llm(llm_name):
    """
    Loads the specified LLM module based on the provided name.

    Args: llm_name (str): The name of the LLM to load (e.g., 'open_ai', 'ollama').

    Exits if the module cannot be found.

    """
    try:
        global llm_module
        llm_module = importlib.import_module('codebaseai.ai_' + llm_name)
        logger.info(f"Using: module 'ai_{llm_name}'.")
    except:
        logger.error(f"Error: module 'ai_{llm_name}' not found.")
        sys.exit(1)

def run_chain() :
    """
    Runs the chain of runnables to process input data and generate an AI response.

    Returns:
        function: A function that can be used to run the LLM chain.
    """
    if llm_module is None:
        logger.error("LLM module not loaded. Please load the LLM module first.")
        sys.exit(1)

    return llm_module.run_chain


def create_connection(llm_model):
    """
    Creates a connection to the specified LLM module.

    Args:
        llm (str): The name of the LLM to use (e.g., 'open_ai', 'ollama').
        llm_model (str): The model name to use with the LLM.

    Returns:
        function: A function that can be used to run the LLM chain.
    """
    return llm_module.create_connection(model_name=llm_model)


def get_model_name(llm, llm_model):
    """
    Retrieves the model name for the specified LLM.
    :param llm:
    :param llm_model:
    :return: model_name (str): The name of the model to use with the LLM.
    """
    if not llm:
        llm = os.environ.get('LLM', 'open_ai')
        logger.info(f"Using default LLM: {llm}")
    if not llm_model:
        if llm == 'ollama':
            llm_model = os.environ.get('OLLAMA_MODEL_NAME', 'mistral')
            logger.info(f"Using default Ollama model: {llm_model}")
        else:
            llm_model = os.environ.get('LLM_MODEL', 'gpt-4o')
            logger.info(f"Using default LLM model: {llm_model}")
    else:
        logger.info(f"Using specified LLM model: {llm_model}")

    return llm_model