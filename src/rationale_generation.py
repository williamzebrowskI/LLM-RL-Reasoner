import re
import ollama

qwen = "qwen2.5:7b"
llama = "llama3.1:8b"
llama_ft = "llama-reason-04:latest"
llama_ft_v5 = "llama-reason-05:latest"

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
        response = ollama.chat(model=llama_ft, messages=[
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


def eval_rationale(correct_answer_text, extracted_answer):

    response = ollama.chat(model=llama, messages=[
            {
                'role': 'user',
                'content':
                f"""
                    You are a evaltiona assistant is to compare two numerical answers and determine if they are the same answer, ignoring differences in units or formatting.\n\n
                    Comparison Rules:\n\n
                    - If the answers are the same, for example, First Answer: '90' and Second Answer: '90 m' or ( km, %, sec, ml, etc) this is a correct match since numerically the same and return 'correct' in your response.\n
                    - If the answers are different, consider them NOT a match and return 'incorrect' in your response.\n\n
                    Ignore differences in formatting, such as trailing zeros.\n\n

                    Compare the Following Answers:\n
                    First answer: {extracted_answer}\n
                    Second answer: {correct_answer_text}\n\n
                    Respond with:\n
                    "correct" if the two answers are the same\n
                    "incorrect" if the two answers are not the same\n\n
                    Please respond with only one of the above options, without any explanations.
                """
            },
     ])


    decision = response['message']['content'].strip()

    return decision