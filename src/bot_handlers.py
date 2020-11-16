import csv_utils
import datetime

def setup(wrtr):
    """passing csv access object to this"""
    global writer
    writer = wrtr

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
Bitte nehmen Sie zur Kenntniss, dass es sich bei dem Bot um ein privates \
Projekt handelt, welches strtig weiterentwickelt wird.\n\
Um mehr Optionen zu erhalten, nutzen Sie bitte /hilfe.\n\
Mit freundlichen Grüßen und bleiben Sie gesund!\n\
Covid Update Bot", chat_id=update.effective_chat.id)


def help(update, context):
    """The help command"""
    context.bot.send_message(text=f"Hallo, \
das hier sind alle verfügbaren Befehle:\n\
Mit den folgenden Befehlen können Sie automatische Updates zu bestimmten \
Regionen erhalten, sobald neue Zahlen verfügbar sind:\n\
/adenau \n/altenahr \n/breisig \n/brohltal \n/grafschaft \n/neuenahr \n\
/remagen \n/sinzig \n\
/alle\n-> Abonniert alle einzeln aufgeführten Updates mit nur einem Klick.\n\n\
Sie können auf die hervorgehobenen Befehle draufklicken, oder diese manuell in \
diesen Chat schicken, um den Befehl einzugeben.\n\
Durch erneutes Eingeben eines Befehls deabonnieren Sie die angegebene Kategorie.\n\n\
\
/show Schlüsselwort oder /sh Schlüsselwort\n \
-> Ruft den aktuellsten Graphen für diese Region ab.\n \
Die Schlüsselwörter sind die oben hervorgehobenen Worte.\n\
Beispiel: '/sh breisig' ruft den Graphen für Bad Breisig ab.\n \
\n\n\
Bleiben Sie gesund!\n\
Corona Bot Kreis Ahrweiler", chat_id=update.effective_chat.id)
    #/kreis\n-> Die aktuellsten Zahlen für den ganzen Kreis.\n\
    #Standardmäßig sind Sie nur für Updates zum gesamzen Kreis angemeldet.


def show(update, context):
    city = ""
    try:
        #trying to get a valid keyword from args
        #the word must be precise otherwise the filename will be faulty
        #using the mapping dict from csv_utils
        city = csv_utils.translator[" ".join(context.args).replace('/', '').lower()]

    #if no valid input was given
    except KeyError as ke:
        context.bot.send_message(text="Geben Sie bitte ein gültiges Schlüsselwort ein.\n\
Die Schlüsselwörter sind die selben, die Sie zum abonnieren verwenden. \n\
Nutzen Sie /help für mehr Informationen.", chat_id=update.effective_chat.id)
        return
    
    #actual part for getting and sending the graph
    today = datetime.date.today()
    #used to go trough the last five possible filenames
    # -> if a day has no data yet, the bot will search his "archive"
    for i in range(5): 
        try: #trying to open a filename
            date = today - datetime.timedelta(i)
            path = f"visuals/{city}-{date}.png"
            with open(path, "rb") as img:
                context.bot.send_photo(photo=img, chat_id=update.effective_chat.id)
            break #if this point is reached, a valid file is found
        except:
            pass #trying next file
    #if no file was created in the last five days
    else:
        context.bot.send_message(text=f"Es ist kein aktueller Graph für {city} verfügbar.\n \
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