import re
import csv
import time
import datetime
import json
import logging
import traceback

import requests 

class Requester:
    def __init__(self, link: str):
        """
        Getting data and triggering write processes
        """

        #downloading data
        self.content = requests.get(link)
        self.success = False #will be True when fresh data is loaded
        if self.content.status_code == 200: #check if request worked

            self.text = self.content.text

            
            self.success = self.prepare_data() #preparing data (for json) - returns True/ False
            #write json to file
            #write_raw needs a date - the date is first collected in write_json()
            if self.success:
                self.write_json()
                self.write_raw() #writing pure request text


        else:
            logging.error(f"Error getting page, [Status Code: {self.content.status_code}]")

    def get_date(self, date):
        """
        Getting date as day.month.year - getting datetime object
        """
        date_parts = date.split(".")
        day = int(date_parts[0])
        month = int(date_parts[1])
        year = int(date_parts[2])
        return datetime.date(year, month, day)

    def date_check(self, date):
        """
        Check to make sure that downloaded data is updated and not from yesterday
        """
        if date == datetime.date.today():   
            return True
        
        else:
            return False

    def get_filename(self):
        """
        Building filename
        """
        self.filename = f"data/ahrweiler-{self.date}.json"
        self.raw_filename = f"data/ahrweiler-{self.date}_raw.txt"


    def write_raw(self):
        """
        Writing the pure request to a file for later data handling
        There is no filename if write_json() failed if this happens
        raw data will be saved as "fallback(date)" to ensure that no data is lost

        """
        try:
            with open(self.raw_filename, "w") as f:
                f.write(self.content.text)

        except Exception as e:
            try:
                with open(f"data/fallback-{datetime.datetime.now()}.txt", "w") as f:
                    f.write(self.content.text)
                logging.error(f"\n{traceback.format_exc()}------")
            
            except Exception as e:
                logging.error("Failed to WRITE")
                logging.error(f"\n{traceback.format_exc()}------")


    def prepare_data(self):
        """
        Getting the needed Information out of HTML-Code with regex
        Preparing data in json formatting
        Returning True / False dependent of actuality of that data
        """
        
        self.orte = []
        self.jsons ={}
        #splitting data to get list
        #its HTML Code and so we get each line of the table in one object
        self.orts_liste = self.text.split("<tr")

        try:
            #going trough list objects
            for i in range(len(self.orts_liste)-1):

                pattern = re.compile(r"[>](\w+[^<]*)[<]")
                captures = pattern.findall(self.orts_liste[i])

                if i > 2: #means it's a town in line 3 to end
                    #saved for later outputs, not needed for json
                    self.orte.append(captures[0])

                    #making actual json
                    self.json_text = [
                            {
                            "location": captures[0],
                            "date": str(self.date),
                            "infected": f"{captures[1]}",
                            "recovered": f"{captures[2]}",
                            "quarantine": f"{captures[3]}",
                            "deceased": f"{captures[4]}"
                            }
                        ]
                    #this town objects will later be added as a list to the "date-section"
                    self.jsons[captures[0]] = self.json_text

                #it's the head of the date information in line 2
                elif i == 1: 
                    self.data_date = captures[1]
                    #getting datteime object
                    date = self.get_date(self.data_date) 
                    
                    #if date of data is from today the function will go on
                    if self.date_check(date):
                        self.date = date 

                    else:
                        logging.debug(f"Data is not updated")                       
                        return False #data is outdated

            #make the full json by pasting the towns list into the "main-section"
            self.full_json = {
                f"{self.date}": [
                    self.jsons
                ]
                }

            return True #data preparation is finished


        except Exception as e:
            logging.error(f"\n{traceback.format_exc()}------")
            print(e)

    def write_json(self):
        try:    #writing json
            #creating filenames with new gained date
            self.get_filename() #created in self.filename /self.raw_filename
            with open(self.filename, "w") as json_f:
                json.dump(self.full_json, json_f, indent=4)
                json_f.write("\n")

        except Exception as e:
            logging.error(f"\n{traceback.format_exc()}------")
            print(e)


    def make_output(self):
        """
        Basic output, meant for trying if data structure is right and readable
        """
        try:
            with open(self.filename, "r") as json_f:
                data = json.load(json_f)

                for i in range(0, len(self.orte)):
                    x = data[str(self.date)][0][self.orte[i]][0]["location"]
                    y = data[str(self.date)][0][self.orte[i]][0]["infected"]
                    print(f"Infizierte in {x}: {y}")
                    
        except Exception as e:
            logging.error(f"\n{traceback.format_exc()}------")



    
if __name__ == "__main__":
    """
    Executing request all n-hours.
    Code will set to sleep, when data was gained
    """
    sleep_time = 7200 #2hrs
    while True:

        logging.basicConfig(
            filename="data/events.log",
            level= logging.INFO,
            style="{",
            format="[{asctime}] [{levelname}] {message}")
        req = Request()

        #req.make_output()
        if req.success:
            
            dt = datetime.datetime.now()
            time_till_tomorrow = ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)
            print(f"Got data for today {datetime.date.today()}")
            logging.info(f"Got data for today - sleeping for {time_till_tomorrow/60/60} hours")
            
            #ana = analyzer.Analyzer(req.date)
            #ana.delta_case()
            time.sleep(time_till_tomorrow)
            
        else:
            print(f"No updates so far - trying again in {sleep_time/60/60} hours")
            logging.info(f"No updates so far - trying again in {sleep_time/60/60} hours")
            time.sleep(sleep_time) #waiting 3hours

