import csv_utils

def setup(wrtr):
    """passing csv access object to this"""
    global writer
    writer = wrtr

def kreis(update, context):
    chat = writer.add(update.message.chat)
    if chat.kreis:
        chat.kreis = False
        context.bot.send_message(text="Sie haben sich aus Updates für den Kreis Ahrweiler ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        chat.kreis = True
        context.bot.send_message(text="Sie haben Updates für den Kreis Ahrweiler aboniert",
                chat_id=update.effective_chat.id)

def adenau(update, context):
    chat = writer.add(update.message.chat)
    print("adenau: ", chat.adenau)
    if chat.adenau:
        chat.adenau = False
        print("adenau: ", chat.adenau)
        context.bot.send_message(text="Sie haben sich aus Updates für Adenau ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        chat.adenau = True
        print("adenau: ", chat.adenau)
        context.bot.send_message(text="Sie haben Updates für Adenau aboniert",
                chat_id=update.effective_chat.id)
        writer.write()

def altenahr(update, context):
    chat = writer.add(update.message.chat)
    if chat.altenahr:
        chat.altenahr = False
        context.bot.send_message(text="Sie haben sich aus Updates für Altenahr ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        chat.altenahr = True
        context.bot.send_message(text="Sie haben Updates für Altenahr aboniert",
                chat_id=update.effective_chat.id)

def breisig(update, context):
    chat = writer.add(update.message.chat)
    if chat.breisig:
        chat.adenau = False
        context.bot.send_message(text="Sie haben sich aus Updates für Bad Breisig ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        chat.breisig = True
        context.bot.send_message(text="Sie haben Updates für Bad Breisig aboniert",
                chat_id=update.effective_chat.id)

def brohltal(update, context):
    chat = writer.add(update.message.chat)
    if chat.brohltal:
        chat.brohltal = False
        context.bot.send_message(text="Sie haben sich aus Updates für das Brohltal ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        chat.brohltal = True
        context.bot.send_message(text="Sie haben Updates für das Brohltal aboniert",
                chat_id=update.effective_chat.id)

def grafschaft(update, context):
    chat = writer.add(update.message.chat)
    if chat.grafschaft:
        chat.grafschaft = False
        context.bot.send_message(text="Sie haben sich aus Updates für die Grafschaft ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        chat.grafschaft = True
        context.bot.send_message(text="Sie haben Updates für die Grafschaft aboniert",
                chat_id=update.effective_chat.id)

def neuenahr(update, context):
    chat = writer.add(update.message.chat)
    if chat.neuenahr:
        chat.neuenahr = False
        context.bot.send_message(text="Sie haben sich aus Updates für Bad Neuenahr-Ahrweiler ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        chat.neuenahr = True
        context.bot.send_message(text="Sie haben Updates für Bad Neuenahr-Ahrweiler aboniert",
                chat_id=update.effective_chat.id)

def remagen(update, context):
    chat = writer.add(update.message.chat)
    if chat.remagen:
        chat.remagen = False
        context.bot.send_message(text="Sie haben sich aus Updates für Remagen ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        chat.remagen = True
        context.bot.send_message(text="Sie haben Updates für Remagen aboniert",
                chat_id=update.effective_chat.id)


def sinzig(update, context):
    #csv_utils.write(str(update.message.chat.id), "sinzig")
    chat = writer.add(update.message.chat)
    print("sinzig: ", chat.sinzig)

    if chat.sinzig:
        chat.sinzig = False
        print("sinzig: ", chat.sinzig)
        context.bot.send_message(text="Sie haben sich aus Updates für Sinzig ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        chat.sinzig = True
        print("sinzig: ", chat.sinzig)
        context.bot.send_message(text="Sie haben Updates für Sinzig aboniert",
                chat_id=update.effective_chat.id)
        #writer.write()
    print()

def alle(update, context):
    chat = writer.add(update.message.chat)
    if chat.all:
        chat.all = False
        context.bot.send_message(text="Sie haben sich aus alles umfassenden Updater ausgetragen, \
es gelten wieder Ihre Einstellungen für einzelne Abos.",
                chat_id=update.effective_chat.id)
    else:
        chat.all = True
        context.bot.send_message(text="Sie werden alle Updates erhalten, \
Ihre aktuellen Abo Einstellungen werden ignoriert.",
                chat_id=update.effective_chat.id)