import csv_utils

def setup(wrtr):
    """passing csv access object to this"""
    global writer
    writer = wrtr

def kreis(update, context):
    chat = writer.add(update.message.chat)
    s = chat.settings
    if s["kreis"]:
        s["kreis"] = False
        context.bot.send_message(text="Sie haben sich aus Updates für den Kreis Ahrweiler ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        s["kreis"] = True
        context.bot.send_message(text="Sie haben Updates für den Kreis Ahrweiler aboniert",
                chat_id=update.effective_chat.id)
    writer.write()

def adenau(update, context):
    chat = writer.add(update.message.chat)
    s = chat.settings
    if s["adenau"]:
        s["adenau"] = False
        context.bot.send_message(text="Sie haben sich aus Updates für Adenau ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        s["adenau"] = True
        context.bot.send_message(text="Sie haben Updates für Adenau aboniert",
                chat_id=update.effective_chat.id)
        writer.write()
    writer.write()

def altenahr(update, context):
    chat = writer.add(update.message.chat)
    s = chat.settings
    if s["altenahr"]:
        s["altenahr"] = False
        context.bot.send_message(text="Sie haben sich aus Updates für Altenahr ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        s["altenahr"] = True
        context.bot.send_message(text="Sie haben Updates für Altenahr aboniert",
                chat_id=update.effective_chat.id)
    writer.write()

def breisig(update, context):
    chat = writer.add(update.message.chat)
    s = chat.settings
    if s["bad breisig"]:
        s["bad breisig"] = False
        context.bot.send_message(text="Sie haben sich aus Updates für Bad Breisig ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        s["bad breisig"] = True
        context.bot.send_message(text="Sie haben Updates für Bad Breisig aboniert",
                chat_id=update.effective_chat.id)
    writer.write()

def brohltal(update, context):
    chat = writer.add(update.message.chat)
    s = chat.settings
    if s["brohltal"]:
        s["brohltal"] = False
        context.bot.send_message(text="Sie haben sich aus Updates für das Brohltal ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        s["brohltal"] = True
        context.bot.send_message(text="Sie haben Updates für das Brohltal aboniert",
                chat_id=update.effective_chat.id)
    writer.write()

def grafschaft(update, context):
    chat = writer.add(update.message.chat)
    s = chat.settings
    if s["grafschaft"]:
        s["grafschaft"] = False
        context.bot.send_message(text="Sie haben sich aus Updates für die Grafschaft ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        s["grafschaft"] = True
        context.bot.send_message(text="Sie haben Updates für die Grafschaft aboniert",
                chat_id=update.effective_chat.id)
    writer.write()

def neuenahr(update, context):
    chat = writer.add(update.message.chat)
    s = chat.settings
    if s["bad neuenahr-ahrweiler"]:
        s["bad neuenahr-ahrweiler"] = False
        context.bot.send_message(text="Sie haben sich aus Updates für Bad Neuenahr-Ahrweiler ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        s["bad neuenahr-ahrweiler"] = True
        context.bot.send_message(text="Sie haben Updates für Bad Neuenahr-Ahrweiler aboniert",
                chat_id=update.effective_chat.id)
    writer.write()

def remagen(update, context):
    chat = writer.add(update.message.chat)
    s = chat.settings
    if s["remagen"]:
        s["remagen"] = False
        context.bot.send_message(text="Sie haben sich aus Updates für Remagen ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        s["remagen"] = True
        context.bot.send_message(text="Sie haben Updates für Remagen aboniert",
                chat_id=update.effective_chat.id)
    writer.write()

def sinzig(update, context):
    #csv_utils.write(str(update.message.chat.id), "sinzig")
    chat = writer.add(update.message.chat)
    s = chat.settings
    print("sinzig: ", s["sinzig"])

    if s["sinzig"]:
        s["sinzig"] = False
        print("sinzig: ", s["sinzig"])
        context.bot.send_message(text="Sie haben sich aus Updates für Sinzig ausgetragen",
                chat_id=update.effective_chat.id)
    else:
        s["sinzig"] = True
        print("sinzig: ", s["sinzig"])
        context.bot.send_message(text="Sie haben Updates für Sinzig aboniert",
                chat_id=update.effective_chat.id)
        #writer.write()
    writer.write()
    print()

def alle(update, context):
    chat = writer.add(update.message.chat)
    s = chat.settings
    if s["all"]:
        s["all"] = False
        context.bot.send_message(text="Sie haben sich aus alles umfassenden Updater ausgetragen, \
es gelten wieder Ihre Einstellungen für einzelne Abos.",
                chat_id=update.effective_chat.id)
    else:
        s["all"] = True
        context.bot.send_message(text="Sie werden alle Updates erhalten, \
Ihre aktuellen Abo Einstellungen werden ignoriert.",
                chat_id=update.effective_chat.id)
    writer.write()