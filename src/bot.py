import threading
import datetime
import logging
import time
import os

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram import Bot
from telegram import error

import commands.commands as cmd
import commands.mod_commands as mdc
import commands.handle_callback as hcb

import data_handling.csv_database as csv_database
import data_handling.analyzer as ana
import data_handling.utils as utils

import request_handling.requester_v2 as req2


API_Key = os.environ['API_Key']
LINK = os.environ["REQUEST_LINK"]
START_NUM = int(os.environ["START_NUM"])
OWNER_USERNAME = os.environ["OWNER_USERNAME"]
REQUEST_INTERVAL = int(os.environ["REQUEST_INTERVAL_SECONDS"])

updater = Updater(API_Key, use_context=True)
dispatcher = updater.dispatcher

bot = Bot(token=API_Key)

logging.basicConfig(
    filename="data/events.log",
    level=logging.INFO,
    style="{",
    format="[{asctime}] [{levelname}] [{name}] {message}")


def send_update(date):
    analyzer = ana.Analyzer(date)

    for city in utils.city_list:
        path = analyzer.visualize(city)

        for chat in writer.entries:
            s = chat.settings
            if s[city.lower()] or s["all"]:
                # print(path)
                try:
                    logging.info(f"SENDING {city: <12} to {chat.id}")
                    bot.send_photo(chat.id, photo=open(path, 'rb'))
                except error.Unauthorized:
                    logging.info(f"Blocked by {chat.username: <12} {chat.id} - passing")

                time.sleep(0.04)  # block that makes sure that 30 messages per second aren't exceeded
            else:
                logging.info(
                    f"Ignoring {city: <11} on {chat.id} - {s[city.lower()]} ({type(s[city.lower()])}) - {s['all']} ({type(s['all'])})")


def make_request():
    rq = req2.RequesterV2('https://www.kreis-ahrweiler.de/presse.php?lfdnrp=', START_NUM)
    while True:
        #rq = req.Requester(LINK)
        # first doing request and then making JSON - both return bool
        if rq.do_request() and rq.make_json():
            print("entered")
            logging.info('Got the requested data - starting dispatch')
            send_update(rq.pub_date)
            logging.info("Sent all messages, sleeping until tomorrow")

            d = datetime.datetime.now()
            till_tomorrow = ((24 - d.hour - 1) * 60 * 60) \
                            + ((60 - d.minute - 1) * 60) \
                            + (60 - d.second) \
                            + (3600 * 7)  # earliest request starts at 7 am
            time.sleep(till_tomorrow)

        else:
            logging.info(f"No new data - sleeping for {round(REQUEST_INTERVAL / 60)} minutes")
            time.sleep(REQUEST_INTERVAL)  # requesting every hour


reqest_thrd = threading.Thread(target=make_request)
reqest_thrd.start()

writer = csv_database.Writer()
# passing writer object into other files
cmd.setup(writer)
mdc.setup(writer)

start_handler = CommandHandler('start', cmd.start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), cmd.menu_menu)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', cmd.caps)
dispatcher.add_handler(caps_handler)

menu_show_handler = CommandHandler(['zeig_graph', 'zeig', 'show', 'zg', 'sh', 's', 'z'], cmd.menu_show)
dispatcher.add_handler(menu_show_handler)

menu_abo_handler = CommandHandler(['abo', 'sub', 'abonnieren'], cmd.menu_abo)
dispatcher.add_handler(menu_abo_handler)

menu_menu_handler = CommandHandler(['menu', 'menue'], cmd.menu_menu)
dispatcher.add_handler(menu_menu_handler)

show_handler = CommandHandler(['Adenau', 'Altenahr', 'Ahrweiler', 'Breisig', 'Brohltal',
                               'Grafschaft', 'Neuenahr', 'Remagen', 'Sinzig',
                               'Bad_Breisig', 'Bad_Neuenahr', 'Bad_Neuenahr_Ahrweiler'
                               ], cmd.show)
dispatcher.add_handler(show_handler)

hilfe_handler = CommandHandler(['hilfe', 'hilf', 'help', 'h', 'abo', 'a', 'mehr', 'more'], cmd.help)
dispatcher.add_handler(hilfe_handler)

about_handler = CommandHandler('about', cmd.about)
dispatcher.add_handler(about_handler)

methods_handler = CommandHandler(["methods", "methoden", "berechnung"], cmd.methods)
dispatcher.add_handler(methods_handler)

notify_handler = CommandHandler("notify", mdc.notify_all)
dispatcher.add_handler(notify_handler)

# responsible for all inline commands
dispatcher.add_handler(CallbackQueryHandler(hcb.handle_callback))

updater.start_polling()
updater.idle()
