# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from utils import format_message, setup_logging
from chat_store import ChatStore
from openai_api import OpenAIResponder
import logging
from typing import List, Dict
from datetime import datetime


testing = -1

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
print("Setting new conversation timestamp: ", timestamp)

# Make sure to set the OPENAI_API_KEY in your environment variables.
api_key = os.environ.get("OPENAI_API_KEY")

# initialize logging
logger = setup_logging('main_log')

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={r"/chat": {"origins": "*"}})

def _testing(conversation : List[Dict]):
    if testing == 0:
        # Call OpenAI API to generate a response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        print(response.choices[0].message.content)

        formatted_response = format_message(response.choices[0].message.content)

    elif testing == 1:
        with open('test_files/long_response_with_code.txt', 'r') as file:
            message = file.read()

        formatted_response = format_message(message)
    elif testing == 2:
        with open('test_files/short_response_with_code_and_list.txt', 'r') as file:
            message = file.read()

        formatted_response = format_message(message)
    elif testing == 3:
        with open('test_files/multi_line_response.txt', 'r') as file:
            message = file.read()

        formatted_response = format_message(message)

    print(formatted_response)


@app.route('/chat', methods=['POST'])

def chat():


    conversation = ChatStore.retrieve_chat(timestamp)

    
    print('conversation:',  conversation)

    # obtain user input from the frontend
    user_input = request.json.get('message')

    # we append it to the conversation
    conversation.append({
        'role': 'user', 
        'content': user_input
    })

    if testing >= 0:
        print("testing")
        _testing(conversation)
    
    # we define the primary AI settings
    primary_AI_responder = OpenAIResponder(
        api_key = api_key,
        #model = model_id,
        logger = logger
    )
    
    # we get the response from the primary AI
    content, status, details = primary_AI_responder.get_response(conversation)

    # we format it to html
    formatted_response = format_message(content)

    # we append the response to the conversation
    ChatStore.add_message(
        timestamp,
        {
            'role': 'assistant', 
            'content': formatted_response,
            'status' : status
        }
    )

    # we return the response to the frontend
    return jsonify({"response": formatted_response})

if __name__ == '__main__':
    app.run(debug=True)
