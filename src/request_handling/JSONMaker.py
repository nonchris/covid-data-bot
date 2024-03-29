import json
import logging
import re
import traceback
from datetime import date
from typing import List, Any, Dict, Union, Optional

import data_handling.utils as utils
from numpy import nan


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
        self.patterns = None
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

        # getting possible press release patterns from file
        # loading it each time the function is called to allow for adjustments while code is running
        self.patterns = JSONMaker.load_patterns()
        if self.patterns is None:
            # logging happens in load_checks()
            return False

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
    def load_patterns(filename="possible_patterns.json") -> Dict[str, List[str]]:
        """
        :param filename: path to filename as string

        Reads possible text patterns from json.\n
        Idea: Patterns are defined externally to minimize code changes

        :returns: patterns as dict containing lists or None if file FileNotFound
        """
        try:
            with open(filename) as f:
                lines = f.read()
                return json.loads(lines)
        except FileNotFoundError:
            print(f"NO PATTERN FILE '{filename}' - EXITING BUILD PROCESS")
            logging.error(f"NO PATTERN FILE '{filename}' - EXITING BUILD PROCESS")

    def validate_captures(self, line: str, captures: list, expected_len=4, city="Unknown") -> Union[Dict[str, Any]]:
        """
        :params line: raw string to validate
        :params captures: list of captures
        :params expected_len: for check if captures equal expect value
        :params city: only optional for better logging

        Validates extracted numbers by:
        - comparing number of captures with expected value\n
        - searching for known pattern to see if number describes what's expected\n
        Patterns are loaded from 'data/possible_patterns.json'\n
        This process fails when only a little thing in the press release differs from all expected patterns\n
        That's what we want!\n\n
        Pattern file is loaded each time the function gets called -> allows for adjustments while code is running

        :return: Filled dict if all checks passed else empty dict
        """

        # setting expected positions of each value
        # checking also for abnormal amount of extracted numbers
        # TODO: EdgeCase: Not every city has a number as mutation value
        # case for the fold press releases - four numbers and no britain mutation
        if len(captures) == expected_len:
            inf_pos, rec_pos, dec_pos, cur_pos, mut_pos = 0, 1, 2, 3, None

        # case for new press releases five numbers, britain mutation is jacked in as 2nd value
        elif len(captures) == expected_len+1:
            inf_pos, rec_pos, dec_pos, cur_pos, mut_pos = 0, 2, 3, 4, 1

        else:
            logging.error(f"FOUND WRONG AMOUNT OF NUMBERS FOR {city}! Expected: {expected_len} Gained: {len(captures)}")
            return {}

        capture_dict = {}

        # controlling positions of keywords that declare meaning of number
        # Example: 'Verbandsgemeinde Adenau:
        # 206 Infektionen gesamt, davon 197 genesen, 2 Personen verstorben, 7 aktuell infizierte Personen;'
        # controlling if expected structures exist
        # infected number
        for pattern in self.patterns["infected"]:
            if line.find(pattern.format(captures[inf_pos])) != -1:
                capture_dict["infected"] = captures[inf_pos]
                break
        else:
            logging.error(f"'INFECTIONS' KEYWORD ({captures[inf_pos]}) NOT AT EXPECTED POSITION ({inf_pos})! - City: {city}\n{line}")
            return {}

        # recovered number
        # current version is Genesene, genesen is legacy, Genese is stupidity
        for pattern in self.patterns["recovered"]:
            if line.find(pattern.format(captures[rec_pos])) != -1:
                capture_dict["recovered"] = captures[rec_pos]
                break
        else:
            logging.error(f"'RECOVERED' KEYWORD ({captures[rec_pos]}) NOT AT EXPECTED POSITION ({rec_pos})!- City: {city}\n{line}")
            return {}

        # deceased number - can be 'person' or 'personen' (plural)
        for pattern in self.patterns["deceased"]:
            if line.find(pattern.format(captures[dec_pos])) != -1:
                capture_dict['deceased'] = captures[dec_pos]
                break
        else:
            logging.error(f"'DECEASED' KEYWORD ({captures[dec_pos]}) NOT AT EXPECTED POSITION ({dec_pos})! - City: {city}\n{line}")
            return {}

        # currently infected
        # current version 'aktuell Infizierte', legacy 'aktuell infizierte (Personen)' -> using lower()
        for pattern in self.patterns["current"]:
            if line.lower().find(pattern.format(captures[cur_pos])) != -1:
                capture_dict["current"] = captures[cur_pos]
                break
        else:
            logging.error(f"'CURRENTLY INFECTED' KEYWORD ({captures[cur_pos]}) NOT AT EXPECTED POSITION ({cur_pos})! - City: {city}\n{line}")
            return {}

        # britain mutation - optional
        # current '7 Fälle der britischen Mutation B.1.1.7'
        if mut_pos:
            for pattern in self.patterns["voc_pos"]:
                if line.find(pattern.format(captures[mut_pos])) != -1:
                    capture_dict["b117"] = captures[mut_pos]
                    break
            else:
                logging.error(
                    f"'BRITAIN MUTATION' KEYWORD ({captures[mut_pos]}) NOT AT EXPECTED POSITION ({mut_pos})! - City: {city}\n{line}")
                return {}
        else:  # if mut_pos == None
            logging.warning(f"'BRITAIN MUTATION' no values for today! - City: {city}\n{line}")
            capture_dict["b117"] = nan  # setting dict value to np.nan

        return capture_dict

    @staticmethod
    def extract_numbers(line: str) -> List[str]:
        """
        :param line: string with numbers

        extracts all 'integers' from string

        :returns: List with all captured numbers
        """
        captures = re.findall(r'(\d+)\s', line)
        return captures

    def prepare_data(self, content: list) -> Optional[Dict[Any, List[Dict[str, Union[str, Any]]]]]:
        """
        :param content: list of strings containing numbers to extract

        - filters lines staring with a city name
        - extracts actual numbers from those lines
        - makes inner JSON structure from extracted numbers

        :return: JSON-like dict when successful else None
        """

        # iterating trough lines
        city_json = {}  # will contain inner json structure (each city one dict)
        for line in content:
            # splitting because the second (and maybe third) word will be the city name
            # Example - 'Verbandsgemeinde Adenau: 206 Infektionen gesamt (...)
            # Example -  Verbandsgemeinde Bad Breisig: 239 Infektionen gesamt (...)
            split = line.split()

            # a sentence this short probably won't be needed, but it causes IndexErrors below - skipping
            if len(split) < 3:
                continue
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
            # checking for whitespace after number to detect only 'integers' as number and not Covid B.1.1.7
            captures = self.extract_numbers(line)

            # checks if found numbers are described as expected, if not: exit
            # getting a dict with the correct processed data back
            captures_dict = self.validate_captures(line, captures, city=name)
            if not captures_dict:
                logging.error("FAILED to validate data integrity - exit without building JSON ")
                return None

            try:
                # building structure - try is there for validation that data is in JSOn shape
                # it shouldn't be able to fail if the line made it until here
                captures_dict["location"] = name
                captures_dict["date"] = str(self.date)
                city_json[name] = [
                    captures_dict
                ]

            except Exception as e:
                logging.error(f"FAILED BUILDING INNER BODY OF JSON")
                logging.error(f"\n{traceback.format_exc()}------")
                return None

        # TODO: CHECK FOR MATCHING KEY AMOUNT
        return city_json  # return structure

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
                json.dump(self.json, json_file, indent=4, allow_nan=True)
                json_file.write("\n")

            return True

        # in case something fails
        except Exception as e:
            logging.error("FAILED WRITING JSON")
            logging.error(f"\n{traceback.format_exc()}------")
            print(e)
            return False
