# -*- coding: utf-8 -*-

import logging

import telegram
import os
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters


#################
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# amend here to change your preset language
chat_language = os.getenv("INIT_LANGUAGE", default="id")

conversation = []


class ChatGPT:

    def __init__(self):

        self.messages = conversation
        self.model = os.getenv("OPENAI_MODEL", default="gpt-3.5-turbo")

    def get_response(self, user_input):
        conversation.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages

        )

        conversation.append(
            {"role": "assistant", "content": response['choices'][0]['message']['content']})

        print("Konten jawaban AI:")
        print(response['choices'][0]['message']['content'].strip())

        return response['choices'][0]['message']['content'].strip()


#####################
telegram_bot_token = str(os.getenv("TELEGRAM_BOT_TOKEN"))


# Load data from config.ini file
# config = configparser.ConfigParser()
# config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=telegram_bot_token)


@app.route('/callback', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


def reply_handler(bot, update):
    """Reply message."""
    # text = update.message.text
    # update.message.reply_text(text)
    chatgpt = ChatGPT()

    # update.message.text 人類的問題 the question humans asked
    # ChatGPT產生的回答 the answers that ChatGPT gave
    ai_reply_response = chatgpt.get_response(update.message.text)

    # 用AI的文字回傳 reply the text that AI made
    update.message.reply_text(ai_reply_response)


# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)
