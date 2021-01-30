import commands.keyboards as kb

"""
File containing all inline-commands the bot can execute
Those commands will be called from handle_callback.py 
Some of those commands are 'inline-duplicates' from 'normal' commands in commands.py 
"""


def menu_more(query):
    """Updates message and menu the 'more' sub-menu"""

    query.edit_message_text(text=f"Weitere Optionen", reply_markup=kb.inline_more)


def methods(query):
    """Displays information about the used calculation methods"""

    query.edit_message_text(reply_markup=kb.inline_more, text='Aktuelle Fallzahlen:\n\n\
Die aktuellen Zahlen werden von der Website des Kreis Ahrweiler bezogen.\n\
Um die Veränderung zum Vortag zu erhalten, wird der neue Wert minus dem letzten verfügbaren Wert gerechnet.\
In der Regel entspricht dies dem Wert des Vortags. Eine Lücke in den Daten wird visuell dargestellt.\n\
\n\n\
Inzidenz:\n\n\
Es wird die ganz normale Formel zur Berchnung, der Inzidenz verwendet.\n\
Infizierte x 100000 / Einwohner\n\
Mehr Informationen zur Berechnung, Rechenfehlern und Abweichungen finden Sie hier:\n\
https://github.com/nonchris/covid-data-bot/pull/12\n\n\
Mehr zu dem Bot erfahren Sie unter "Über den Bot"')


def about(query):
    """Displays 'about' information'"""

    query.edit_message_text(reply_markup=kb.inline_more, text='Dieser Bot ist ein Open Source Projekt.\n\
Das bedeutet, dass Sie den gesamten Quelltext online einsehen können.\n\n\
Das Projekt steht weder mit dem Kreis Ahrweiler, \
noch mit einer anderen Behörde in Verbindung und ist für Sie völlig kostenlos.\n\
Für Richtigkeit und Vollständigkeit der Daten wird keine Haftung übernommen.\n\
Der offizielle Quellcode des Bots:\n\
https://github.com/nonchris/covid-data-bot')


def bot_help(query):
    """The help command - now inline"""

    query.edit_message_text(reply_markup=kb.inline_more,
    text=f'Wählen Sie unter "Abonnieren" die Regionen aus, zu denen der Bot Ihnen automatisch neue Zahlen senden soll.\n\
Standardmäßig sind  keine Regionen abonniert.\n\n\
Unter "Graphen" können Sie jederzeit den neusten Graph zu einer Region abrufen.\n\n\
"Mehr" bietet Ihnen zusätzliche Informationen über den Bot.\n\n\
Mit dem Pfeil kommen Sie zurück ins Hauptmenü.\n\n\
Sollte der Bot Ihnen kein Menü anzeigen, schreiben Sie einfach etwas in den Chat, der Bot wird Ihnen ein neues \
Menü zusenden.\n\n\
Danke, dass Sie den Corona Bot Kreis Ahrweiler verwenden. \n\n\
Bleiben Sie gesund!\n\
')


def menu_show(query):
    """Displays main menu"""

    print(kb.inline_show_soft)
    print("eyy")
    query.edit_message_text(text='Zu welcher Region möchten Sie den Graphen sehen?',
                            reply_markup=kb.inline_show_soft)


def soft_back(query):
    """Back command that edits message instead of sending a new one"""

    query.edit_message_text(text='Was möchten Sie als nächstes tun?',
                            reply_markup=kb.inline_menu)
