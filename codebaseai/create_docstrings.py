import os
import re
import pathlib
import logging
import langchain_core.prompts as prompts

logger = logging.getLogger(__name__)

#Try capturing only python
RE_MATCH_PYTHON_BLOCK = re.compile(r"```(?:python)(.*?)```", re.DOTALL | re.IGNORECASE)


def create_docstrings(script:pathlib.Path, output_file_path:pathlib.Path, run_chain, model_name):
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
    prompt = prompts.ChatPromptTemplate.from_template("""
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

    logger.info(f"Reading {script} writing {output_file_path}")

    if os.path.exists(output_file_path) and os.path.getmtime(script) < os.path.getmtime(output_file_path):
        logger.info(f"Skipping {script} as it is not newer than the existing output.")
        return
    else:
        logger.info(f"Processing {script} to create docstrings.")

    script_content = ""
    with open(script, "r", encoding="utf-8") as script_file:
        script_content = script_file.read()

    if len(script_content.strip()) == 0:
        logger.info(f"Skipping empty file: {script} ")
        return

    #query llm
    ai_response = run_chain(prompt, script, model_name)

    #capture Python code from response
    python_ai_response = RE_MATCH_PYTHON_BLOCK.search(ai_response).group(1)

    #write output file
    with open(output_file_path, "w") as output_file:
        if python_ai_response :
            output_file.write(python_ai_response)
        else:
            logger.warn("There was no python block in the ai response, writing the entire response to {output_file}")
            output_file.write(ai_response)

    logger.info(f"Docstrings created in {output_file_path}")
