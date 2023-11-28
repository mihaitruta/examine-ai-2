import os
from datetime import datetime
from utils import setup_logging, read_records, write_objects_to_jsonl
from typing import Dict
from datetime import datetime
import random
import string


logger = setup_logging('chat_store_log')

class ChatStore:

    @staticmethod 
    def new_chat(file_dir = 'chat_logs'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chat_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
        file_path = f"{file_dir}/chat_list.jsonl"

        # initialize the log file
        log_path = f"{file_dir}/chat_log_{timestamp}_{chat_id}.jsonl"
        with open(log_path, 'w') as file:
            pass 

        write_objects_to_jsonl([{
            'timestamp' : timestamp,
            'id' : chat_id,
            'file_path' : log_path
        }], file_path, mode='a', new_line = 2)

        return chat_id


    @staticmethod 
    def _new_chat(file_dir = 'chat_logs'):
        file_path = f"{file_dir}/chat_list.jsonl"

        # Ensure the directory exists
        os.makedirs(file_dir, exist_ok=True)
        # Create the file if it doesn't exist
        with open(file_path, 'a') as file:
            pass 

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chat_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))


        # initialize the log file
        log_path = f"{file_dir}/chat_log_{timestamp}_{chat_id}.jsonl"
        with open(file_path, 'w') as file:
            pass 
        
        write_objects_to_jsonl([{
            'timestamp' : timestamp,
            'id' : chat_id,
            'file_path' : log_path
        }], file_path, mode='a')

        return chat_id

    @staticmethod
    def _retrieve_chat_file_path(chat_id : str, file_dir = 'chat_logs'):

        file_path = f"{file_dir}/chat_list.jsonl"

        # Ensure the directory exists
        os.makedirs(file_dir, exist_ok=True)
        # Create the file if it doesn't exist
        with open(file_path, 'a') as file:
            pass 

        if os.path.exists(file_path):
            chats = read_records(file_path, logger=logger)

        for chat in chats:
            if chat['id'] == chat_id:
                return chat['file_path']

        return None


    @staticmethod
    def retrieve_chat(chat_id : str, file_dir = 'chat_logs'):
        log_path = ChatStore._retrieve_chat_file_path(chat_id, file_dir = file_dir)
        return read_records(log_path, logger=logger)
                

    @staticmethod
    def add_message(chat_id, message : Dict, file_dir = 'chat_logs'):
        log_path = ChatStore._retrieve_chat_file_path(chat_id, file_dir = file_dir)
        write_objects_to_jsonl([message], log_path, mode='a')