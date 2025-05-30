# AI-documentation support
Module to analyse Python repositories using standard tools and AI

#### Developed by Interactivity

- GitHub: [https://github.com/Interactivity-BV/codebaseai](https://github.com/Interactivity-BV/codebaseai)

- Contact: [info@interactivity.nl](mailto:info@interactivity.nl)

## Module create_reports.py
### create_vulture_report( )

Creates a summary report for Vulture analysis using AI.

Args:
- report (str): The Vulture analysis report content.

Returns:
- str: The AI-generated summary of the Vulture report.

Side Effects:
    Writes the summary to a markdown file in the output directory.


### create_pylint_report( )

Creates a summary report for Pylint analysis using AI.

Args:
- report (str): The Pylint analysis report content.

Returns:
- str: The AI-generated summary of the Pylint report.

Side Effects:
    Writes the summary to a markdown file in the output directory.


### create_radon_cc_report( )

Creates a summary report for Radon CC analysis using AI.

Args:
- report (str): The Radon CC analysis report content.

Returns:
- str: The AI-generated summary of the Radon CC report.

Side Effects:
    Writes the summary to a markdown file in the output directory.


### create_radon_mi_report( )

Creates a summary report for Radon MI analysis using AI.

Args:
- report (str): The Radon MI analysis report content.

Returns:
- str: The AI-generated summary of the Radon MI report.

Side Effects:
    Writes the summary to a markdown file in the output directory.


### create_full_report( )

Creates a full summary report combining all analysis reports using AI.

Args:
- report (str): The combined content of all analysis reports.

Returns:
- str: The AI-generated full summary report.

Side Effects:
    Writes the summary to a markdown file in the output directory.


### create_report_with_openai( )

Generates analysis reports using OpenAI.

Side Effects:
    Processes each report file in the report directory and generates corresponding AI summaries.
    Writes the summaries to markdown files in the output directory.


### main( )

Main function to create analysis reports using OpenAI.

Side Effects:
    Checks the existence of the report directory and initiates the report generation process.
    Logs errors and information messages.


---

## Module create_docstrings.py
### create_docstrings( )

Creates docstrings for a given Python script using OpenAI's language model.

Args:
- script (str): The path to the Python script file.

Returns:
- str: The AI-generated script with added docstrings.

Side Effects:
    Writes the modified script with docstrings to the output directory.
    Logs the process of creating docstrings.

Raises:
- FileNotFoundError: If the script file does not exist.



### create_mdocs_report( )

Generates a summary report of the documentation using AI.

Args:
- documentation (str): The documentation content to summarize.

Returns:
- str: The AI-generated summary of the documentation.

Side Effects:
    Writes the summary to a file in the output directory.
    Logs the process of creating the summary.


### create_mdocs_onboarding( )

Creates an onboarding guide for new developers based on the documentation.

Args:
- documentation (str): The documentation content to use for the onboarding guide.

Returns:
- str: The AI-generated onboarding guide.

Side Effects:
    Writes the onboarding guide to a file in the output directory.
    Logs the process of creating the onboarding guide.


### process_mdocs( )

Processes the mdocs settings and generates the documentation file.

Side Effects:
    Writes the mdocs settings to a JSON file.
    Executes shell commands to generate and move the documentation file.
    Logs the process of generating the documentation.


### main( )

Main function to add docstrings to Python scripts in a codebase using OpenAI.

Side Effects:
    Logs the analysis process.
    Exits the program if the codebase directory does not exist.

Raises:
- SystemExit: If the codebase directory does not exist.



---

## Module ai.py
### create_connection( )

Establishes a connection to the OpenAI API using the specified model.

Args:
- model_name (str): The name of the OpenAI model to use. Defaults to "gpt-4o".

Returns:
- ChatOpenAI: An instance of the ChatOpenAI class configured with the specified model and API key.

Raises:
- None

Side Effects:
    None

Future Work:
    - Consider allowing more configuration options for the connection.


### run_chain( )

Executes a chain of runnables to process input data and generate an AI response.

Args:
- prompt (ChatPromptTemplate): The prompt template to use for generating the AI response.


- input_data (str): The input data to be processed by the chain.


- model_name (str): The name of the OpenAI model to use. Defaults to "gpt-4o".


- connection (ChatOpenAI, optional): An existing connection to the OpenAI API. If not provided, a new connection is created.

Returns:
- str: The response generated by the AI.

Raises:
- Exception: If there is an error during the chain execution.

Side Effects:
    - Logs an error message if the OpenAI API key is not found.
    - Exits the program if the API key is missing.

Future Work:
    - Implement error handling for specific exceptions during chain execution.
    - Consider adding more detailed logging for debugging purposes.


---

## Module refactor_java.py
### refactor( )

Refactors a given method using AI based on a provided prompt.

Args:
- method_code (str): The Java method code to be refactored.


- prompt_text (str): The prompt text to guide the AI refactoring.


- connection: The connection object for interacting with the AI model.

Returns:
- str: The refactored method code.

Raises:
- Exception: If the AI response is not in the expected format.



### remove_comments_from_code( )

Replaces comments in Java code with placeholders to prevent interference with code parsing.

Args:
- java_code (str): The Java code from which comments need to be removed.

Returns:
- tuple: A tuple containing the stripped code and a list of comments.



### restore_comments( )

Restores the original comments in the refactored code.

Args:
- refactored_code (str): The refactored Java code with placeholders.


- comments (list): The list of original comments.

Returns:
- str: The refactored code with comments restored.



### extract_and_refactor_methods( )

Extracts methods from a Java file, refactors them using AI, and restores comments.

Args:
- file_path (str): The path to the Java file to be refactored.


- prompt_text (str): The prompt text to guide the AI refactoring.


- connection: The connection object for interacting with the AI model.

Returns:
- str: The refactored Java code with comments restored.



### comment_placeholder( )
_No docstring available_

---

## Module create_readme.py
### create_readme( )

Generates or updates a README.md file based on the provided input using an AI model.

Args:
- input (str): The input text containing information extracted from the codebase.

Returns:
- str: The AI-generated README.md content.

Side Effects:
    - Writes the generated README.md content to the specified output file.
    - Logs the success or failure of the README.md creation.

Raises:
- - Logs an error if the AI response is empty.



### main( )

Main function to analyze the codebase and generate or update the README.md file.

Side Effects:
    - Logs the analysis process and any errors encountered.
    - Calls the create_readme function to generate the README.md content.


---

## Module commands.py
### run_command( )

Executes a shell command and writes its output to a specified file, while logging the process.

Args:
- command (str): The shell command to be executed.


- output_file (str): The path to the file where the command's output will be written.


- logger (logging.Logger): A logger instance used to log information, warnings, or errors.

Side Effects:
    - Writes the command output to the specified file.
    - Logs information, warnings, or errors based on the command execution result.

Raises:
- subprocess.CalledProcessError: Raised if the command execution fails.

Notes:
    - If the command fails with exit status 3, a warning is logged indicating an invalid argument.
    - If the command fails with exit status 30, a warning is logged indicating a timeout.
    - Other non-zero exit statuses result in an error being logged.
    - Future work could include handling additional specific exit codes or improving error handling.


---

## Module analyse_codebase.py
### analyze_with_vulture( )

Finds unused code using Vulture.

Side Effects:
    Generates a report on unused code and saves it to the output directory.
    Logs the process of running Vulture.


### analyze_with_pylint( )

Checks code quality with Pylint.

Side Effects:
    Generates a code quality report and saves it to the output directory.
    Logs the process of running Pylint.


### analyze_with_radon( )

Analyzes code complexity and maintainability using Radon.

Side Effects:
    Generates reports on cyclomatic complexity and maintainability index.
    Saves the reports to the output directory.
    Logs the process of running Radon.


### main( )

Main function to run all analysis tools.

Side Effects:
    Checks the existence of the codebase directory.
    Runs Vulture, Pylint, and Radon analyses.
    Logs the overall process and results of the analysis.
    Exits the program if the codebase directory does not exist.


---

