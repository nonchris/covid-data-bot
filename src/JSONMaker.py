import json
import logging
import re
import traceback
from datetime import date
from typing import List, Any, Dict, Union, Optional

import src.utils as utils


class JSONMaker:
    """
    Class responsible for taking pre-filtered lines of press release and converting it into a JSON file
    - Handles final filtering for needed case numbers of the requested data
    - Builds JSON from extracted numbers and writes it
    """

    def __init__(self):
        """Just inits variables"""
        self.date = None  # holds date of data input

        self.status = False  # status whether everything worked
        self.json = {}  # final json that will be written

    def make_json(self, creation_date: date, content: list) -> bool:
        """
        :param creation_date: date of data
        :param content: list of strings containing numbers to extract

        Function to start creation\n
        Process:\n
        - filter for relevant numbers
        - convert those numbers to JSON like structure
        - build and write JSON to file
        :return: status if processing was successful
        """

        self.date = creation_date  # holds date press release was created

        self.status = False  # status for external access
        self.json = {}  # final JSON structure

        # returns bool - only continuing when function worked
        pre_json = self.prepare_data(content)
        if pre_json:
            # building json -> wrapping inner data structure
            self.json = self.build_json(pre_json)

            # saving status for external control
            self.status = self.write_json()
            return self.status

        return False

    @staticmethod
    def validate_captures(line: str, captures: list, expected_len=4, city="Unknown") -> bool:
        """
        :params line: raw string to validate
        :params captures: list of captures
        :params expected_len: for check if captures equal expect value
        :params city: only optional for better logging

        Validates extracted numbers by:
        - comparing number of captures with expected value
        - searching for know pattern to see if number describes what's expegcted\n
        This process is hardcoded and fails when only a little thing in the press release changes - that's what we want!

        :return: True if all checks passed else False
        """

        # abnormal amount of extracted numbers
        if len(captures) != expected_len:
            logging.error(f"FOUND WRONG AMOUNT OF NUMBERS FOR {city}! Expected: {expected_len} Gained: {len(captures)}")
            return False  # exiting

        # controlling positions of keywords that declare meaning of number
        # Example: 'Verbandsgemeinde Adenau:
        # 206 Infektionen gesamt, davon 197 genesen, 2 Personen verstorben, 7 aktuell infizierte Personen;'
        # controlling if expected structures exist
        # infected number
        if line.find(f'{captures[0]} Infektionen gesamt') == -1:
            logging.error(f"INFECTIONS KEYWORD NOT AT EXPECTED POSITION! - City: {city}\n{line}")
            return False

        # recovered number
        if line.find(f'{captures[1]} genesen') == -1:
            logging.error(f"RECOVERED KEYWORD NOT AT EXPECTED POSITION!- City: {city}\n{line}")
            return False

        # deceased number - can be 'person' or 'personen' (plural)
        if line.find(f'{captures[2]} Person verstorben') == -1 and line.find(
                f'{captures[2]} Personen verstorben') == -1:
            logging.error(f"DECEASED KEYWORD NOT AT EXPECTED POSITION! - City: {city}\n{line}")
            return False

        # currently infected
        if line.find(f'{captures[3]} aktuell infizierte') == -1:
            logging.error(f"CURRENTLY INFECTED KEYWORD NOT AT EXPECTED POSITION! - City: {city}\n{line}")
            return False

        return True

    def prepare_data(self, content: list) -> Optional[Dict[Any, List[Dict[str, Union[str, Any]]]]]:
        """
        :param content: list of strings containing numbers to extract

        - filters lines staring with a city name
        - extracts actual numbers from those lines
        - makes inner JSON structure from extraced numbers

        :return: JSON-like dict when successful else None
        """

        # iterating trough lines
        pre_json = {}  # will contain inner json structure
        for line in content:
            # splitting because the second (and maybe third) word will be the city name
            # Example - 'Verbandsgemeinde Adenau: 206 Infektionen gesamt (...)
            # Example -  Verbandsgemeinde Bad Breisig: 239 Infektionen gesamt (...)
            split = line.split()
            one_word = split[1][:-1].lower()  # holds name in first case
            two_words = f"{split[1]} {split[2][:-1]}".lower()  # for second case

            # checking if keyword matches a key from the 'translator' dict
            try:
                # trying first case first, because it's more likely
                name = utils.translator[one_word]

            except KeyError:
                # failed - let's try the second one
                try:
                    name = utils.translator[two_words]

                except KeyError as e:
                    # failed again? - we don't want that line
                    logging.debug(f"Failed translating {one_word} / {two_words}")
                    continue  # going straight to next word

            # finally extracting numbers from line
            captures = re.findall(r'\d+', line)

            # checks if found numbers are described as expected, if not: exit
            if not self.validate_captures(line, captures, city=name):
                logging.error("FAILED to validate data integrity - exit without building JSON ")
                return None

            try:
                # building structure - try is just there for case x
                # it shouldn't be able to fail if the line made it until here
                pre_json[name] = [
                    {
                        "location": name,
                        "date": str(self.date),
                        "infected": captures[0],
                        "current": captures[3],
                        "recovered": captures[1],
                        "deceased": captures[2],
                    }
                ]

            except Exception as e:
                logging.error(f"FAILED BUILDING INNER BODY OF JSON")
                logging.error(f"\n{traceback.format_exc()}------")
                return None

        # TODO: CHECK FOR MATCHING KEY AMOUNT
        return pre_json  # return structure

    def build_json(self, pre_json) -> dict:
        """
        Wraps inner JSON structure in outer body\n
        -> setting date of received data as key

        :return: JSON-like dict containing the complete structure
        """
        full_json = {
            f"{self.date}": [
                pre_json
            ]
        }

        return full_json

    def get_filename(self) -> str:
        """
        Building JSON filename
        :return: filename
        """
        return f"data/ahrweiler-{self.date}.json"

    def write_json(self) -> bool:
        """
        Writes JSON to file
        :return: bool - status if everything worked like expected
        """
        # trying to create and write file
        try:
            with open(self.get_filename(), "w") as json_file:
                json.dump(self.json, json_file, indent=4)
                json_file.write("\n")

            return True

        # in case something fails
        except Exception as e:
            logging.error("FAILED WRITING JSON")
            logging.error(f"\n{traceback.format_exc()}------")
            print(e)
            return False
