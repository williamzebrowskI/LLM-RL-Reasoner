# mypackage/rationalization.py
import ollama
from .utils import is_rationale_correct

def rationalize(question, options, correct_answer, prompt_set, model="llama3.1:8b"):
    """
    Generates a correct rationale for a question given the correct answer.

    Parameters:
        question (str): The question to be answered.
        options (dict): A dictionary mapping option letters to option texts.
        correct_answer (str): The correct answer text.
        prompt_set (str): The initial prompt set containing examples.

    Returns:
        str: The generated rationale.
    """
    # Prepare the options text
    options_text = '\n'.join([f"{key}: {value}" for key, value in options.items()])

    # Construct the input prompt with explicit instructions
    input_text = (
        prompt_set
        + "\n\n"
        + "Provide a detailed explanation for the following question, ensuring that the explanation clearly justifies why the correct answer is chosen.\n"
        + f"Question: {question}\n"
        + "Options:\n"
        + options_text + "\n"
        + f"Correct Answer: {correct_answer}\n"
        + "Explanation:"
    )

    try:
        # Use Ollama (or your LLM) to get the response
        response = ollama.chat(model=model, messages=[
            {
                'role': 'user',
                'content': input_text,
            },
        ])

        # Extract the generated rationale
        generated_rationale_full = response['message']['content'].strip()

        # Assign the entire response as the rationale
        generated_rationale = generated_rationale_full

        # Optionally, verify the rationale's correctness
        if is_rationale_correct(generated_rationale, correct_answer, question):
            return generated_rationale
        else:
            print(f"Generated rationale does not sufficiently explain the correct answer for question: {question}")
            return ''

    except Exception as e:
        print(f"Error during rationalization: {e}")
        return ''