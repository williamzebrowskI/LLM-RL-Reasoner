# mypackage/rationalization.py
import ollama
from .utils import is_rationale_correct

llama_ft = "llama-reason-04:latest"
llama_v5 = "llama-reason-05:latest"

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

    # prompt = (
    #     "You are a reasoning assistant that provides clear, step-by-step explanations to arrive at a final calculated answer.\n"
    #     "\n"
    #     "Instructions:\n"
    #     "1. To understand what is being asked, you must break the question down.\n"
    #     "2. Walk through the problem step by step to formulate an calculated answer.\n"
    #     "3. You will be given a hint to guide your reasoning steps only.\n"
    #     f"Question: {question}\n\n"
    #     "Respond with:\n"
    #     "Your step by step reasoning\n"
    #     "Your final answer, 'Answer: '\n\n"
    #     "About the Hint:\n"
    #     "1. Never reveal you were given a hint in your response.\n"
    #     "2. Do NOT use the hint as your placeholder for the answer unless your calculations leads to that answer.\n"
    #     "3. Your final step-by-step calculated answer must match the hint."
    #     f"Here is the hint, {correct_answer}"
    # )
    # prompt = (
    #     "You are a reasoning assistant that provides clear, step-by-step explanations to arrive at a final calculated answer.\n\n"
    #     "Instructions:\n"
    #     "1. Break down the question to understand what is being asked.\n"
    #     "2. Provide a logical, step-by-step reasoning to reach the calculated answer.\n"
    #     "3. Use the hint provided to guide your reasoning steps, but do not mention the hint in your response.\n"
    #     "4. Ensure your final calculated answer matches the hint.\n\n"
    #     f"Question:\n{question}\n\n"
    #     "Respond with:\n"
    #     "- Your step-by-step reasoning.\n"
    #     "- Your final answer, MUST be formatted as 'Answer: __ '\n\n"
    #     f"Hint: {correct_answer}\n"
    #     "1. Never reveal you were given a hint in your response.\n"
    #     "2. Do NOT use the hint as your placeholder for the answer unless your calculations leads to that answer.\n"
    # )

    prompt = ("You are an expert in explaining complex concepts. Given the correct answer, provide a comprehensive "
            "step-by-step rationale for why it is correct. Consider multiple angles and potential counterarguments.\n\n"
            f"Question: {question}\n"
            f"Correct Answer: {correct_answer}\n"
            "A: Let's break this down step-by-step:\n\n")

    try:
        # Use Ollama (or your LLM) to get the response
        response = ollama.chat(model=llama_v5, messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])

        # Extract the generated rationale
        generated_rationale = response['message']['content'].strip()

        return generated_rationale

    except Exception as e:
        print(f"Error during rationalization: {e}")
        return ''