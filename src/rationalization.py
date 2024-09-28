# mypackage/rationalization.py
import ollama
from .utils import is_rationale_correct

def rationalize(question, correct_answer, prompt_set):
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

    # Construct the input prompt with explicit instructions
    input_text = (
        f"{prompt_set}\n\n"
        "With the provided examples above, provide a detailed explanation for the following question, ensuring that the explanation clearly justifies why the correct answer is chosen.\n"
        "Ensure that you end your response with your concise answer in the format \"Answer: [answer]\". \n\n"
        f"Question: {question}\n"
        f"Correct Answer: {correct_answer}\n\n"
        "Explanation:"
    )

    try:
        # Use Ollama (or your LLM) to get the response
        response = ollama.chat(model="llama3.1:8b", messages=[
            {
                'role': 'user',
                'content': input_text,
            },
        ])

        # Extract the generated rationale
        generated_rationale = response['message']['content'].strip()

        return generated_rationale

    except Exception as e:
        print(f"Error during rationalization: {e}")
        return ''