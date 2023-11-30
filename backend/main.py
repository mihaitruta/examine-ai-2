import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from utils import format_message, setup_logging
from chat_store import ChatStore
from openai_api import OpenAIResponder
import logging
from typing import List, Dict
from datetime import datetime
from safeguard import SafeguardAI
import argparse

testing = -1

# Make sure to set the OPENAI_API_KEY in your environment variables.
api_key = os.environ.get("OPENAI_API_KEY")

# initialize logging
logger = setup_logging('main_log')

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={r"/chat": {"origins": "*"}, r"/reset_chat": {"origins": "*"}, r"/get_eval": {"origins": "*"} })

def _testing():
    test_responses = {
        1: lambda: open('test_files/long_response_with_code.txt').read(),
        2: lambda: open('test_files/short_response_with_code_and_list.txt').read(),
        3: lambda: open('test_files/multi_line_response.txt').read()
    }

    response_generator = test_responses.get(testing)
    if response_generator:
        message = response_generator()
        formatted_response = format_message(message)
        return formatted_response

    return None


# endpoint for resetting chat
@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    chat_id = ChatStore.new_chat()
    return jsonify({'message' : 'reset', 'chat_id' : chat_id})


# endpoint for obtaining evaluation
@app.route('/get_eval', methods=['POST'])
def get_eval():
    print("Getting safeguard eval")

    data = request.get_json()
    print(data)
    user_input = data.get('message')
    chat_id = data.get('chat_id')
    print(user_input)
    print(chat_id)

    # we define the safeguard AI settings
    safeAI = SafeguardAI(
        api_key = api_key,
        model = 'gpt-3.5-turbo-0613',
        logger=logger
    )

    evaluation = safeAI.get_evaluation(chat_id)

    return jsonify({'evaluation' : evaluation})
    
    
# endpoint for chat responses
@app.route('/chat', methods=['POST'])
def chat():

    # obtain user input from the frontend
    data = request.get_json()
    user_input = data.get('message')
    chat_id = data.get('chat_id')

    # if testing we return predefined response
    testing = app.config['TESTING']
    if testing > -1:
        test_response = _testing(conversation)
        if test_response is not None:
            return jsonify({"response": test_response})

    # we store the user reply
    ChatStore.add_user_message(chat_id, user_input)

    # we retrieve the conversation based on chat_id
    conversation = ChatStore.retrieve_chat(chat_id)
    
    # we define the primary AI settings
    primary_AI_responder = OpenAIResponder(
        api_key = api_key,
        logger = logger
    )
    # we get the response from the primary AI
    content, status, details = primary_AI_responder.get_response(conversation)
    # we format it to html
    formatted_response = format_message(content)
    # we append the response to the conversation
    ChatStore.add_assistant_message(chat_id, formatted_response, status)
    # we return the response to the frontend
    return jsonify({"response": formatted_response})


if __name__ == '__main__':
    # Argument parser setup
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--testing', 
        type=int, 
        default=-1, 
        help='testing with hard coded response'
    )
    args = parser.parse_args()
    testing = args.testing

    app.config['TESTING'] = args.testing

    app.run(debug=True)
