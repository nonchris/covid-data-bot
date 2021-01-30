import datetime

from telegram import Update, CallbackQuery

import data_handling.utils as utils
import commands.keyboards as kb


def setup(wrtr):
    """passing csv access object to this"""
    global writer
    writer = wrtr

abo_text = "\
/abo_adenau \n/abo_altenahr \n/abo_breisig \n/abo_brohltal \n/abo_grafschaft\
\n/abo_bad_neuenahr_ahrweiler \n/abo_remagen \n/abo_sinzig \n\
/abo_alle\n"
    #/kreis\n-> Die aktuellsten Zahlen für den ganzen Kreis.\n\
    #Standardmäßig sind Sie nur für Updates zum gesamzen Kreis angemeldet.

#this secondary keyboard is needed to make the keyboard
#pop up dagain when user disabled the custom keyboard and /help won't appear

def start(update, context):
    """Command triggered at /start"""
    print(context.args)
    name = ""
    if (fname := update.message.chat.first_name):
        name = f"{fname} "
    if (lname := update.message.chat.last_name):
        name += f"{lname} "
    if not name:
        name = f"{update.message.chat.username} "

    context.bot.send_message(text=f"Hallo {name.strip()},\n\
dieser Bot kann Ihnen täglich ein Update senden, so bald es neue Zahlen gibt.\n\
Bitte nehmen Sie zur Kenntniss, dass es sich bei dem Bot um ein privates Projekt handelt.\n\
\n\
Mit freundlichen Grüßen und bleiben Sie gesund!\n\
Covid Update Bot", reply_markup=kb.menu_kb, chat_id=update.effective_chat.id)

    context.bot.send_message(chat_id=update.effective_chat.id,
text=f'Bitte wählen Sie aus den angegebenen Optionen aus, was Sie tun möchten.\n\
Wählen Sie die Regionen aus, zu denen Sie automatische Updates erhalten wollen:\n\
/abonnieren\n\
Lassen Sie sich einzelne Graphen anzeigen:\n\
/zeig_graph\n\
Zeigt Ihnen eine Liste von Befehlen an:\n\
/hilfe\n\
')
    writer.add(update.message.chat)


def help(update, context):
    """The help command"""
    context.bot.send_message(text=f'Hallo, \
das hier sind alle verfügbaren Befehle:\n\n\
/abo - Öffnet ein Menü zur Auswahl gewünschter Abonnements.\n\
Erneutes Eingeben eines Befehls deabonniert die angegebene Kategorie.\n\n\
\
/zeig - Öffnet einen Dialog, in dem Sie den Graphen zu einer Region abrufen können.\n\
\n\
Jeden Befehl, den Sie in einem Dialog finden, können Sie auch von Hand eingeben.\n\n\
Ihnen wird das Menü nicht angezeigt?\n\
Nutzen Sie /menu\n\
Sie können zwischen Bot-Tatstur und normaler Tatstur mit einer Schaltfläche \
in der Text-Zeile hin und her wechseln.\n\
Hervorgehoben Befehle sind zudem klickbar.\n\n\
Bleiben Sie gesund!\n\
Corona Bot Kreis Ahrweiler', reply_markup=kb.inline_more, chat_id=update.effective_chat.id)


def menu_menu(update, context):
    context.bot.send_message(text='Was möchten Sie als nächstes tun?',
                             reply_markup=kb.inline_menu, chat_id=update.effective_chat.id)


def menu_show(update, context):
    context.bot.send_message(text='Bitte wählen Sie eine Region.',
                             reply_markup=kb.inline_show, chat_id=update.effective_chat.id)


def menu_abo(update, context):
    context.bot.send_message(text='Bitte wählen Sie eine Region.',
                             reply_markup=kb.inline_sub, chat_id=update.effective_chat.id)


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


def show(update, context, city='', query=None):

    # if query:
    #     query.delete_message()
    #getting word that actually triggerd that command
    #using the mapping dict from csv_utils
    if city == '':
        city = utils.translator[update['message']['text'][1:].lower()]

    #actual part for getting and sending the graph
    today = datetime.date.today()
    #used to go trough the last five possible filenames
    # -> if a day has no data yet, the bot will search his "archive"
    for i in range(5): 
        try: #trying to open a filename
            date = today - datetime.timedelta(i)
            path = f"visuals/{city}-{date}.png"
            print(path)
            with open(path, "rb") as img:

                message = context.bot.send_photo(photo=img, chat_id=update.effective_chat.id,
                                                 reply_markup=kb.inline_show)
            break #if this point is reached, a valid file is found
        except:
            pass #trying next file
    #if no file was created in the last five days
    else:
        message = context.bot.send_message(text=f"Es ist kein aktueller Graph für {city} verfügbar.\n\
Sind sie sicher, dass Sie eine gültige Region eigegeben haben? - \
Die Schlüsselwörter sind die selben, die Sie zum abonnieren verwenden. \n\
Nutzen Sie /help für mehr Informationen", chat_id=update.effective_chat.id, reply_markup=kb.inline_show)

    return message

def methods(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=kb.menu_kb,
                             text="Aktuelle Fallzahlen:\n\n\
Die aktuellen Zahlen werden von der Website des Kreis Ahrweiler bezogen.\n\
Um die Veränderung zum Vortag zu erhalten, wird der neue Wert minus dem letzten verfügbaren Wert gerechnet.\
In der Regel entspricht dies dem Wert des Vortags. Eine Lücke in den Daten wird visuell dargestellt.\n\
\n\n\
Inzidenz:\n\n\
Es wird die ganz normale Formel zur Berchnung, der Inzidenz verwendet.\n\
Infizierte x 100000 / Einwohner\n\
Mehr Informationen zur Berechnung, Rechenfehlern und Abweichungen finden Sie hier:\n\
https://github.com/nonchris/covid-data-bot/pull/12\n\n\
Mehr über den Bot: /about")

def about(update, context):
    context.bot.send_message(text='Dieser Bot ist ein Open Source Projekt.\n\
Das bedeutet, dass Sie den gesamten Quelltext online einsehen können.\n\
Dieses Projekt steht weder mit dem Kreis Ahrweiler, \
noch einer anderen Behörde in Verbindung.\n\
Für Richtigkeit und Vollständigkeit der Daten wird keine Haftung übernommen.\n\
https://github.com/nonchris/covid-data-bot', \
                             chat_id=update.effective_chat.id, reply_markup=kb.menu_kb)

def caps(update, context):
    """
    Triggered on /caps
    """
    print(writer)
    text_caps = ' '.join(context.args).upper()
    print(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)