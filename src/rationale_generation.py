import re
import ollama

qwen = "qwen2.5:7b"
llama = "llama3.1:8b"

def generate_rationale_and_answer(question, prompt_set, model=llama):
    """
    Generates a rationale and answer for a given question using the language model.

    Args:
        question (str): The question text.
        prompt_set (str): The prompt set to guide the model.

    Returns:
        str: Generated rationale and answer.
    """
    prompt = (
        f"{prompt_set}\n\n"
        "Please solve the following problem in a step-by-step process and provide a detailed explanation. "
        "Do not reference any options or external information. "
        "Ensure that you end your response with your answer in the format \"Answer: [text]\".\n\n"
        f"Question: {question}\n"
        "\nAnswer Explanation:"
    )

    
    try:
        response = ollama.chat(model=model, messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        
        generated_rationale = response['message']['content'].strip()
        
    except Exception as e:
        print(f"Error generating rationale: {e}")
        generated_rationale = ''
    
    return generated_rationale