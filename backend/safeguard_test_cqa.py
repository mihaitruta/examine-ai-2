import os
import logging
import json
import re
from typing import List, Dict
from primary import PrimaryAI
from safeguard import SafeguardAI
from utils import read_records_with_id, setup_logging, write_objects_to_jsonl



api_key = os.getenv('OPENAI_API_KEY')

logger = setup_logging('safeguard_test_log')

def format_prompt(record: dict) -> str:
    # Extract the question stem
    question_stem = record['question']['stem']

    # Extract the choices and format them
    choices = record['question']['choices']
    formatted_choices = ' '.join([f"\n{choice['label']}. {choice['text']}" for choice in choices])

    # Construct the prompt
    prompt = f"Question: {question_stem}\nChoices:{formatted_choices}\nIdentify the one correct answer from the choices above. '"

    return prompt

def extract_answer(response : str) -> str:
    
    pattern_1 = r"The correct answer is\s+([A-E])"
    pattern_2 = r"Answer:\s*([A-E])"
    pattern_3 = r"\b([A-E])\.\s+\w+"

    patterns = [pattern_1, pattern_2, pattern_3]

    for pattern in patterns:
        match = re.search(pattern, response)
        if match:
            return match.group(1)

    return "X"


def get_answers(primaryAI : PrimaryAI, records : List[Dict], answers_file : str, ct : int = -1) -> List[Dict]:

    idx = 0
    for id, record in records.items():
        prompt = format_prompt(record)
        print(prompt)

        (response, status, details) = primaryAI.get_response_to_prompt(prompt)

        print(response)

        answer = extract_answer(response)

        print(answer)

        write_objects_to_jsonl([{'id': id, 'answer': answer}], answers_file, mode='a')

        idx += 1

        if ct > 0:
            if idx >= ct:
                break


def write_answers_to_jsonl(answers, file_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as file:
        for idx, answer in enumerate(answers):
            # Convert the answer to JSON and write it to the file
            json_line = json.dumps(answer)
            file.write(json_line)
            if idx < len(answers) - 1:
                file.write('\n')



if __name__ == "__main__":

    primary_model_id = 'gpt-4-1106-preview'
    dataset_file = './datasets/CommonsenseQA/train_rand_split_500.jsonl'
    answers_file = './results/CommonsenseQA/p_' + primary_model_id + '_cqa_500.jsonl'
    #answers_file = './results/CommonsenseQA/test.jsonl'
    

    primaryAI = PrimaryAI(
        api_key = api_key, 
        model = primary_model_id,
        logger = logger
    )

    records = read_records_with_id(dataset_file, logger=logger)

    get_answers(primaryAI, records, answers_file=answers_file)
