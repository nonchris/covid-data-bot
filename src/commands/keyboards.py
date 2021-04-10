import copy
from typing import List, Tuple

from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import data_handling.utils as utils

"""
File containing old keyboard markups and new inline-keyboards
"""

# Standard Keyboards
menu_kb = ReplyKeyboardMarkup([
    ['/abonnieren'], ['/zeig_graph'], ['/hilfe']
], one_time_keyboard=False)

menu2_kb = ReplyKeyboardMarkup([
    ['/abonnieren'], ['/zeig_graph'], ['/mehr']
], one_time_keyboard=False)

show_kb = ReplyKeyboardMarkup([
    ['/Adenau', '/Altenahr', '/Bad_Breisig'],
    ['/Brohltal', '/Grafschaft', '/Remagen'],
    ['/Sinzig', '/Bad_Neuenahr_Ahrweiler']
], one_time_keyboard=True)

abo_kb = ReplyKeyboardMarkup([
    ['/abo_adenau', '/abo_altenahr', '/abo_brohltal'],
    ['/abo_grafschaft', '/abo_remagen', '/abo_sinzig'],
    ['/abo_alle', '/abo_bad_breisig'],
    ['/abo_bad_neuenahr_ahrweiler', ]
], one_time_keyboard=True)

# Inline Keyboards
"""
Syntactic keyword scheme:
General
- clear: triggers the removal of the inline keyboard on the previous message
-> can be used in front of every callback 

- soft: no new created message, editing message instead

For special methods
- show: keyword to access show method 
- sub: keyword to access subscription method

The whole callback string does not contain spaces or other 'spacers'
"""

# different buttons for going a menu up - symbol used is the 'left arrow' emoji

# this is the 'normal' back button which will just trigger a new menu-message
back_button = InlineKeyboardButton(u'\u2B05', callback_data='back')

# soft back button that triggers an edit of the message and inline-keyboard - no new message
back_button_soft = InlineKeyboardButton(u'\u2B05', callback_data='softback')

# sends a new message but issues the removal of the inline keyboard of the previous message
back_button_clear = InlineKeyboardButton(u'\u2B05', callback_data='clearback')


def gen_city_menu(prefix: str) -> Tuple[List[List[InlineKeyboardButton]], List[List[InlineKeyboardButton]]]:
    """
    Function generating city-keyboards

    :param prefix: prefix that is scanned for in handle_callback

    - Generates list of InlineButtons from a list (located in utils)
    - Splits this list in lists of three objects
    - Builds nested list of keyboards buttons
    - It also inserts a 'back button' at the first position

    :returns: Tuple of two lists: First with 'clear back button', second with 'soft/ inline back button'
    """

    # converting city list to list of buttons - doing some adjustments to callback parameters
    buttons = [InlineKeyboardButton(city, callback_data=prefix + city.replace(' ', '_').lower()) for city in
               utils.city_list]

    # inserting hard back-button
    buttons.insert(0, back_button_clear)

    arranged_buttons = []  # for the final nested list
    row = []  # holds each row
    for i in range(len(buttons)):
        # building list of three objects
        if i % 3 != 0 or i == 0:
            row.append(buttons[i])

        # if line contains three buttons
        else:
            arranged_buttons.append(copy.deepcopy(row))  # appending row
            row.clear()  # clearing
            row.append(buttons[i])  # appending next button

    # appending last row that wasn't caught because it isn't filled up
    arranged_buttons.append(row)

    # replacing hard button with soft one
    soft_version = copy.deepcopy(arranged_buttons.copy())
    soft_version[0][0] = back_button_soft

    return arranged_buttons, soft_version


# main menu
inline_menu = InlineKeyboardMarkup([[InlineKeyboardButton('Abonnieren', callback_data='menu_sub'),
                                     InlineKeyboardButton('Graphen', callback_data='menu_show'),
                                     InlineKeyboardButton('Mehr', callback_data='more')],
                                    [InlineKeyboardButton('Übersicht der DRK Teststellen',
                                                          url='www.kv-aw.drk.de/corona-schnelltest')]])

# start menu - same as above just with other labeled 'more button'
inline_start = InlineKeyboardMarkup([[InlineKeyboardButton('Abonnieren', callback_data='menu_sub'),
                                     InlineKeyboardButton('Graphen', callback_data='menu_show'),
                                     InlineKeyboardButton('Hilfe', callback_data='more')]])

# more menu
inline_more = InlineKeyboardMarkup([[back_button_soft,
                                     InlineKeyboardButton('Hilfe', callback_data='help'),
                                     InlineKeyboardButton('Über Bot', callback_data='about'),
                                     InlineKeyboardButton('Kontakt', callback_data='contact')],
                                    [InlineKeyboardButton('Infos zur Berechnung', callback_data='methods'),
                                     InlineKeyboardButton('Teilen', callback_data='share')],
                                    [InlineKeyboardButton('Teststellen in der Umgebung', callback_data='test_centers')]])

# menu for showing graphs
_inline_show, _inline_show_soft = gen_city_menu('clearshow')
inline_show, inline_show_soft = InlineKeyboardMarkup(_inline_show), InlineKeyboardMarkup(_inline_show_soft)

# menu for subscribing
_inline_sub, _inline_sub_soft = gen_city_menu('sub')
inline_sub, inline_sub_soft = InlineKeyboardMarkup(_inline_sub), InlineKeyboardMarkup(_inline_sub_soft)
