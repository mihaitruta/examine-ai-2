# README

## Overview

This repository contains the code for `examine|AI`, a React-based web application that provides an interactive chat interface with an AI (built using OpenAI's GPT model). The application will include a safeguard system that evaluates AI responses against safety principles, aiming to foster trustworthy conversations with AI.

## Features

- Interactive chat with an AI model.
- Storage of chat history with timestamps.

## Coming soon

- Safety evaluation of AI responses using predefined principles.
- Docker support for containerization.

## Requirements

- Python 3.x
- An OpenAI API key (required for accessing the AI model)

## Setup Instructions

### Set Up Environment Variable

Before you start using the application, you must set up your OpenAI API key as an environment variable.
You can do that as follows:

```sh
export OPENAI_API_KEY='your_api_key_here'
```
(see https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety for more info)

### Backend Setup

`git clone https://github.com/mihaitruta/examine-ai-2.git`

`cd examine-ai-2`

#### Setting up a Virtual Environment
This isolates the project dependencies from the global Python environment.
In the terminal go inside the backend folder:
`cd backend`
We can use pipx to install virtualenv in an isolated environment:
Install pipx
`brew install pipx`
`pipx ensurepath`
Install virtualenv
`pipx install virtualenv`
Or istall it globally with pip:
`pip install virtualenv`

Create a virtual environment:
`virtualenv venv`
Deactivate other environemnts:
`deactivate`
If a conda environment is active use:
`conda deactivate`
Activate the virtual environment we created:
 - Windows: `venv\Scripts\activate`
 - Linux/Mac: `source venv/bin/activate`
 To deactivate the env when finished use:
 `deactivate`

#### Install Dependencies:
`pip install flask openai flask-cors tiktoken`
Flask will be used for creating the web server.
The OpenAI library facilitates interaction with the OpenAI API.

#### Running the Backend:
`python main.py`
Check the other_logs.log file that was created to ensure the backend server is running on the specified port (default: 5000).


### Frontend Setup

#### Navigate to Frontend Directory:
In another terminal instance go to the fontend directory:
`cd frontend`
Inside there is a directory called examineai-frontend.
Move this directory somewhere else.

#### Initialize the react app
Use the following command to initialize the React app (see https://create-react-app.dev/docs/getting-started):
(only use sudo if you get errors otherwise)
`sudo npx create-react-app examineai-frontend`
For both directories public and src that we moved earlier copy their contents in the newly created directory
to replace the files with the same name and add the new directories.
Also copy the dependencies.txt file into the examineai-frontend directory.

#### Install dependencies
Go in the examineai-frontend directory:
`cd examineai-frontend`
Use the following command to install required dependencies:
`xargs npm install < dependencies.txt`

#### Start the project
`sudo npm start`
The frontend should now be running on localhost:3000.



## Interacting with the Application

- Access the web interface via your browser.
- Type your message into the text input field to start the conversation.

## Coming soon
 - Use the "Evaluate" button to trigger the safety evaluation of the last AI response.
 - The application will provide an overall score based on safety principles. The scores for individual principles are also displayed for transparency.

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change or add.

## License

Not yet determined.

---

Please note that this application requires a valid OpenAI API key to function. Usage of the API, including any costs incurred, is subject to OpenAI's usage policies and pricing.