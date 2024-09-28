import json
import re
import os

def push_incorrect_pairs(incorrect_pairs, file_path='data/incorrect_pairs.json'):
    """
    Pushes new incorrect pairs into a JSON file. If the file does not exist, it creates one.
    
    Args:
        new_pairs (list): A list of dictionaries containing incorrect pairs.
        file_path (str): The path to the JSON file. Defaults to 'incorrect_pairs.json'.
        
    Example:
        new_incorrect = [
            {
                'question': 'Sample question?',
                'rationale': 'Sample rationale.',
                'answer': 'Incorrect answer',
                'correct_answer': 'Correct answer'
            },
            # Add more pairs as needed
        ]
        push_incorrect_pairs(new_incorrect)
    """
    # Check if the file exists
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if not isinstance(data, list):
                    print(f"Warning: {file_path} does not contain a list. Overwriting with a new list.")
                    data = []
        except json.JSONDecodeError:
            print(f"Warning: {file_path} is not a valid JSON file. Overwriting with a new list.")
            data = []
    else:
        # If the file doesn't exist, start with an empty list
        data = []
    
    # Append new incorrect pairs
    data.extend(incorrect_pairs)
    
    # Write back to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    print(f"Successfully added {len(incorrect_pairs)} incorrect pair(s) to '{file_path}'.")



def convert_correct_pairs_to_conversations(correct_pairs):
    """
    Converts a list of correct_pairs to the new conversation format.
    
    Args:
        correct_pairs (list): List of dictionaries with keys 'question', 'rationale', and 'answer'.
    
    Returns:
        list: List of dictionaries in the format {"text": "Q: ...\nA: ..."}
    """
    new_conversations = []
    for pair in correct_pairs:
        question = pair.get('question', '').strip()
        rationale = pair.get('rationale', '').strip()
        
        if not question or not rationale:
            print(f"Warning: Missing question or rationale in pair: {pair}. Skipping.")
            continue
        
        # Remove any trailing "Answer: ..." lines from the rationale
        # This ensures that the rationale does not contain explicit "Answer:" labels
        rationale_cleaned = re.sub(r'\n*Answer:\s*.*$', '', rationale, flags=re.IGNORECASE).strip()
        
        # Additionally, remove any "Rationale:" labels if present
        rationale_cleaned = re.sub(r'^Rationale:\s*', '', rationale_cleaned, flags=re.IGNORECASE).strip()
        
        # Create the new conversation format
        convo = {
            "text": f"Q: {question}\nA: {rationale_cleaned}"
        }
        new_conversations.append(convo)
    return new_conversations


def append_conversations_to_jsonl(conversations, file_path='finetuning_data.jsonl'):
    """
    Appends a list of conversations to an existing JSONL file in the desired format.
    
    Each conversation is a dict with 'text': 'Q: ...\nA: ...'
    This function ensures that any residual 'Answer:' labels are removed from the 'A: ...' section.
    
    Args:
        conversations (list): List of conversations to append, each as {"text": "Q: ...\nA: ..."}.
        file_path (str): Path to the existing JSONL file.
    
    Returns:
        None
    """
    # Check if the file exists
    if os.path.exists(file_path):
        # Check if the file ends with a newline
        with open(file_path, 'rb') as f:
            try:
                f.seek(-1, os.SEEK_END)
                last_char = f.read(1)
                if last_char != b'\n':
                    newline_needed = True
                else:
                    newline_needed = False
            except OSError:
                # File is empty
                newline_needed = False
    else:
        # File does not exist; will be created
        newline_needed = False

    with open(file_path, 'a', encoding='utf-8') as f:
        # If a newline is needed before appending, add it
        if newline_needed:
            f.write('\n')
        
        for convo in conversations:
            text = convo.get('text', '').strip()
            
            # Ensure that the text starts with "Q: " and contains "A: "
            if not text.startswith("Q: ") or "\nA: " not in text:
                print(f"Warning: Conversation does not follow the 'Q: ...\nA: ...' format. Skipping: {convo}")
                continue
            
            # Split the text into Question and Answer parts
            try:
                q_part, a_part = text.split("\nA: ", 1)
            except ValueError:
                print(f"Warning: Unable to split 'Q' and 'A' parts. Skipping: {convo}")
                continue
            
            # Clean the Answer part by removing any "Answer:" labels if present
            # Although it should already be cleaned, this is an extra safeguard
            a_part_cleaned = re.sub(r'\n*Answer:\s*.*$', '', a_part, flags=re.IGNORECASE).strip()
            a_part_cleaned = re.sub(r'^Answer:\s*', '', a_part_cleaned, flags=re.IGNORECASE).strip()
            
            # Reconstruct the cleaned conversation text
            new_text = f"{q_part}\nA: {a_part_cleaned}"
            
            # Append the cleaned conversation to the list
            processed_convo = {"text": new_text}
            
            # Serialize and write to the file
            json_line = json.dumps(processed_convo, ensure_ascii=False)
            f.write(json_line + '\n')
    
    print(f"Successfully appended {len(conversations)} conversations to '{file_path}'.")