import os
import requests
import re
import readline
from dotenv import load_dotenv
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from rich import print as rprint
from rich.markdown import Markdown

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import ANSI


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

class GPTChat:
    def __init__(self):
        self.historial_chat = []

    def enviar_mensaje(self, mensaje, model="gpt-3.5-turbo"):
        if len(mensaje) > 4096:
            print("Error: El mensaje de entrada es demasiado largo. Por favor, acórtalo e intenta de nuevo.")
            return None

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        historial_mensajes = [{"role": "user" if i % 2 == 0 else "assistant", "content": msg} for i, msg in enumerate(self.historial_chat)]
        historial_mensajes.append({"role": "user", "content": mensaje})

        data = {
            "model": model,
            "messages": historial_mensajes,
            "temperature": 0.5,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            choices = response.json()["choices"]
            return choices[0]["message"]["content"].strip()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

    @staticmethod
    def resaltar_codigo(texto):
        texto_rich = Markdown(texto)
        rprint(texto_rich)


    def main(self):
        print_formatted_text(ANSI('\033[32mEscribe \'exit\' para terminar la conversación :: GPTchat ▓▒░\033[0m'))
        session = PromptSession(history=InMemoryHistory())

        try:
            while True:
                mensaje = session.prompt(ANSI('\033[32m\n/>: \033[0m'))
                if mensaje.lower() == "salir":
                    break

                respuesta = self.enviar_mensaje(mensaje)

                if respuesta:
                    print_formatted_text(ANSI('\033[31mOutput:\033[0m'))
                    self.resaltar_codigo(respuesta)
                    self.historial_chat.extend([mensaje, respuesta])
                else:
                    print(None)
        except (EOFError, KeyboardInterrupt):
            print_formatted_text(ANSI('\n\033[32mSaliendo del programa...\033[0m'))
            pass

        for entrada in self.historial_chat[::2]:
            readline.add_history(entrada)

if __name__ == "__main__":
    histfile = ".conversation_history"
    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        pass

    gpt_chat = GPTChat()

    try:
        gpt_chat.main()
    finally:
        readline.set_history_length(1000)
        readline.write_history_file(histfile)
