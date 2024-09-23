from .parsing import parse_options
from .utils import escape_special_characters

def create_prompt_examples(ds_train, num_examples):
    prompt_examples = []
    for i in range(num_examples):
        example = ds_train[i]
        question = example['question']
        options = example['options']
        rationale = example['rationale']
        correct_option = example['correct'].strip().upper()
        
        options_dict = parse_options(options)
        correct_answer = options_dict.get(correct_option, None)
        
        if correct_answer is None:
            print(f"Warning: Correct answer not found for prompt example index {i}. Skipping.")
            continue
        
        escaped_rationale = escape_special_characters(rationale)
        
        example_response = (
            "Question: {}\n"
            "Options:\n{}\n"
            "Answer Explanation: {}\n"
            "Answer: {}\n"
            "Please respond with only the letter corresponding to the correct answer (A, B, C, D, or E).\n"
            "###\n"
        ).format(
            question,
            '\n'.join(options),
            escaped_rationale,
            correct_answer
        )
        
        prompt_examples.append({
            'question': question,
            'options': options,
            'rationale': escaped_rationale,
            'answer': correct_option
        })
    return prompt_examples

def create_prompt_set(ds_train, num_examples):
    prompt_set = ""
    for i in range(num_examples):
        example = ds_train[i]
        question = example['question']
        options = example['options']
        rationale = escape_special_characters(example['rationale'])
        correct_option = example['correct'].strip().upper()
        
        # options_dict = parse_options(options)
        # correct_answer_text = options_dict.get(correct_option, "")
        
        prompt_set += (
            "Question: {}\n"
            "Options:\n{}\n"
            "Answer Explanation: {}\n"
            "Answer: {}\n"
            "Please respond with only the letter corresponding to the correct answer (A, B, C, D, or E).\n"
            "###\n"
        ).format(
            question,
            '\n'.join(options),
            rationale,
            correct_option
        )
    return prompt_set