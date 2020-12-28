import os
import logging

from telegram import error

def setup(wrtr):
    """passing csv access object to this"""
    global writer
    writer = wrtr

def notify_all(update, context):
    """A command for the host to send notifications to all subscribers"""
    if str(update.message.chat.username) == os.environ["OWNER_USERNAME"]:
        message = update.message.text.replace("/notify ", "") #removing command
        feedback = send_to_all(context.bot, message) #sending to all
        context.bot.send_message(text=feedback, chat_id=update.effective_chat.id) #feedback for admin

def send_to_all(bot, message: str) -> str:
    """A slim dispatcher, that sends a text to all registered subscribers"""
    attempts = 0 #counts each iteration
    blocked = 0 #counts fails which are probably blocks
    for chat in writer.entries:
        attempts += 1
        logging.info("SENDING notification to all")
        #try to send message
        try:
            bot.send_message(text=message, chat_id=chat.id)
        except error.Unauthorized:
            blocked += 1
    feedback = f"Reached {attempts-blocked} of {attempts} subscribers"
    logging.info(feedback)
    return feedback