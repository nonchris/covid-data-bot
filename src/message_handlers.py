def setup(wrtr):
    """passing csv access object to this file"""
    global writer
    writer = wrtr

def echo(update, context):
    """Happens when somebody writes something"""
    context.bot.send_message(chat_id=update.effective_chat.id, \
        text="Nutzen Sie /help oder /h und /start, um mehr zu über den Bot zu erfahren.")