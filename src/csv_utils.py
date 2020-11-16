import time
import csv
import os


def str_to_bool(s: str):
    status = {"True": True,
                "False": False,}

    try:
        return status[s]
    except KeyError as e:
        #logging
        print("Error", e)
        return False

class ChatObject: 
    """Class that creates an object from csv entry"""
    
    def __init__(self, l: list):

        self.id = int(l[0])
        self.type = l[1]
        self.username = l[2]

        self.first_name = l[3]
        self.last_name = l[4]
        self.first_contact = l[5]

        self.settings = {
            "kreis": str_to_bool(l[6]),
            "adenau": str_to_bool(l[7]),
            "altenahr": str_to_bool(l[8]),
            "bad breisig": str_to_bool(l[9]),
            "brohltal": str_to_bool(l[10]),
            "grafschaft": str_to_bool(l[11]),
            "bad neuenahr-ahrweiler": str_to_bool(l[12]),
            "remagen": str_to_bool(l[13]),
            "sinzig": str_to_bool(l[14]),
            "all": str_to_bool(l[15]),
            }
        #logging



class Writer:
    """
    Handles all csv file accesses, like read /write /search
    - Hardcoded on telegram chat-objects
    """
    def __init__(self, file="data/chats.csv"):
        """
        takes filename
        """
        self.file = file
        self.file_check()
        self.entries = self.read()
        print(self.entries)
 

    def file_check(self):
        """checks if csv file exists, creates if not"""
        
        if os.path.isfile(self.file):
            None
        else:
            open(self.file, "w").close()
    
    def add(self, content) -> ChatObject:
        """
        Handles creation of new ChatObjects no created yet
        - Needs a telegram.chat object as input
        - Checks if object already exists
        - Creates new one of needed
        - returns ChatObject
        """
        #if entry already exists - breaking
        result = self.search_id(content["id"])
        if result:
            #print(result)
            return result[0]
        #logging new
        #getting content to write
        #keys for the telegram.chat object
        keys = ["id", "type", "username", "first_name", "last_name"]
        line = [] #will contain the row to add
        for key in keys: #going trough chat object
            line.append(f"{content[key]}")
        
        #adding time to entry
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        line.append(f"{t}")

        line.append(True) #seeting kreis subscription to True by default
        for x in range(9):
            line.append(False)

        new = ChatObject(line)

        self.entries.append(new)

        return new


    def read(self):
        """
        Reads a whole csv file 
        Returns a list filled with created 'ChatObject'
        """

        self.entries = [] #return list of objects
        with open(self.file, "r") as csvfile:
            read = csv.reader(csvfile, delimiter=';')
            for row in read:
                #appending ChatObject to list
                self.entries.append(ChatObject(row))
        
        #print("ENTRIES ", self.entries)
        return self.entries


    def search_id(self, entry: int):
        """Searches for a chat id in whole file"""

        results = []
        for chat in self.entries:
            if chat.id == entry:
                results.append(chat)
        return results


    def write(self):
        text = ""
        for c in self.entries:
            o = c.settings
            text += f"{c.id};{c.type};{c.username};{c.first_name};"
            text += f"{c.last_name};{c.first_contact};{o['kreis']};{o['adenau']};"
            text += f"{o['altenahr']};{o['bad breisig']};{o['brohltal']};{o['grafschaft']};"
            text += f"{o['bad neuenahr-ahrweiler']};{o['remagen']};{o['sinzig']};{o['all']};\n"

        with open(self.file, "w") as f:
            f.write(text)
