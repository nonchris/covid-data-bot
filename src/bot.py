import configparser
import logging
import json
import os

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import Bot

import bot_handlers as btc
import message_handlers as msh
config = configparser.ConfigParser()
config.read("config.ini")
updater = Updater(token=config['credentials']['TELEGRAM_TOKEN'], use_context=True)
dispatcher = updater.dispatcher

bot = Bot(token=config['credentials']['TELEGRAM_TOKEN'])



logging.basicConfig(
        filename="data/events.log",
        level= logging.INFO,
        style="{",
        format="[{asctime}] [{levelname}] {message}")

def start(update, context):
	context.bot.send_message(text="Hello my dear friend :)", chat_id=update.effective_chat.id)

def echo(update, context):
    print(update.message.from_user.username)
    print(update.message.chat)
    print("written")
    context.bot.send_message(chat_id=update.effective_chat.id, text="That's cool!")

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    print(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


#chats = writer.search_id(402239048)
#print("CHATS: ",chats)

start_handler = CommandHandler('start', btc.start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), msh.echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', btc.caps)
dispatcher.add_handler(caps_handler)

#bot.send_message(chat_id=402239048, text="Automated text")

updater.start_polling()