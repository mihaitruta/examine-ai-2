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
from safeguard import SafeguardAI


testing = -1

# Make sure to set the OPENAI_API_KEY in your environment variables.
api_key = os.environ.get("OPENAI_API_KEY")

# initialize logging
logger = setup_logging('main_log')

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={r"/chat": {"origins": "*"}, r"/reset_chat": {"origins": "*"}, r"/get_eval": {"origins": "*"} })

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


@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    chat_id = ChatStore.new_chat()
    return jsonify({'message' : 'reset', 'chat_id' : chat_id})



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
    
    

@app.route('/chat', methods=['POST'])
def chat():

    # obtain user input from the frontend
    data = request.get_json()
    user_input = data.get('message')
    chat_id = data.get('chat_id')
    print(chat_id)

    conversation = ChatStore.retrieve_chat(chat_id)

    # we append it to the conversation
    conversation.append({
        'role': 'user', 
        'content': user_input
    })

    # we store the user reply
    ChatStore.add_message(
        chat_id,
        {
            'role': 'user', 
            'content': user_input,
            'status' : 'OK'
        }
    )

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
        chat_id,
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
