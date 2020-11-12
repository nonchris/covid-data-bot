import time
import csv
import os


def str_to_bool(s: str):
    status = {"True": True,
                "False": False}
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

        self.kreis = str_to_bool(l[6])
        self.adenau = str_to_bool(l[7])
        self.altenahr = str_to_bool(l[8])
        self.breisig = str_to_bool(l[9])
        self.brohltal = str_to_bool(l[10])
        self.grafschaft = str_to_bool(l[11])
        self.neuenahr = str_to_bool(l[12])
        self.remagen = str_to_bool(l[13])
        self.sinzig = str_to_bool(l[14])
        self.all = str_to_bool(l[15])
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
