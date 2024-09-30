# mypackage/rationalization.py
import ollama
from .utils import is_rationale_correct

llama_ft = "llama-reason-04:latest"

prompt_set = """
Example 1:\n\n
Question: Two friends plan to walk along a 43-km trail, starting at opposite ends of the trail at the same time. If Friend P's rate is 15% faster than Friend Q's, how many kilometers will Friend P have walked when they pass each other?\n
Answer Explanation: Let Friend Q's speed be x km/h. Then Friend P's speed is 1.15x km/h. Since they start at the same time and meet after t hours, the total distance covered is:\n
x * t + 1.15x * t = 43\n
2.15x * t = 43\n
t = 43 / 2.15 ≈ 20 hours\n
Friend P walked 1.15x * t = 1.15 * 20 = 23 km.\n
Thus, the answer is 23 km.\n
Answer: 23 km\n\n

Example 2: \n\n
Question: In the coordinate plane, points (x, 1) and (5, y) are on line k. If line k passes through the origin and has slope 1/5, then what are the values of x and y respectively?\n
Answer Explanation: The equation of line k is y = (1/5)x. Substituting (x, 1):\n
1 = (1/5)x → x = 5\n
Substituting (5, y):\n
y = (1/5)*5 → y = 1\n
Thus, the answer is, x = 5 and y = 1.  5 and 1\n
Answer: x = 5 and y = 1
"""

def rationalize(question, correct_answer):
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

    rationalization_prompt = (
        f"{prompt_set}\n\n"
        "The examples above demonstrate how you should output your response.\n"
        "Please follow the instructions below for this task:\n"
        "1. Provide a concise step-by-step explanation for the following question, ensuring that the reasoning naturally leads to an answer.\n"
        "2. You are forbidden to reference or imply that a correct answer or hint was provided in advance.\n"
        "3. Perform your calculations and reasoning based solely on the information given in the question.\n"
        "6. After your explanation and any necessary corrections, you MUST end your response with 'Answer: [final answer]' in a similar format as the examples above.\n\n"
        f"Question: {question}\n"
        f"Hint: The correct answer is {correct_answer}\n"
        "Answer Explanation: \n"
        "Answer: "
    )

    try:
        # Use Ollama (or your LLM) to get the response
        response = ollama.chat(model=llama_ft, messages=[
            {
                'role': 'user',
                'content': rationalization_prompt,
            },
        ])

        # Extract the generated rationale
        generated_rationale = response['message']['content'].strip()

        return generated_rationale

    except Exception as e:
        print(f"Error during rationalization: {e}")
        return ''