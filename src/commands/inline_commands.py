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

    query.edit_message_text(
        text="Berechnung der Daten\n---\n"
             "Aktuelle Fallzahlen:\n\n"
             "Die aktuellen Zahlen werden direkt aus den Pressemitteilungen auf der Website des Kreis Ahrweiler bezogen.\n"
             "Um die Veränderung zum Vortag zu erhalten, wird der neue Wert minus dem letzten veröffentlichten Wert gerechnet.\n"
             "In der Regel entspricht dies dem Wert des Vortages. Eine Lücke in den Daten wird durch das Auslassen der "
             "x-Achenbeschriftung dargestellt.\n\n"
             "Sollte ein Tag in den Daten fehlen wird der Unterschied zum letzten vorhandenen Tag berechnet.\n"
             "Dadurch ist der Anstieg an diesem Tag die Summe aus dem letzten und dem aktuellen Tag.\n"
             "Werden die Daten nachgereicht, passen sich alle Werte wieder an."
             "\n\n---\n\n"
             "Inzidenz:\n\n"
             "Es wird die ganz normale Formel zur Berchnung, der Inzidenz verwendet.\n"
             "Infizierte x 100000 / Einwohner\n\n"
             "Ein Abweichen von der offiziellen Angabe ist möglich. "
             "Dies liegt an der Verwendung verschiedener Einwohnerzahlen, sowie der Rundung des Inzidenzwertes.\n\n"

             "Die Einwohnerzahlen zur Berechnung werden vom Statistischen Landesamt RLP bezogen:\n"
             "https://infothek.statistik.rlp.de/MeineHeimat/index.aspx?id=102&l=2&g=07131&tp=1025\n"
             "https://infothek.statistik.rlp.de/MeineHeimat/content.aspx?id=101&l=1&g=07131&tp=2",
        reply_markup=kb.inline_more)


def about(query):
    """Displays 'about' information'"""

    query.edit_message_text(
        text='Dieser Bot ist ein Open Source Projekt.\n'
              'Das bedeutet, dass Sie den gesamten Quelltext online einsehen können.\n\n'
              'Das Projekt steht weder mit dem Kreis Ahrweiler '
              'noch mit einer anderen Behörde in Verbindung und ist für Sie völlig kostenlos.\n'
              'Für Richtigkeit und Vollständigkeit der Daten wird keine Haftung übernommen.\n\n'
              'Der offizielle Quellcode des Bots:\n'
              'https://github.com/nonchris/covid-data-bot\n\n'
              'Quelle der Daten:\n'
              'https://www.kreis-ahrweiler.de/presseaktuell.php',
        reply_markup=kb.inline_more,)


def bot_help(query):
    """The help command - now inline"""

    query.edit_message_text(
        text=f'Wählen Sie unter "Abonnieren" die Regionen aus, zu denen der Bot Ihnen automatisch neue Zahlen senden soll.\n'
        'Standardmäßig sind  keine Regionen abonniert.\n\n'
        'Unter "Graphen" können Sie jederzeit den neusten Graph zu einer Region abrufen.\n\n'
        '"Mehr" bietet Ihnen zusätzliche Informationen über den Bot.\n\n'
        'Mit dem Pfeil kommen Sie zurück ins Hauptmenü.\n\n'
        'Sollte der Bot Ihnen kein Menü anzeigen, schreiben Sie einfach etwas in den Chat, der Bot wird Ihnen ein neues '
        'Menü zusenden.\n\n'
        'Danke, dass Sie den Corona Bot Kreis Ahrweiler verwenden. \n\n'
        'Bleiben Sie gesund!\n',
        reply_markup=kb.inline_more)


def menu_show(query):
    """Displays show menu"""
    query.edit_message_text(reply_markup=kb.inline_show_soft,
                            text='Zu welcher Region möchten Sie den Graphen sehen?')


def menu_sub(query):
    """Displays main menu"""
    query.edit_message_text(reply_markup=kb.inline_sub_soft,
                            text='Welche Regionen möchten Sie abonnieren?\n'
                                 'Sobald neue Zahlen verfügbar sind, wird Ihnen die Grafik zu allen '
                                 'abonnierten Regionen geschickt.\n'
                                 'Durch erneutes Wählen einer Region deabonnieren Sie Updates.')


def soft_back(query):
    """Back command that edits message instead of sending a new one"""

    query.edit_message_text(reply_markup=kb.inline_menu,
                            text='Was möchten Sie als nächstes tun?')


def share(query):
    query.edit_message_text(reply_markup=kb.inline_more,
                            text='Tägliche Updates zu den Corona Fallzahlen im Kreis Ahrweiler:\n'
                            't.me/aw_covidbot')

def contact(query):
    query.edit_message_text(reply_markup=kb.inline_more,
                            text='Verbesserungsvorschläge und Fehler können Sie direkt auf GitHub äußern:\n'
                                 'https://github.com/nonchris/covid-data-bot/issues\n'
                                 'Ansonsten können Sie eine Mail an covidbot@nonchris.eu schreiben.')