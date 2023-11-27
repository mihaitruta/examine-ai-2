const exampleCode = `
# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from utils import format_message

testing = 0

# Initialize the Flask application
app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})
  # Enable CORS for all routes

# initialize openai client using OpenAI API key from environment variable
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    if testing == 0:
        # Call OpenAI API to generate a response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_input}]
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

    print(formatted_response)

    return jsonify({"response": formatted_response})

if __name__ == '__main__':
    app.run(debug=True)

`;
export default exampleCode;