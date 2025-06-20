import logging
import langchain_core.prompts as prompts

logger = logging.getLogger(__name__)

def create_readme(input, output_doc, run_chain, model_name):
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
    prompt = prompts.ChatPromptTemplate.from_template("""
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
    ai_response = run_chain(prompt, input, model_name)
    if ai_response.startswith("```"):
        ai_response = ai_response[9:].strip()
    if ai_response.endswith("```"):
        ai_response = ai_response[:-3]

    if len(ai_response.strip()) > 0:
        with open(output_doc, "w") as output_file:
            output_file.write(ai_response)
        logger.info(f"README.md created in {output_doc}")
    else:
        logger.error("AI response was empty file")
    return ai_response