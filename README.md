# Python Codebase Analyzer

This project is a Python script that analyzes a Python codebase for unused code, linting issues, and complexity metrics. It also processes the output with a large language model. The analysis tools used include `vulture`, `pylint`, and `radon`. It also enables you to create docstrings on all your Python files and generate documentation based on these docstrings.

## Disclaimer

The code has only been tested on relatively small projects. It might be that the reports are too long for the context memory of the LLM. Also, keep in mind that for large codebases, the costs of using the OpenAI API might be significant. Use at your own risk! At a later stage, large reports will be processed in chunks using the langchain modules.

## Features

- **Vulture:** Detects unused code, variables, and imports.
- **Pylint:** Checks code quality and provides linting feedback.
- **Radon:** Analyzes cyclomatic complexity and maintainability index.
- **LLM Integration:** Outputs are processed with LangChain to gain additional insights and recommendations.
- **Documentation generation:** Add docstrings to the Python files and process them with `mdocs`. Documentation is created with a summary of the module and an onboarding file for new developers.

## Prerequisites

- Python 3.7 or higher
- Git (for cloning the repository)
- An [OpenAI API key](https://www.openai.com) and a model to use. **Tip**: use a model with a large context window, for example, gpt-4o, to fit large files.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Interactivity-BV/codebaseai
   cd codebaseai
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

   or

   ```bash
   pip install vulture pylint radon langchain langchain_openai langchain_core mdocs python-dotenv
   ```

4. Verify installation:
   - Check `vulture` version:
     ```bash
     vulture --version
     ```
   - Check `pylint` version:
     ```bash
     pylint --version
     ```
   - Check `radon` version:
     ```bash
     radon --version
     ```

5. Create the `.env` file and place your `OPENAI_API_KEY` in that file.

## Creating the Basic Reports

The `analyse_codebase.py` runs the Python code analytics tools and creates report files for each of the tools.

1. Run the script:
   ```bash
   python analyse_codebase.py -c ~/git/my_project -o ~/reports -l ~/reports/log.txt
   ```

2. View the generated reports in the `analysis_reports` directory:
   - `vulture_report.txt`: Lists unused code.
   - `pylint_report.txt`: Provides linting issues and code quality feedback.
   - `radon_cc_report.txt`: Shows cyclomatic complexity.
   - `radon_mi_report.txt`: Shows maintainability index.

## Running ChatGPT on Reports

The `create_reports.py` processes the reports by asking ChatGPT for summary information, suggestions to fix the code, and specific insights. It will also use the detailed reports from each of the tools to generate a global project evaluation.

1. Run the script:
   ```bash
   python create_reports.py -r ~/reports -o ~/reports -l ~/reports/log.txt
   ```

2. View the generated reports in the `analysis_reports` directory:
   - `vulture_report_summary_ai.md`: Reporting on unused code.
   - `pylint_report_summary_ai.md`: Reporting on linting issues and code quality feedback.
   - `radon_cc_report_summary_ai.md`: Reporting on cyclomatic complexity.
   - `radon_mi_report_summary_ai.md`: Reporting on maintainability index.
   - `full_analysis_summary_ai.md`: Reporting on the entire codebase.

## Example Output

Please check the `example_reports` for the reporting done on this project.

## Documentation Generation

The `create_docstrings.py` script adds docstrings to all Python scripts. It will then run `mdocs` on the codebase and process the resulting documentation with the LLM to produce a summary report and an onboarding file.

Please be aware:
  - When using the module directory for both input and output, Python files will be overwritten. Make sure you have committed all your changes before doing this.
  - The codebase needs to be a module: it should contain a `__init__.py` file.
  - The script creates a `docs` directory in the output directory.

```bash
cd ..
python codebase/create_docstrings.py -o . -c codebase -t "AI-documentation support" -D "Module to analyse Python repositories using standard tools and AI" -u "https://github.com/Interactivity-BV/codebaseai" -d "Interactivity" -e "info@interactivity.nl"
```

## Create or update README.md

The `create_readme.py` processes Python main files, markdown files and the requirements.txt to create or update the [README.md](README.md):

```bash
python codebase/create_readme.py -t "Title of the repository" -o codebase/README.md -c codebase
```

## Java-code refactoring

The `refactor_java.py` extracts Java-methods from Java files and refactors them using the prompt in `refactoring_prompt.txt`. You can change the prompt
based on the type of refactoring you need, for example because an API changed or methods used are depricated. 
The example prompt provides the instructions to rewrite methods using the Neo4J API 3.5 to the Neo4J API 5.5, which has different ways of handling 
transactions.

It is not a silver bullet, but it will save you a lot of time doing silly stuff. However:

- The refactoring is done on methods. Hence any imports etc will not be fixed
- Each method is processed separately: any higher-level refactoring will not be taken into account 

```bash
python3 codebase/refactor_java.py -j ~/git/my_java_app -o refactered_my_java_app -p codebase/refactoring_prompt.txt
```

## Contribution

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Additional Resources

- [Documentation Summary](docs/documentation_summary_ai.md)
- [Onboarding Guide](docs/documentation_onboarding_ai.md)
- [Full Analysis Summary](example_reports/full_analysis_summary_ai.md)

This README provides a comprehensive overview of the project, its features, and how to get started. For more detailed information, refer to the documentation files linked above.