import datetime

from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext

import data_handling.utils as utils
import commands.keyboards as kb


def setup(wrtr):
    """passing csv access object to this"""
    global writer
    writer = wrtr


"""
Main commands of the bot that actually do something other than navigating menus and updating messages
There are some legacy commands below
"""


def start(update, context):
    """Command triggered at /start"""

    # extracting name of user
    name = ""
    if fname := update.message.chat.first_name:
        name = f"{fname} "
    if lname := update.message.chat.last_name:
        name += f"{lname} "
    if not name:
        name = f"{update.message.chat.username} "

    context.bot.send_message(
        text=f"Hallo {name.strip()},\n"
             "dieser Bot kann Ihnen täglich die neusten Covid-19 Fallzahlen aus von Ihnen abonnierten Regionen senden.\n\n"
             "Zusätzlich können Sie jederzeit die aktuelsten Zahlen zu einer Region aus dem Kreis abrufen.\n\n"
             "Bitte nehmen Sie zur Kenntniss, dass es sich bei dem Bot um ein privates Projekt handelt.\n"
             "Mit freundlichen Grüßen und bleiben Sie gesund!\n"
             "Covid Update Bot",
        reply_markup=kb.inline_start, chat_id=update.effective_chat.id)

    # saving chat/ user to database
    writer.add(update.message.chat)


def subscribe(update: Update, query: CallbackQuery, location: str) -> None:
    """
    Inline command responsible for handling subscriptions

    :param update: Telegram Update Object for getting right user
    :param query: Telegram Query Object for inline functionality
    :param location: Location that should be toggled

    - Adds user to database
    - Toggles status of chosen location
    - Updates message
    - Saves new settings to db
    """

    # getting chat by using the writer.add method
    # it checks database and adds chat if not already existing
    # the users chat will be returned
    chat = writer.add(update.effective_chat)

    settings = chat.settings  # settings of that chat contain subscription status
    # if location is not subscribed - subscribing
    if not settings[location]:
        settings[location] = True
        query.edit_message_text(text=f'Sie haben {location} abonniert',
                                reply_markup=kb.inline_sub_soft)

    # location is subscribed - settings subscription to false
    else:
        settings[location] = False
        query.edit_message_text(text=f'Sie haben {location} deabonniert',
                                reply_markup=kb.inline_sub_soft)

    # writing db to store changes
    writer.write()


def show(update: Update, context: CallbackContext, city='', query=None):
    """
    Shows graph of a given location

    :param update: Telegram Update Object
    :param context: Telegram Context Object
    :param city: Name of the requested location
    :param query: Inline Query

    Tries to find a graph of location generated in last five days\n
    Sends Error Message when no graph is available\n
    Graphs are always sent as a new message, there is no option for inline graphs

    """

    # this line exists to support legacy commands like /sinzig that request a graph via command
    if city == '':
        city = utils.translator[update['message']['text'][1:].lower()]

    # getting date form today for building filename
    # used to go trough the last five possible filenames
    today = datetime.date.today()

    for i in range(5):
        """Iterating trough last five days"""

        try:  # trying to open a filename
            date = today - datetime.timedelta(i)
            path = f"visuals/{city}-{date}.png"
            print(path)
            with open(path, "rb") as img:

                # sending message
                message = context.bot.send_photo(photo=img,
                                                 chat_id=update.effective_chat.id,
                                                 reply_markup=kb.inline_show)
            # if this point is reached, a valid file is found
            break

        # filename was invalid, passing exception
        except:
            pass  # trying next file

    # if no file was created in the last five days
    else:
        message = context.bot.send_message(
            text=f"Es ist kein aktueller Graph für {city} verfügbar.\n"
                 "Dies ist der Fall, wenn der Bot seit 5 Tagen keine neuen Daten mehr erhalten hat.\n"
                 "Bitte melden Sie diesen Vorfall auf GitHub:\nhttps://github.com/nonchris/covid-data-bot/issues",
            chat_id=update.effective_chat.id, reply_markup=kb.inline_show)

    return message


def bot_help(update, context):
    """Legacy help-command, new one is in inline_commands.py"""
    context.bot.send_message(
        text=f'Hallo, das hier sind alle verfügbaren Befehle:\n\n'
             '/abo - Öffnet ein Menü zur Auswahl gewünschter Abonnements.\n'
             'Erneutes Eingeben eines Befehls deabonniert die angegebene Kategorie.\n\n'

             '/zeig - Öffnet einen Dialog, in dem Sie den Graphen zu einer Region abrufen können.\n\n'
             'Die Auswahl innerhalb eines Dialoges ist über die Buttons unterhalb der gesendeten Nachricht möglich.\n\n'
             'Ihnen wird das Menü nicht angezeigt?\n'
             'Schreiben Sie dem Bot eine beliebige Nachricht und er sendet Ihnen ein neues Hauptmenü.\n'
             'Hervorgehoben Befehle und Felder unter Nachrichten sind klickbar.\n\n'
             'Bleiben Sie gesund!\n'
             'Corona Bot Kreis Ahrweiler', reply_markup=kb.inline_more, chat_id=update.effective_chat.id)


"""
Legacy main commands, which are still usable.
They all point to new inline keyboards
"""


def menu_menu(update, context):
    context.bot.send_message(text='Was möchten Sie als nächstes tun?',
                             reply_markup=kb.inline_menu, chat_id=update.effective_chat.id)


def menu_show(update, context):
    context.bot.send_message(text='Bitte wählen Sie eine Region.',
                             reply_markup=kb.inline_show, chat_id=update.effective_chat.id)


def menu_abo(update, context):
    context.bot.send_message(text='Bitte wählen Sie eine Region.',
                             reply_markup=kb.inline_sub, chat_id=update.effective_chat.id)


def caps(update, context):
    """
    Triggered on /caps
    """
    print(writer)
    text_caps = ' '.join(context.args).upper()
    print(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
