import re
import ollama

qwen = "qwen2.5:7b"
llama = "llama3.1:8b"
llama2 = "llama3.2:3b"

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
        "---\n"
        "The examples above are how you should answer and explain the answer to the question you are given.\n"
        "Follow the instructions below in this task:\n"
        "1. Solve the following problem step-by-step.\n"
        "2. Provide a detailed explanation that justifies the correct answer.\n"
        "3. Do not reference any options or external information.\n"
        "4. You MUST end your response with your answer in the format \"Answer: [full answer]\".\n"
        "---\n\n"
        f"Question: {question}\n\n"
        "Answer Explanation:\n"
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