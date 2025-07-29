import re
import logging
import langchain_core.prompts as prompts

logger = logging.getLogger(__name__)

COMMENT_PATTERN = re.compile(r'/\*[\s\S]*?\*/|[^:]//[^\n]*')


def refactor(method_code, prompt_text, connection, run_chain, model_name):
    """
    Refactors a given method using AI based on a provided prompt.

    Args:
        method_code (str): The Java method code to be refactored.
        prompt_text (str): The prompt text to guide the AI refactoring.
        connection: The connection object for interacting with the AI model.

    Returns:
        str: The refactored method code.

    Raises:
        Exception: If the AI response is not in the expected format.
    """
    prompt = prompts.ChatPromptTemplate.from_template(prompt_text + """
                                                          
        Method: 
        `{input}`
        """
                                              )
    ai_response = run_chain(prompt, method_code, model_name=model_name, connection=connection)
    if ai_response.startswith("```"):
        ai_response = ai_response[7:].strip()
        ai_response = ai_response.rsplit("```", 1)[0].strip()
    return ai_response

def remove_comments_from_code(java_code):
    """
    Replaces comments in Java code with placeholders to prevent interference with code parsing.

    Args:
        java_code (str): The Java code from which comments need to be removed.

    Returns:
        tuple: A tuple containing the stripped code and a list of comments.
    """
    comments = []

    def comment_placeholder(match):
        comments.append(match.group())  # Store comment
        return f'/*COMMENT{len(comments)-1}*/'  # Replace with placeholder

    stripped_code = re.sub(COMMENT_PATTERN, comment_placeholder, java_code)
    return stripped_code, comments

def restore_comments(refactored_code, comments):
    """
    Restores the original comments in the refactored code.

    Args:
        refactored_code (str): The refactored Java code with placeholders.
        comments (list): The list of original comments.

    Returns:
        str: The refactored code with comments restored.
    """
    for i, comment in enumerate(comments):
        refactored_code = refactored_code.replace(f'/*COMMENT{i}*/', comment, 1)
    return refactored_code

def extract_and_refactor_methods(file_path, prompt_text, connection, run_chain, model_name):
    """
    Extracts methods from a Java file, refactors them using AI, and restores comments.

    Args:
        file_path (str): The path to the Java file to be refactored.
        prompt_text (str): The prompt text to guide the AI refactoring.
        connection: The connection object for interacting with the AI model.

    Returns:
        str: The refactored Java code with comments restored.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        java_code = f.read()

    # Step 1: Remove comments temporarily to avoid `{}` inside comments affecting extraction
    java_code = java_code.replace("//", " // ")  # Ensure `//` comments are separated by spaces
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
                        refactored_method = refactor(method_body, prompt_text, connection, run_chain, model_name)
                        method_bodies[method_body] = refactored_method
                        break

    # Step 4: Replace old methods with refactored versions in the modified code
    for old_method, new_method in method_bodies.items():
        refactored_code = refactored_code.replace(old_method, new_method)

    # Step 5: Restore original comments before writing back the file
    refactored_code = restore_comments(refactored_code, comments)
    return refactored_code