import threading
import datetime
import logging
import time
import os

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import Bot
from telegram import error

import src.commands.commands as cmd
import src.commands.mod_commands as mdc
import src.commands.message_handlers as msh
import src.commands.subscription_commands as sbc

import src.data_handling.csv_database as csv_database
import src.data_handling.analyzer as ana

import src.data_handling.utils as utils

import requester as req

API_Key = os.environ['API_Key']
LINK = os.environ["REQUEST_LINK"]
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
    while True:
        rq = req.Requester(LINK)
        if rq.success:
            logging.info('Got the requested data - starting dispatch')
            send_update(rq.date)
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
msh.setup(writer)
sbc.setup(writer)
mdc.setup(writer)

start_handler = CommandHandler('start', cmd.start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), msh.echo)
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

####
# kreis
kreis_handler = CommandHandler(['abo_kreis', 'sub_kreis',
                                'abokreis', 'subkreis', 'akreis', 'skreis'], sbc.tgl_kreis)
dispatcher.add_handler(kreis_handler)

# adenau
adenau_handler = CommandHandler(['abo_adenau', 'sub_adenau',
                                 'aboadenau', 'subadenau', 'aadenau', 'sadenau'], sbc.tgl_adenau)
dispatcher.add_handler(adenau_handler)

# altenahr
altenahr_handler = CommandHandler(['abo_altenahr', 'sub_altenahr',
                                   'aboaltenahr', 'subaltenahr', 'aaltenahr', 'saltenahr'], sbc.tgl_altenahr)
dispatcher.add_handler(altenahr_handler)

# breisig
breisig_handler = CommandHandler(['abo_breisig', 'sub_breisig', 'abobreisig', 'subbreisig',
                                  'abreisig', 'abo_bad_breisig', 'sub_bad_breisig', 'sbreisig'], sbc.tgl_breisig)
dispatcher.add_handler(breisig_handler)

# brohltal
brohltal_handler = CommandHandler(['abo_brohltal', 'sub_brohltal',
                                   'abobrohltal', 'subbrohltal', 'abrohltal', 'sbrohltal'], sbc.tgl_brohltal)
dispatcher.add_handler(brohltal_handler)

# grafschaft
grafschaft_handler = CommandHandler(['abo_grafschaft', 'sub_grafschaft',
                                     'abografschaft', 'subgrafschaft', 'agrafschaft', 'sgrafschaft'],
                                    sbc.tgl_grafschaft)
dispatcher.add_handler(grafschaft_handler)

# neuenahr/ahrweiler
neuenahr_handler = CommandHandler(['abo_neuenahr', 'sub_neuenahr',
                                   'aboneuenahr', 'subneuenahr', 'aneuenahr', 'abo_bad_neuenahr', 'sneuenahr',
                                   'abo_ahrweiler', 'sub_ahrweiler',
                                   'aboahrweiler', 'subahrweiler', 'aahrweiler', 'sahrweiler'], sbc.tgl_neuenahr)
dispatcher.add_handler(neuenahr_handler)

# remagen
remagen_handler = CommandHandler(['abo_remagen', 'sub_remagen',
                                  'aboremagen', 'subremagen', 'aremagen', 'sremagen'], sbc.tgl_remagen)
dispatcher.add_handler(remagen_handler)

# sinzig
sinzig_handler = CommandHandler(['abo_sinzig', 'sub_sinzig',
                                 'abosinzig', 'subsinzig', 'asinzig', 'ssinzig'], sbc.tgl_sinzig)
dispatcher.add_handler(sinzig_handler)

# kreis
kreis_handler = CommandHandler(['abo_kreis', 'sub_kreis',
                                'abokreis', 'subkreis', 'akreis', 'skreis'], sbc.tgl_kreis)
dispatcher.add_handler(kreis_handler)

# alle
alle_handler = CommandHandler(['abo_alle', 'sub_alle',
                               'aboalle', 'suballe', 'aalle', 'salle'], sbc.tgl_alle)
dispatcher.add_handler(alle_handler)

# ['abo_', 'sub_', 'abo', 'sub', 'a']

# bot.send_message(chat_id=402239048, text="Automated text")

updater.start_polling()
updater.idle()
