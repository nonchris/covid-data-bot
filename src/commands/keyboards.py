from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

menu_kb = ReplyKeyboardMarkup([
                    ['/abonnieren'], ['/zeig_graph'], ['/hilfe', '/about', '/methods'] \
                    ], one_time_keyboard=False)
menu2_kb = ReplyKeyboardMarkup([
                    ['/abonnieren'], ['/zeig_graph'], ['/mehr'] \
                    ], one_time_keyboard=False)
show_kb = ReplyKeyboardMarkup([
                    ['/Adenau', '/Altenahr', '/Bad_Breisig'], \
                    ['/Brohltal', '/Grafschaft', '/Remagen'],\
                    ['/Sinzig', '/Bad_Neuenahr_Ahrweiler'] \
                    ], one_time_keyboard=True)
abo_kb = ReplyKeyboardMarkup([
    ['/abo_adenau', '/abo_altenahr', '/abo_brohltal'],
    ['/abo_grafschaft', '/abo_remagen', '/abo_sinzig'],
    ['/abo_alle', '/abo_bad_breisig'],
    ['/abo_bad_neuenahr_ahrweiler',]
    ], one_time_keyboard=True)
