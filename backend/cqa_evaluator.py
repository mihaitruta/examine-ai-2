import logging
import json
import re
from typing import List, Dict
from primary import PrimaryAI
from safeguard import SafeguardAI
from utils import api_key, setup_logging, read_records, calculate_accuracy


if __name__ == "__main__":

    logger = setup_logging('eval_log')

    primary_model_id = 'gpt-3.5-turbo-0613'

    'p_gpt-3.5-turbo-0613_cqa_100.jsonl'

    dataset_file = './datasets/CommonsenseQA/train_rand_split_100.jsonl'
    answers_file = './results/CommonsenseQA/p_' + primary_model_id + '_cqa_100.jsonl'
    

    primaryAI = PrimaryAI(
        api_key = api_key, 
        model = primary_model_id,
        logger = logger
    )

    correct_answers = read_records(dataset_file, logger=logger, fields=['answerKey'])

    pAI_answers = read_records(answers_file, logger=logger, fields=['answer'])

    accuracy = calculate_accuracy(correct_answers, pAI_answers, logger=logger)

    print('accuracy = ', accuracy)