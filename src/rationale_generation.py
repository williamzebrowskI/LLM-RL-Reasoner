import re
import ollama

qwen = "qwen2.5:7b"
llama = "llama3.1:8b"

def generate_rationale_and_answer(question, options, prompt_set, model=llama):
    options_text = '\n'.join([f"{key}) {value}" for key, value in options.items()])
    
    input_text = (
        prompt_set
        + "\n\n"
        + "Please solve the following problem and provide a detailed explanation. "
        + "Ensure that you end your response with the following format:\n"
        + "\"And the answer is: [answer]\"\n\n"
        + f"Question: {question}\n"
        + "Options:\n"
        + options_text
        + "\nAnswer Explanation:"
    )
    
    try:
        response = ollama.chat(model=model, messages=[
            {
                'role': 'user',
                'content': input_text,
            },
        ])
        
        generated_rationale_full = response['message']['content'].strip()
        generated_rationale = generated_rationale_full
        generated_answer_text = extract_answer(generated_rationale, options)
        
    except Exception as e:
        print(f"Error generating rationale: {e}")
        generated_rationale = ''
        generated_answer_text = None
    
    return generated_rationale, generated_answer_text

def extract_answer(generated_rationale, options):
    match = re.search(r'And the answer is:\s*([A-E])\)?\s*([$]?[0-9.]+)', generated_rationale, re.IGNORECASE)
    
    if match:
        option_letter = match.group(1).upper()
        answer_value = match.group(2).strip()
        
        if option_letter in options:
            if answer_value == options[option_letter]:
                return options[option_letter]
            else:
                return options[option_letter]
        else:
            for key, value in options.items():
                if value.lower() == answer_value.lower():
                    return value
            return None
    else:
        return None