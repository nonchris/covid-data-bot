import configparser
import logging
import atexit
import time
import sys


from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import Bot

import bot_handlers as btc
import toggle_subs as tgs
import message_handlers as msh
import csv_utils

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



@atexit.register
def goodbye():
    writer.write()
    print("Saved to file - stopping now")

writer = csv_utils.Writer()
#passing writer object into other files
btc.setup(writer)
msh.setup(writer)
tgs.setup(writer)

#chats = writer.search_id(402239048)
#print("CHATS: ",chats)

start_handler = CommandHandler('start', btc.start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), msh.echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', btc.caps)
dispatcher.add_handler(caps_handler)

help_handler = CommandHandler('hilfe', btc.help)
dispatcher.add_handler(help_handler)

help_handler = CommandHandler('help', btc.help)
dispatcher.add_handler(help_handler)

####
kreis_handler = CommandHandler('kreis', tgs.kreis)
dispatcher.add_handler(kreis_handler)

adenau_handler = CommandHandler('adenau', tgs.adenau)
dispatcher.add_handler(adenau_handler)

altenahr_handler = CommandHandler('altenahr', tgs.altenahr)
dispatcher.add_handler(altenahr_handler)

breisig_handler = CommandHandler('breisig', tgs.breisig)
dispatcher.add_handler(breisig_handler)

brohltal_handler = CommandHandler('brohltal', tgs.brohltal)
dispatcher.add_handler(brohltal_handler)

grafschaft_handler = CommandHandler('grafschaft', tgs.grafschaft)
dispatcher.add_handler(grafschaft_handler)

neuenahr_handler = CommandHandler('neuenahr', tgs.neuenahr)
dispatcher.add_handler(neuenahr_handler)

remagen_handler = CommandHandler('remagen', tgs.remagen)
dispatcher.add_handler(remagen_handler)

sinzig_handler = CommandHandler('sinzig', tgs.sinzig)
dispatcher.add_handler(sinzig_handler)

kreis_handler = CommandHandler('kreis', tgs.kreis)
dispatcher.add_handler(kreis_handler)

alle_handler = CommandHandler('alle', tgs.alle)
dispatcher.add_handler(alle_handler)


#bot.send_message(chat_id=402239048, text="Automated text")

updater.start_polling()