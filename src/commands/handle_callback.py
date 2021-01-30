import logging
import traceback

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import commands.commands as commands
import commands.inline_commands as incom
from data_handling.utils import translator


def handle_callback(update: Update, context: CallbackContext):
    """
    Handles all callbacks from inline commands

    :param update: Telegram Update Object
    :param context: Telegram CallbackContext Object

    - Commands are mapped in a central dict
    - The received query.data string is the key to find the command\n
    Commands can rely on callback-query on context, update and other optional params.\n

    Given callbacks can contain certain extra keywords to trigger extra operations.\n
    Control flow is achieved by using a callback string that can contain certain prefixes that call for
    action before the actual command is mentioned.\n
    The callback string will be sliced during this process.

    :returns: None
    """

    command_switch = {
        'back': commands.menu_menu,
        'show': commands.show,
        'sub': commands.subscribe,

        'methods': incom.methods,
        'about': incom.about,
        'more': incom.menu_more,
        'help': incom.bot_help,
        'menu_show': incom.menu_show,
        'menu_sub': incom.menu_sub,
        'softback': incom.soft_back,
    }

    # extracting callback object
    query = update.callback_query
    query.answer()
    key = query.data

    # clear at the start of callback is the symbol to clear the inline keyboard
    # this is triggered when a new message will be sent so the chat is more clean
    # used in show/ subscription and 'back' commands
    if key.startswith('clear'):
        print("clearing", key)
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[]]))
        key = key.replace('clear', '')

    # catching show command because it needs a special input
    if key.startswith('show'):
        command_switch['show'](update, context, city=translator[key.replace('show', '')])

    # catching sub commands because it needs a special input
    elif key.startswith('sub'):
        command_switch['sub'](update, query, translator[key.replace('sub', '')])

    # all other commands are 'normal'
    else:
        # trying to get matching key for query
        try:
            # trying to extract command
            command = command_switch[key]

            # check if command belongs to inline commands
            if command.__module__ == 'commands.inline_commands':
                command(query)

            # must be a command that sends a new message
            else:
                command(update, context)

        # if we fail to extract the key
        except KeyError:
            logging.error(f"CAN'T FIND COMMAND {key} IN COMMAND_SWITCH\n{traceback.format_exc()}")
            print(f'{key} was NOT listed!')
