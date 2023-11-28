import os
import re
import tiktoken
from typing import List, Dict
import json
import logging
import sys

EXIT_STATUS_ANSWERS_MALFORMED = 1
EXIT_STATUS_PREDICTIONS_MALFORMED = 2
EXIT_STATUS_PREDICTIONS_EXTRA = 3
EXIT_STATUS_PREDICTION_MISSING = 4

api_key = os.getenv('OPENAI_API_KEY')

# in $ / 1K tokens
api_details = {
    'gpt-3.5-turbo-1106' : {'prompt' : 0.001, 'output' : 0.002, 'context' : 16385},
    'gpt-3.5-turbo-0613' : {'prompt' : 0.001, 'output' : 0.002, 'context' : 4096},
    'gpt-3.5-turbo-16k-1106' : {'prompt' : 0.002, 'output' : 0.004, 'context' : 16385},
    'gpt-3.5-turbo-16k-0613' : {'prompt' : 0.002, 'output' : 0.004, 'context' : 16385},
    'gpt-4-0613' : {'prompt' : 0.03, 'output' : 0.06, 'context' : 8192},
    'gpt-4-32k-0613' : {'prompt' : 0.06, 'output' : 0.12, 'context' : 32768},
    'gpt-4-1106-preview' : {'prompt' : 0.01, 'output' : 0.03, 'context' : 128000},
    }

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def escape_html(text):
    """Escape special HTML characters in text."""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\"", "&quot;")
                .replace("'", "&#039;"))

def format_message(text):
    in_code_block = False
    formatted_lines = []
    code_lines = []
    code_content = ''
    language = None


    lines = text.split('\n')
    lines_ct = len(text.split('\n'))
    for idx, line in enumerate(lines):
        if line.startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                # Extract language from the start of the code block
                language = line[3:].strip() or ""
                #line = f'<div class="code-header">{language}</div><pre>'
                #formatted_lines.append(line)
                #code_block = "<div class=\"code-header\" onclick=\"handleCodeHeaderClick(`" + code_content + "`)\">python</div><pre>" + code_content + "</pre>"
            else:
                #header_line = f'<div class="code-header" onclick="handleCodeHeaderClick(`' + code_content + '`)">{language}</div><pre>'
                header_line = f'<div class="code-container"><div class="code-header">{language}</div><pre>'
                formatted_lines.append(header_line)
                formatted_lines.extend(code_lines)
                formatted_lines.append('</pre></div>')
                code_lines = []
                code_content = ''
            continue

        if in_code_block:
            code_lines.append(escape_html(line))
            code_content += line + '\n'
        else:
            if re.match(r"^\d+\.\s+", line):
                # Apply list formatting to lines outside code blocks
                formatted_line = re.sub(r"^(\d+\.)\s+(.*)", r"<li>\2</li>", escape_html(line))
                formatted_lines.append(formatted_line)
            else:
                formatted_line = escape_html(line)
                #if formatted_line == '':
                #    formatted_line = '<br>'
                formatted_line += '<br>'
                formatted_lines.append(formatted_line)

        if idx == lines_ct - 1:
            if in_code_block:
                header_line = f'<div class="code-header">{language}</div><pre>'
                formatted_lines.append(header_line)
                formatted_lines.extend(code_lines)
                formatted_lines.append('</pre>')


    result = '\n'.join(formatted_lines)

    return result


# modified from 
# https://github.com/allenai/aristo-leaderboard/blob/master/openbookqa/evaluator/evaluator.py
def read_records_with_id(filename: str, logger, fields : List = None) -> Dict:

    records = {}

    with open(filename, "rt", encoding="UTF-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            try:
                record = json.loads(line)
            except ValueError as e:
                logging.error("Error while reading file %s: %s", filename, e)
                sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

            question_id = record["id"]

            if question_id in records:
                logging.error("Key %s repeated in %s", question_id, filename)
                sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)
            
            if fields is None:
                records[question_id] = record
            else:
                records[question_id] = {}
                for field in fields:
                    if field in record:
                        records[question_id][field] = record[field]
                    else:
                        logging.error("Field %s not in record %s in file %s.", field, question_id, filename)

    if len(records) == 0:
        logging.error("No answers found in file %s", filename)
        sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)
    logging.info("\nSuccessfully read file %s.\n", filename)
    
    return records

def read_records(filename: str, logger, fields : List = None) -> Dict:

    records = []

    record_nr = 0
    with open(filename, "rt", encoding="UTF-8", errors="replace") as f:
        for line in f:
            print("looking at line:<", line, '>')
            line = line.strip()
            if line != '':
                try:
                    record = json.loads(line)
                except ValueError as e:
                    logging.error("Error while reading file %s: %s", filename, e)

                if fields is None:
                    records.append(record)
                else:
                    item = {}
                    for field in fields:
                        if field in record:
                            item[field] = record[field]
                        else:
                            logging.error("Field %s not in record %s in file %s.", field, record_nr, filename)
                    records.append(item)
                record_nr += 1

    logging.info("\nSuccessfully read file %s.\n", filename)
    
    return records


# based on https://github.com/allenai/aristo-leaderboard/blob/master/openbookqa/evaluator/evaluator.py
def calculate_accuracy(actual : Dict, predicted : Dict, logger) :
    score = 0.0

    for question_id, answer in actual.items():
        try:
            # we take the first field as the answer (or list of answers)     
            predictions_for_q = next(iter(predicted[question_id].values()))  
        except KeyError:
            logging.error("Missing prediction for question '%s'.", question_id)
            sys.exit(EXIT_STATUS_PREDICTION_MISSING)

        # we take the first field as the answer 
        answer = next(iter(answer.values()))  

        if answer in predictions_for_q:
            score += 1.0 / len(predictions_for_q)

        del predicted[question_id]

    if len(predicted) > 0:
        logging.error("Found %d extra predictions, for example: %s", len(predicted),
                      ", ".join(list(predicted.keys())[:3]))
        sys.exit(EXIT_STATUS_PREDICTIONS_EXTRA)

    return score / len(actual)


def write_objects_to_jsonl(objects, file_path, mode='a', new_line = 1):

    # new_line = 1 write on new line if file is not empty
    # new_line = 2 always write on new line 

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    write_on_new_line = False

    if new_line == 1 :
        # Check if the file is non-empty
        try:
            with open(file_path, 'r') as file:
                # If the file has content, prepend a newline to the first line to append
                if file.read(1):
                    write_on_new_line = True
                    print('file is not empty')
        except FileNotFoundError:
            # If the file doesn't exist, it's okay; it will be created in append mode
            pass
    elif new_line == 2:
        write_on_new_line = True
    else:
        write_on_new_line = True


    with open(file_path, 'a') as file:
        for idx, obj in enumerate(objects):
            # Convert the object to JSON and write it to the file
            json_line = json.dumps(obj)
            # if we are adding the first object we potentially add a new line first
            if idx == 0:
               if write_on_new_line:
                    file.write('\n')
            file.write(json_line)
            # if we wrote the last object we skip the new line
            if idx < len(objects) - 1:
                file.write('\n')



def setup_logging(log_name : str):
    # Setup logging
    if log_name is not None:
        logging.basicConfig(
            filename=log_name+'.log', 
            level=logging.INFO, 
            format='\n<<<<<log>>>>> %(asctime)s - %(name)s - %(levelname)s - %(message)s <<<<</log>>>>>'
        )
        logger = logging.getLogger(log_name)
    else:
        logging.basicConfig(
                filename='default_log.log',
                level=logging.INFO, 
                format='\n<<<<<log>>>>> %(asctime)s - %(name)s - %(levelname)s - %(message)s <<<<</log>>>>>'
        )
        logger = logging.getLogger('default_log') 

    # Divert other logs away from the main log
    # Create a file handler for the log file
    file_handler = logging.FileHandler('other_logs.log')
    # set the level and formatter for the handler
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # Get the loggers for Werkzeug and add the handler
    for other_logger in (logging.getLogger('httpx'), logging.getLogger('werkzeug')):
        other_logger.addHandler(file_handler)
        other_logger.propagate = False  # Prevent logs from propagating to the root logger

    return logger