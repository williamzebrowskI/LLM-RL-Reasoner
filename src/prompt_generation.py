from .parsing import parse_options
from .utils import escape_special_characters
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
        options (list): List of option strings (e.g., ['A) $60.00', 'B) $35.42', ...]).
        correct_label (str): Correct answer label (e.g., 'A').
        
    Returns:
        str: The correct answer text (e.g., '$60.00') or None if not found.
    """
    for opt in options:
        if opt.startswith(f"{correct_label})"):
            return opt.split(')', 1)[1].strip()
    print(f"Warning: Correct answer label '{correct_label}' not found in options.")
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