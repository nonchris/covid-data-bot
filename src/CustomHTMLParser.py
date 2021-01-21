import re
from html.parser import HTMLParser


class CustomParser(HTMLParser):
    """
    This extension of HTMLParser extracts the needed text from the raw HTML
    """

    def error(self, message):
        pass

    def collect(self, html_text: str) -> list:
        """
        Function that starts the processing
        -> initializes additional required class variables
        -> feeds text input to parser function

        is_capture: needed to toggle whether the incoming line is interesting
        found_lines: will contain all found text at the end

        Returns: found_text (str)
        """

        self.is_capture = False
        self.found_lines = []

        self.feed(html_text)

        return self.found_lines

    def handle_data(self, text):
        """
        Function gets called when HTMLParser finds actual content on website
        - checks whether headline matches using RegEx
            - sets is_capture to True
             - starts to collect all following lines in found_text
        - sets is_capture to False when start of line matches last expected line
        """

        # cleaning text and checking whether text is empty
        text = text.strip()
        if text == "":
            return

        # headline pattern
        # example: Coronavirus: Ein weiterer Todesfall und 14 Neuinfektionen im Kreis
        # Disclaimer: The cases are evaluated from a regex-able view!
        # There is no judgement about the actual meaning of that headline.
        # best case: infections as digits deaths as letters or don't even exist
        # text_headline = re.compile(r'^Coronavirus:(\D*\d+){1,2} Neuinfektionen im Kreis$')
        # worst case: both numbers are written in letters instead of digits
        text_headline2 = re.compile(r'^Coronavirus:(\s\w+){1,5}\sNeuinfektionen im Kreis$')
        # most unlikely case: infections and deaths both are numbers
        # text_headline3 = re.compile(r'^Coronavirus:\D*\d+\D*\d+ Neuinfektionen im Kreis$')

        # tries to find pattern in input
        # captures = text_headline.search(text)
        captures2 = text_headline2.search(text)
        # captures3 = text_headline3.search(text)

        # if pattern is found
        if captures2 is not None:  # or captures is not None: #or captures3 is not None:
            # sets capture status to True
            self.is_capture = True

        # just for controls...
        # if text.startswith("Corona"):
        #     print("Starts with corona:", text)
        #     print("captures:", captures)

        # when line is in needed block
        if self.is_capture:
            self.found_lines.append(text)

            # checking if line is last interesting line
            if text.startswith("Kreisverwaltung Ahrweiler - "):
                self.found_lines.remove("©")  # removing one unneeded line, we know it's there
                self.is_capture = False  # setting capture to False to skip the rest
