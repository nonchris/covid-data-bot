def setup(wrtr):
    """passing csv access object to this file"""
    global writer
    writer = wrtr

def echo(update, context):
    """Happens when somebody writes something"""
    #print(update.message.from_user.username)
    #print(update.message.chat)
    #print(writer)
    #print("writing")
    #writer.add(update.message.chat)
    #print("written")
    context.bot.send_message(chat_id=update.effective_chat.id, text="That's cool!")