# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from utils import format_message, setup_logging
from openai_api import OpenAIResponder
import logging

testing = -1

# Make sure to set the OPENAI_API_KEY in your environment variables.
api_key = os.environ.get("OPENAI_API_KEY")

# initialize logging
logger = setup_logging('main_log')

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/chat": {"origins": "*"}})


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_input}]
    
    if testing == 0:
        # Call OpenAI API to generate a response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
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
    else:
        formatted_response = format_message("...")




    primary_AI_responder = OpenAIResponder(
        api_key = api_key,
        #model = model_id,
        logger = logger
    )

    content, status, details = primary_AI_responder.get_response(messages)

    formatted_response = format_message(content)
    print(formatted_response)

    return jsonify({"response": formatted_response})

if __name__ == '__main__':
    app.run(debug=True)
