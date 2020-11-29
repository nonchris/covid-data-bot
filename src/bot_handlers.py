import csv_utils
import datetime

def setup(wrtr):
    """passing csv access object to this"""
    global writer
    writer = wrtr

abo_text = "\
/abo_adenau \n/abo_ahrweiler \n/abo_altenahr \n/abo_breisig \n/abo_brohltal \n/abo_grafschaft\
\n/abo_neuenahr \n/abo_remagen \n/abo_sinzig \n\
/abo_alle\n"
    #/kreis\n-> Die aktuellsten Zahlen für den ganzen Kreis.\n\
    #Standardmäßig sind Sie nur für Updates zum gesamzen Kreis angemeldet.

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
Covid Update Bot", chat_id=update.effective_chat.id)

    context.bot.send_message(chat_id=update.effective_chat.id,
text=f'Wählen Sie die Regionen, über die Sie täglich informiert werden möchten:\n\
{abo_text}\
Bad Neuenahr und Ahrweiler versenden die selbe Grafik. \n\
Nutzen Sie /hilfe für weitere Optionen.\n\
Alle Befehle sind klickbar.\n')


def help(update, context):
    """The help command"""
    context.bot.send_message(text=f'Hallo, \
das hier sind alle verfügbaren Befehle:\n\n\
Befehle um automatische Updates zu gewählten \
Regionen zu erhalten, sobald neue Zahlen verfügbar sind:\n\
{abo_text}\
Abo_alle abonniert alle Updates mit nur einem Klick.\n\n\
Bad Neuenahr und Ahrweiler versenden die selbe Grafik. \n\
Durch erneutes Eingeben eines Befehls deabonnieren Sie die angegebene Kategorie.\n\n\
\
Graphen für eine Region abrufen:\n\
/zeig Region - kurz: /z\n\
Die Regionen sind die Namen aus den oben gelisteten Abo-Befehlen.\n\
Beispiel: /z breisig\n\n\
Sie können die hervorgehobenen Befehle anklicken, oder diese in \
den Chat eingeben, um den Befehl auszuführen.\n\n\
Bleiben Sie gesund!\n\
Corona Bot Kreis Ahrweiler', chat_id=update.effective_chat.id)



def show(update, context):
    city = ""
    #getting word that actually triggerd that command
    #using the mapping dict from csv_utils
    city = csv_utils.translator[update['message']['text'][1:].lower()]
    
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
                context.bot.send_photo(photo=img, chat_id=update.effective_chat.id)
            break #if this point is reached, a valid file is found
        except:
            pass #trying next file
    #if no file was created in the last five days
    else:
        context.bot.send_message(text=f"Es ist kein aktueller Graph für {city} verfügbar.\n\
Sind sie sicher, dass Sie eine gültige Region eigegeben haben? - \
Die Schlüsselwörter sind die selben, die Sie zum abonnieren verwenden. \n\
Nutzen Sie /help für mehr Informationen", chat_id=update.effective_chat.id)


def caps(update, context):
    """
    Triggered on /caps
    """
    print(writer)
    text_caps = ' '.join(context.args).upper()
    print(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)