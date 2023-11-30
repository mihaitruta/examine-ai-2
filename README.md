# README

## Overview

This repository contains the code for `examine|AI`, a React-based web application that provides an interactive chat interface with an AI (built using OpenAI's GPT model). The application will include a safeguard system that evaluates AI responses against safety principles, aiming to foster trustworthy conversations with AI.

## Features

- Interactive chat with an AI model.
- Storage of chat history with timestamps.
- Factuality Evaluation

## Coming soon

- In depth safety evaluation of AI responses.
- Docker support for containerization.

## Requirements

- Python 3.12 ([download here](https://www.python.org/downloads/release/python-3120/))
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
Clone the repository to your local device:
`git clone https://github.com/mihaitruta/examine-ai-2.git`
In a terminal go to the project folder:
`cd examine-ai-2`

#### Setting up a Virtual Environment
This isolates the project dependencies from the global Python environment.
In the terminal go inside the backend folder:
`cd backend`
Create a new virtual environment:
python3.12 -m venv /path/to/new/virtualenv
Deactivate other environemnts:
`deactivate`
If a conda environment is active use:
`conda deactivate`
Activate the virtual environment we created:
 - Windows: `\path\to\new\virtualenv\Scripts\activate`
 - Linux/Mac: `source /path/to/new/virtualenv/bin/activate`
 To deactivate the env when finished use:
 `deactivate`

#### Install Dependencies:
`pip install -r requirements.txt`

#### Running the Backend:
`python main.py`
The backend server should now be running on the default port (5000).

### Frontend Setup

#### Navigate to Frontend Directory:
In another terminal instance go to the fontend directory:
`cd frontend`
Inside there is a directory called examineai-frontend.
Move this directory somewhere else.

#### Initialize the react app
Use the following command to initialize the React app (see [React Getting Started](https://create-react-app.dev/docs/getting-started)):
(only use sudo if you get errors otherwise)
`sudo npx create-react-app examineai-frontend`
For each file in the directory we moved earlier copy it back to the newly created project directory.
Replace any files with identical names.

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
- Use the "Evaluate" button to trigger the safety evaluation of the AI responses.

## Coming soon

 - Improved in-depth multi-dimensinal evaluation

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change or add.

## License

Not yet determined.

---

Please note that this application requires a valid OpenAI API key to function. Usage of the API, including any costs incurred, is subject to OpenAI's usage policies and pricing.