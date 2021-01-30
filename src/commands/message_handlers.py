from commands.keyboards import menu2_kb
import commands.keyboards as kb

def setup(wrtr):
    """passing csv access object to this file"""
    global writer
    writer = wrtr


def echo(update, context):
    """Happens when somebody writes something"""
    context.bot.send_message(text='Was möchten Sie machen?\n\
            /abo   /zeig   /hilfe',
                             reply_markup=kb.inline_menu, chat_id=update.effective_chat.id)
