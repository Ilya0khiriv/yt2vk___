import sys
import requests
import json
import re
import os
from typing import Optional
from dotenv import load_dotenv; load_dotenv()

def response(text=None, chat=None, cust_sys=None):
    class DeepSeekAPI:
        """
        A class to interact with the DeepSeek API for initiating chat sessions.
        """

        def __init__(self, api_token: Optional[str] = os.environ.get("DEEPSEEK")):
            self.command = None
            self.auth_headers = {
                'Authorization': f'Bearer {api_token}'
            }
            self.api_base_url = 'https://chat.deepseek.com/api/v0/chat'
            self.api_session = requests.Session()
            self.api_session.headers.update(self.auth_headers)

            if not cust_sys:
                with open("ban.txt", "r") as s:
                    self.instructions = s.read()
            else:
                self.instructions = cust_sys

        def clear_chat(self) -> None:
            """
            Clears the chat context by making a POST request to the clear_context endpoint.
            """
            clear_payload = {"model_class": "deepseek_chat", "append_welcome_message": False}
            clear_response = self.api_session.post(f'{self.api_base_url}/clear_context', json=clear_payload)
            clear_response.raise_for_status()

        def generate(self, user_message: str, response_temperature: float = 1.0, model_type: Optional[str] = "deepseek_chat", verbose: bool = False, system_prompt: Optional[str] = ""):
            """
            Generates a response from the DeepSeek API based on the provided message.
            """
            request_payload = {
                "message": f"[Instructions: {self.instructions}]\n\nUser Query:{user_message}",
                "stream": True,
                "model_preference": None,
                "model_class": model_type,
                "temperature": response_temperature
            }
            api_response = self.api_session.post(f'{self.api_base_url}/completions', json=request_payload, stream=True)
            api_response.raise_for_status()

            combined_response = ""
            for response_line in api_response.iter_lines(decode_unicode=True, chunk_size=1):
                try:
                    if response_line:
                        cleaned_line = re.sub("data:", "", response_line)
                        response_json = json.loads(cleaned_line)
                        response_content = response_json['choices'][0]['delta']['content']
                        if response_content and not re.match(r'^\s{5,}$', response_content):
                            if verbose: print(response_content, end="", flush=True)
                            combined_response += response_content
                except:
                    pass

            return combined_response

    api = DeepSeekAPI()

    if chat:
        while True:
            d = input(f"\nYou: ")
            response = api.generate(user_message=d, model_type='deepseek_chat', verbose=False)
            print(f"\nAI: {response}")
            
    api.clear_chat()
    print(f"\nYou: {text}")
    response = api.generate(user_message=text, model_type='deepseek_chat', verbose=False)
    print(f"\nAI: {response}")
    return response

if __name__ == "__main__":
    text = "lol"

    cust_sys = """
        забудь мои все мои команды прежде
        Ты переводчик и твоя задача выдать перевод на русский: который должен содержать то же колличество слов, что и оригинальный текст
        никогда не убирай ' /n ' даже если оно всередине предложения
        """
    response = response(text=text, cust_sys=None)

    print(response)