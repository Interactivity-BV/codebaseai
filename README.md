# Python Codebase Analyzer

This project is a Python script that analyzes a Python codebase for unused code, linting issues, and complexity metrics. It also processes the output with a large language model (ChatGPT 4o only for now). The analysis tools used include `vulture`, `pylint`, and `radon`.

## Disclaimer

The code has only be tested on relatively small projects. It might be that the reports are too long for the context memory of the LLM. Also keep in mind that for large codebases the costs of using the OpenAI API might be significant. Use at your own risk! 
At a later stage large reports will be processed in chunks using the langchain modules. 

## Features

- **Vulture:** Detects unused code, variables, and imports.
- **Pylint:** Checks code quality and provides linting feedback.
- **Radon:** Analyzes cyclomatic complexity and maintainability index.
- **LLM Integration:** Outputs are processed with LangChain to gain additional insights and recommendations.
- **Documentation generation:** Add docstrings to the Python files and process them with `mdocs`. Documentation is created with a summary of the module and an onboarding file for new developers.

## Prerequisites

- Python 3.7 or higher
- Git (for cloning the repository)

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
   pip install vulture pylint radon langchain langchain_openai langchain_core mdocs
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

## Creating the basic reports

The `analyze_codebase.py` runs the Python code analytics tools and creates report files for each of the tools.

1. Run the script:
   ```bash
   python analyze_codebase.py -c ~/git/my_project -o ~/reports -l ~/reports/log.txt
   ```

2. View the generated reports in the `analysis_reports` directory:
   - `vulture_report.txt`: Lists unused code.
   - `pylint_report.txt`: Provides linting issues and code quality feedback.
   - `radon_cc_report.txt`: Shows cyclomatic complexity.
   - `radon_mi_report.txt`: Shows maintainability index.

## Running ChatGPT on reports

The `create_reports.py` processes the reports by asking ChatGPT for summary information, suggestions to fix the code and specific insights. It will also use the detailed reports from each of the tools to generate a global project evaluation.

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

## Example output

Please check the `example_reports` for the reporting done on this project.

## Documentation generation

The `create_docstrings.py` script adds docstrings to all Python scripts. It will then run `mdocs` on the codebase and process the resulting documentation with the LLM to produce a summary report and an onboarding file. 

Please be aware:
  - When using the module directory for both input and output, Python files will be overwritten. Make sure you have committed all you changes before doing this.
  - The codebase needs to be a module: it should contain a `__init__.py` file
  - The script creates a `docs` directory in the output directory.

```bash
cd ..
python codebase/create_docstrings.py -o . -c codebase -t "AI-documentation support" -m "Module to analyse Python repositories using standard tools and AI" -u "https://github.com/Interactivity-BV/codebaseai" -d "Interactivity" -e "info@interactivity.nl"
```

## Contribution

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
