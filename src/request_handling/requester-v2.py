import datetime
import logging
import time
import traceback
from datetime import date

from dateutil import parser as dateparser

import requests

from CustomHTMLParser import CustomParser
from src.request_handling.JSONMaker import JSONMaker


class RequesterV2:
    """
    The new Request Class that connects to the press releases
    It handles requests and searching for valuable data (interesting lines from HTML-text)
    The actual data (found lines) processing is done by the JSONMaker class

    The process is based on iterating trough numbered press releases to find a new release from today\n
    This class also does the checks whether the data found is usable using also the HTMLParser class
    If data seems valid the status code True will be returned and the JSONMaker class can start

    If no data is found the class will return False and 'fall asleep' until it gets called again.

    This class is meant to be created once at startup and stay active until the whole program stops.

    do_request() is the method to start a new try for a request.
    """

    def __init__(self, link: str, start_nr: int):

        # 'static variables'
        self.parser = CustomParser()  # initializing HTML parser
        self.link = link  # holds link base

        # 'dynamic variables'
        self.status = False
        self.latest_nr = start_nr  # number of last requested press release
        self.pub_date = None       # holds date of publication
        self.latest_link = ""      # holds final link to
        self.lines = []            # holds found and filtered lines

    def do_request(self):
        """
        Resets results variables and starts scan for new press releases
        :return: bool - status if new release was found
        """
        # resetting variables
        self.lines = []
        self.status = False
        self.pub_date = None
        self.latest_link = ""

        # starting request
        self.status = self.find_latest(self.latest_nr)
        return self.status

    @staticmethod
    def extract_date(lines: list) -> date:
        """
        :param lines: list containing all extracted lines from request.

        Extracts the date from out found lines\n
        - We know that the date is in the last time with the copyright information
        - Date is the last part of that line

        Extracting date by by:\n
        - extracting last line from lines
        - casting line to string and splitting it
        - retrieving last object from that new list
        - converting date to date-object using parser from dateutil

        :return: parsed date
        """
        this_date: str = str(lines[-1]).split()[-1]
        this_date: date = dateparser.parse(this_date).date()

        return this_date

    @staticmethod
    def is_today(to_test: date, look_back=0) -> bool:
        """
        :param to_test: date that needs to be tested
        :param look_back: optional to compare to a passed date

        Tests if input date is current day\n
        Offering look_back parameter to compare to an other day using timedelta()

        :return: True if date matches comparison
        """
        if datetime.date.today() - datetime.timedelta(look_back) == to_test:
            return True
        return False

    def get_raw_filename(self) -> str:
        """Building RAW filename"""
        return f"data/ahrweiler-{self.pub_date}_raw.txt"

    def write_raw(self, text: str):
        """
        :param text: HTML text gained via request
        Writing the pure request to a file for later data handling
        """
        try:
            with open(self.get_raw_filename(), "w") as f:
                f.write(text)

        except Exception as e:
            logging.error("Failed to WRITE")
            logging.error(f"\n{traceback.format_exc()}------")

    def find_latest(self, nr) -> bool:
        """
        :param nr: number to complete request link

        Requests website:
        - builds link, links are counted upwards like release=0001 / 0002 etc
        - starts request

        Starts content analysis
        - using self instance of HTMLParser

        Evaluates results:\n
        - checks if site has content (returns if empty)
        - checks if content has the required scheme (see HTMLParser)
        - checks if date is from today

        If new release is not found:\n
            Starts recursive call of that function with incremented number param\n
        If release is found:\n
            saving extracted content in self.lines\n
            saving nr of link in self.latest_nr

        :return: bool - True if new data gained, else false
        """

        link = self.link + str(nr)

        content = requests.get(link)

        # check if request worked
        if content.status_code != 200:
            logging.error(f"Error getting page, [Status Code: {content.status_code}]")

        # returning false if there is no link for day, yet
        # checks for place-holders -> there are unlimited links for press-releases
        # 'Druckversion' is only contained by pages that contain content
        if content.text.find("Druckversion") == -1:
            print("found nothing")
            return False

        # filtering for relevant content
        # found lines will be a list that is empty if article does not match scheme
        found_lines = self.parser.collect(content.text)
        print("-----------------------")

        # checking if matching content was found
        # extracting date to see if news are from today
        self.pub_date = None
        if found_lines:
            self.pub_date = self.extract_date(found_lines)

        # we're done - found correct press-release!
        if self.is_today(self.pub_date):  # and date != -1:
            print("FOUND matching date!")
            print(self.pub_date, link)
            self.write_raw(content.text)  # writing html code
            self.lines = found_lines      # saving found lines
            self.latest_nr = nr           # saving link number
            self.latest_link = link       # saving source link
            return True

        else:
            print("Tried: ", link)
            time.sleep(1)  # we don't wanna spam them to much - do we? :)
            self.find_latest(nr + 1)  # recursive call


if __name__ == "__main__":
    req = RequesterV2("https://www.kreis-ahrweiler.de/presse.php?lfdnrp=", 9689)
    req.do_request()
    maker = JSONMaker()
    maker.make_json(req.pub_date, req.lines)
