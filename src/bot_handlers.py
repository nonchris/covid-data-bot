import csv_utils

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
aktuell sind Auswertungen nur für Sinzig möglich.\n\
Ich werde täglich ein Update schicken, so bald es neue Zahlen gibt.\n\
Bitte nehmen Sie zur Kenntniss, dass es sich bei mir um ein privates \
Projekt handelt und ich mich noch in der Entwicklung befinde.\n\
Um mehr Optionen zu erhalten, nutzen Sie bitte /hilfe.\b\
Mit freundlichen Grüßen und bleiben Sie gesund!\n\
Corona Bot Kreis Ahrweiler", chat_id=update.effective_chat.id)


def help(update, context):
    """The help command"""
    context.bot.send_message(text=f"Hi, \
das hier sind alle verfügbaren Befehle:\n\
Mit den folgenden Commands können Sie sich für einzelne Updates anmelden:\n\
/adenau \n/altenahr \n/breisig \n/brohltal \n/grafschaft \n/neuenahr \n\
/remagen \n/sinzig \n\
/kreis\n-> Die aktuellsten Zahlen für den ganzen Kreis.\n\
/alle\n-> Aboniert alle einzeln aufgeführten Updates mit nur einem Klick.\n\n\
Sie können auf die blau hervorgehobenen Befehle draufklicken, oder diese manuell in \
diesen Chat schicken, um den Befehl einzugeben.\n\
Durch erneutes Eingeben eines Befehls deabonieren Sie die angegebene Kategorie.\n\n\
Standardmäßig sind Sie nur für Updates zum gesamzen Kreis angemeldet.\n\
Bleiben Sie gesund!\n\
Corona Bot Kreis Ahrweiler", chat_id=update.effective_chat.id)


def caps(update, context):
    """
    Triggered on /caps
    """
    print(writer)
    text_caps = ' '.join(context.args).upper()
    print(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)