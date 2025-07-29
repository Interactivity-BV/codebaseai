import logging
import json
import langchain_core.prompts as prompts
import codebaseai.commands as commands

logger = logging.getLogger(__name__)

def create_mdocs_report(documentation, output_docs, run_chain, model_name):
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
    prompt = prompts.ChatPromptTemplate.from_template("""
        Here is the output of a mdocs analysis of the docstrings in this module.
        Summarize the key functionalities and workflows described in this documentation.md. 
        Highlight the main modules, their responsibilities, and how they interact. 
        Additionally, point out any unique features or design patterns used.

        Documentation:
         {input}
        """
                                              )

    output_file_path = output_docs / "documentation_summary_ai.md"
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, documentation, model_name)
        output_file.write(ai_response)
    logger.info(f"Documentation summary saved to {output_file_path}")
    return ai_response

def create_mdocs_onboarding(documentation, output_docs, run_chain, model_name):
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
    prompt = prompts.ChatPromptTemplate.from_template("""
        Here is the output of a mdocs analysis of the docstrings in this module.
        Create an onboarding guide for new developers based on the documentation.md. 
        Explain the codebase structure, key modules to focus on, and the typical development workflow.

        Documentation:
         {input}
        """
                                              )

    output_file_path = output_docs / "documentation_onboarding_ai.md"
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, documentation, model_name)
        output_file.write(ai_response)
    logger.info(f"Documentation onboarding saved to {output_file_path}")
    return ai_response

def process_mdocs(config, codebase_dir, output_docs):
    """
    Processes the mdocs settings and generates the documentation file.

    Side Effects:
        Writes the mdocs settings to a JSON file.
        Executes shell commands to generate and move the documentation file.
        Logs the process of generating the documentation.
    """

    mdocs_settings_path = codebase_dir /"mdocs_settings.json"
    logger.info(f"Writing mdocs settings file to {mdocs_settings_path}")
    with open(mdocs_settings_path, "w") as settings_file:
        json.dump(config, settings_file, indent=4)

    documentation_path = codebase_dir / "documentation.md"
    documentation_target_path = output_docs / "documentation.md"
    logger.info(f"mdocs running on {codebase_dir.resolve()}")
    commands.run_command(f"cd {codebase_dir.resolve()} && mdocs .", output_file=None, logger=logger)
    commands.run_command(f"mv {documentation_path.resolve()} {documentation_target_path.resolve()}", output_file=None, logger=logger)
