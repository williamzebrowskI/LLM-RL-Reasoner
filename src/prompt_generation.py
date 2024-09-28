from .parsing import parse_options
from .utils import escape_special_characters
import ollama
import re

def create_prompt_examples(ds_train, num_examples):
    prompt_examples = []
    for i in range(num_examples):
        example = ds_train[i]
        question = example['question']
        rationale = example['rationale']
        correct_option = example['correct'].strip().upper()
        
        example_response = (
            "Question: {}\n"
            "Answer Explanation: {}\n"
            "Answer: {}\n"
            "###\n"
        ).format(
            question,
            rationale,
            correct_option
        )
        
        prompt_examples.append({
            'question': question,
            'rationale': rationale,
            'answer': correct_option
        })
    return prompt_examples


def clean_options(options):
    """
    Cleans the options by removing redundant labels and extracting meaningful answer texts.
    
    Args:
        options (list): List of option strings.
        
    Returns:
        list: Cleaned list of option strings.
    """
    cleaned = []
    for opt in options:
        # Split on ')', keep all parts after the first split
        parts = opt.split(')')
        if len(parts) >= 2:
            letter = parts[0].strip().upper()
            # Rejoin the rest in case there are multiple ')'
            text = ')'.join(parts[1:]).strip()
            # Handle cases where the text starts with another label like 'A)' or 'I)'
            inner_match = re.match(r'^([A-EI]+)\)\s*(.*)', text)
            if inner_match:
                # If text starts with labels like 'I)', remove them
                text = inner_match.group(2).strip()
            cleaned.append(f"{letter}) {text}")
        else:
            # Handle unexpected formats
            print(f"Warning: Unable to clean option '{opt}'. Keeping it as is.")
            cleaned.append(opt)
    return cleaned


def escape_special_characters(text):
    """
    Escapes special characters in the text to prevent formatting issues.
    
    Args:
        text (str): The input text.
    
    Returns:
        str: The escaped text.
    """
    # Example implementation, adjust based on actual needs
    escape_chars = {
        "\\": "\\\\",
        "\n": "\\n",
        "\t": "\\t",
        "\"": "\\\"",
    }
    for char, esc_char in escape_chars.items():
        text = text.replace(char, esc_char)
    return text

def get_correct_answer_text(options, correct_label):
    """
    Retrieves the answer text corresponding to the correct label.
    
    Args:
        options (list): List of option strings (e.g., ['A) 12', 'B) 6', ...]).
        correct_label (str): Correct answer label (e.g., 'A').
        
    Returns:
        str: The correct answer text (e.g., '12') or None if not found.
    """
    pattern = re.compile(rf'^{re.escape(correct_label.upper())}\)\s*(.*)$')
    
    for opt in options:
        match = pattern.match(opt.strip())
        if match:
            return match.group(1).strip()
    
    print(f"Warning: Correct answer label '{correct_label}' not found in options.")
    return None

def extract_answer_text(rationale):
    """
    Extracts the answer text from the rationale using regex.
    
    Args:
        rationale (str): Generated rationale string.
    
    Returns:
        str or None: Extracted answer text if found, else None.
    """
    # Attempt to extract the answer text after 'Answer:'
    match = re.search(r'Answer:\s*(.+)', rationale, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def create_prompt_set(ds_train, num_examples):
    """
    Creates a prompt set string from the training dataset without including options.
    
    Args:
        ds_train (list): List of training examples, each as a dictionary with keys 'question', 'options', 'rationale', and 'correct'.
        num_examples (int): Number of examples to include in the prompt set.
    
    Returns:
        str: Formatted prompt set string without options.
    """
    prompt_set = ""
    for i in range(num_examples):
        example = ds_train[i]
        question = example['question']
        raw_options = example['options']
        rationale = escape_special_characters(example['rationale'])
        correct_label = example['correct'].strip().upper()
        
        # Clean the options
        cleaned_options = clean_options(raw_options)
        
        # Get the correct answer text
        correct_answer_text = get_correct_answer_text(cleaned_options, correct_label)
        
        if correct_answer_text is None:
            print(f"Skipping example {i} due to missing correct answer.")
            continue  # Skip examples without a valid correct answer
        
        # Add the 'correct_answer_text' to the example for later use
        example['correct_answer_text'] = correct_answer_text
        
        # Build the prompt set string without options
        prompt_set += (
            "Question: {}\n"
            "Answer Explanation: {}\n"
            "Answer: {}\n"
            "###\n"
        ).format(
            question,
            rationale,
            correct_answer_text
        )
    return prompt_set

def eval_answer_prompt(correct_answer, extracted_answer):

    eval_response = ollama.chat(model="llama3.1:8b", messages=[
            {
                'role': 'user',
                'content':
                f"""
                    Your task is to compare two numerical answers and determine if they are the same answer, ignoring differences in units or formatting.\n\n
                    Comparison Rules:\n\n
                    - If the answers are the same, for example, First Answer: '90' and Second Answer: '90 miles' or ( km, %, sec, ml, etc) this is a match and return 'correct' in your response.\n
                    - If the answers are different, consider them NOT a match and return 'incorrect' in your response.\n\n
                    Ignore differences in formatting, such as trailing zeros.\n\n

                    Compare the Following Answers:\n
                    First answer: {correct_answer}\n
                    Second answer: {extracted_answer}\n\n
                    Respond with:\n
                    "correct" if the two answers are the same\n
                    "incorrect" if the two answers are not the same\n\n
                    Please respond with only one of the above options, without any explanations.
                """
            },
     ])
    
    decision = eval_response['message']['content'].strip()
    return decision

