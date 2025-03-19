import re
import sys
import logging
import argparse 
import os
from ai import run_chain
from commands import run_command
from langchain_core.prompts import ChatPromptTemplate

# Parse command line arguments
parser = argparse.ArgumentParser(description="Refactor Java code using AI.")
parser.add_argument("-j", "--java_dir", required=True, help="The Java package(s) directory to refactor.")
parser.add_argument("-o", "--output_dir", required=True, help="The directory to store the refactored source code.")
parser.add_argument("-l", "--log_file", default='./analysis.log', help="The file to save the log.")
parser.add_argument("-m", "--model_name", default="gpt-4o", help="OpenAI model name.")
parser.add_argument("-p", "--prompt", default="./refactoring_prompt.txt", help="The refactor prompt")  
args = parser.parse_args()

# Configure logging
logging.basicConfig(
    filename=args.log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a logger object
logger = logging.getLogger(__name__)


SRC_DIR = args.java_dir
if not os.path.exists(SRC_DIR):
    logger.error(f"Error: Directory {SRC_DIR} does not exist.")
    sys.exit(1)

if not SRC_DIR.endswith('/'):
    SRC_DIR += '/'
OUTPUT_DIR = args.output_dir
if not OUTPUT_DIR.endswith('/'):
    OUTPUT_DIR += '/'

MODEL_NAME = args.model_name

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def refactor(method_code, prompt_text):
    prompt = ChatPromptTemplate.from_template(prompt_text + """
                                                          
        Method: 
        `{input}`
        """
    )
    logger.debug("----METHOD CODE----")
    logger.debug(method_code)
    logger.debug("----/METHOD CODE/----") 
    ai_response = run_chain(prompt, method_code, model_name=MODEL_NAME)
    if ai_response.startswith("```"):
        ai_response = ai_response[7:].strip()
        ai_response = ai_response.rsplit("```", 1)[0].strip()
    logger.debug("----AI RESPONSE----")
    logger.debug(ai_response)  
    logger.debug("----/AI RESPONSE/----")
    return ai_response

def remove_comments_from_code(java_code):
    """Replaces comments with placeholders so they don't interfere with `{` and `}` counting."""
    comment_pattern = re.compile(r'/\*[\s\S]*?\*/|[^:}]//[^\n]*')
    comments = []
    
    def comment_placeholder(match):
        comments.append(match.group())  # Store comment
        return f'/*COMMENT{len(comments)-1}*/'  # Replace with placeholder
    
    stripped_code = re.sub(comment_pattern, comment_placeholder, java_code)
    return stripped_code, comments

def restore_comments(refactored_code, comments):
    """Restores the original comments after refactoring."""
    for i, comment in enumerate(comments):
        refactored_code = refactored_code.replace(f'/*COMMENT{i}*/', comment, 1)
    return refactored_code

def extract_and_refactor_methods(file_path, prompt_text):
    with open(file_path, 'r', encoding='utf-8') as f:
        java_code = f.read()


    # Step 1: Remove comments temporarily to avoid `{}` inside comments affecting extraction
    stripped_code, comments = remove_comments_from_code(java_code)

    # Step 2: Updated regex to correctly handle return types, generics (`<>`), and exclude control statements
    method_signature_pattern = re.compile(
        r'^\s*'  # Start of line with optional spaces
        r'(?:(?:public|private|protected|static|final|synchronized|abstract|native|transient)\s+)*'  # Modifiers
        r'(?!if|else|while|for|switch|catch|return|new|case)\s*'  # Ensure it's not a control structure
        r'[a-zA-Z_][\w<>\[\],\s]*'  # Return type (supports `<>` generics)
        r'\s+(\w+)\s*'  # Method name
        r'\(\s*[^()]*\s*\)'  # Parameters (ensures balanced parentheses)
        r'(?:\s*throws\s+[\w<>\[\],. ]+)?'  # Optional "throws" clause
        r'\s*\{',  # Ensure it directly follows `{`
        re.MULTILINE
    )
    
    method_positions = [m.start() for m in method_signature_pattern.finditer(stripped_code)]
    refactored_code = stripped_code  # Preserve original file structure
    method_bodies = {}

    # Step 3: Extract and refactor methods using a stack-based approach
    for start in method_positions:
        brace_count = 0
        inside_string = False
        for i in range(start, len(stripped_code)):
            char = stripped_code[i]

            # Toggle inside_string when encountering an unescaped quote (`"`)
            if char == '"' and (i == 0 or stripped_code[i-1] != '\\'):
                inside_string = not inside_string

            if not inside_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        method_body = stripped_code[start:i + 1]
                        refactored_method = refactor(method_body, prompt_text)
                        method_bodies[method_body] = refactored_method
                        break


    # Step 4: Replace old methods with refactored versions in the modified code
    for old_method, new_method in method_bodies.items():
        refactored_code = refactored_code.replace(old_method, new_method)

    # Step 5: Restore original comments before writing back the file
    refactored_code = restore_comments(refactored_code, comments)
    return refactored_code


if __name__ == "__main__":
    with open(args.prompt, 'r', encoding='utf-8') as prompt_file:
        prompt_text = prompt_file.read()
    for root, dirs, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                cleaned_path = re.sub(r"^(\.\./|\.\/)+", "", file_path)
                if cleaned_path.startswith("/"):
                    cleaned_path = cleaned_path[1:] 
                    logger.warning(f"Input path is absolute. Removing leading slash: {cleaned_path}")
                output_file_path = os.path.join(OUTPUT_DIR, cleaned_path)

                if os.path.exists(output_file_path) and os.path.getmtime(file_path) < os.path.getmtime(output_file_path):
                    logger.info(f"Skipping {file_path} as it is not newer than the existing output.")
                else:
                    logger.info(f"Refactoring {file_path}.")
                    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                    refactored_code = extract_and_refactor_methods(file_path, prompt_text)
                    with open(output_file_path, "w") as output_file:
                        output_file.write(refactored_code)
                        logger.info(f"Refactored code written to: {output_file_path}")
                    run_command(f"astyle -n --style=java {output_file_path}", None, logger)
    logger.info("Refactoring completed.")       






