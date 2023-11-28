import os
from datetime import datetime
from utils import setup_logging, read_records, write_objects_to_jsonl
from typing import Dict


logger = setup_logging('chat_store_log')

class ChatStore:

    @staticmethod
    def retrieve_chat(timestamp, file_dir = 'chat_logs'):
        file_path = f"{file_dir}/chat_log_{timestamp}.jsonl"

        # Ensure the directory exists
        os.makedirs(file_dir, exist_ok=True)
        # Create the file if it doesn't exist
        with open(file_path, 'a') as file:
            pass 

        return read_records(file_path, logger=logger)

    @staticmethod
    def add_message(timestamp, message : Dict, file_dir = 'chat_logs'):
        file_path = f"{file_dir}/chat_log_{timestamp}.jsonl"
        write_objects_to_jsonl([message], file_path, mode='a')