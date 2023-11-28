
import os
from openai_api import OpenAIResponder

api_key = os.getenv('OPENAI_API_KEY')

class SafeguardAI:
    def __init__(self, api_key: str, model: str = 'gpt-3.5-turbo-0613', logger=None):
        self._api_key = api_key
        # initialize openai client using provided OpenAI API key
        self._model = model
        self._logger = logger
        self._responder = OpenAIResponder(api_key=api_key, model=model, logger=logger)

    def get_response(self, messages):
        response, status, details = self._responder.get_response(messages)
        return response, status, details


def _test_safeguard_ai():
    model = 'gpt-3.5-turbo-0613'

    prompt = "Q: Who starred in the 1996 blockbuster Independence Day?"
    prompt += "A: "
    
    safeguardAI = SafeguardAI(api_key=api_key, model=model)
    
    response, status, details = safeguardAI.get_response([{'role': 'system', 'content': prompt}])
    
    print('response ', response)
    print('status ', status)
    print('details ', details)


if __name__ == "__main__":
    _test_safeguard_ai()

