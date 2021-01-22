import json
import datetime
import logging
import traceback

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Analyzer:
    def __init__(self, date: datetime.date):
        self.cities = ["Adenau", "Altenahr", "Bad Breisig", "Brohltal", \
                       "Grafschaft", "Bad Neuenahr-Ahrweiler", "Remagen", "Sinzig"]

        #Source: https://infothek.statistik.rlp.de/MeineHeimat/index.aspx?id=102&l=2&g=07131&tp=1025
        #Numbers are from 31.12.2019
        self.population = {
            "Adenau": 13022,
            "Altenahr": 10910,
            "Bad Breisig": 13530,
            "Brohltal": 18433,
            "Grafschaft": 10977,
            "Bad Neuenahr-Ahrweiler": 28468,
            "Remagen": 17116,
            "Sinzig": 17630

        }

        self.date = date

        self.days = 20

        self.dataframes = {}
        self.diffframes = {}

        for city in self.cities:
            self.city = city
            self.df = pd.DataFrame()

            self.read_data()

            self.calc_data()

            # self.visualize()

    def read_data(self):

        start_date = self.date - datetime.timedelta(self.days - 1)
        for t in range(self.days):
            date = start_date + datetime.timedelta(t)
            try:
                with open(f"data/ahrweiler-{date}.json") as f:
                    # loading data, getting fist 'main' key (date)
                    data = json.load(f)
                    # print(data)
                    key = list(data.keys())[0]

                    # getting 'sub keys' (locations)
                    sub_keys = data[key][0]
                    sub_keys = list(sub_keys.keys())

                    # 'croppig' json to only one city
                    city_dict = data[key][0][self.city][0]

                    dt = pd.json_normalize(city_dict)
                    # print(dt)
                    # building dataframe
                    if self.df.size > 0:
                        self.df = self.df.append(dt)

                    else:  # if df is empty
                        self.df = pd.DataFrame(dt)

            except FileNotFoundError as e:
                # print(f"data/ahrweiler-{date}.json -- not found")
                pass

            except json.decoder.JSONDecodeError as e:
                logging.error(f"Error Encoding json for {date} - {e}")

            except Exception as exc:
                traceback.print_exc(limit=None, file=None, chain=True)
                logging.error(f"Error in Analyzer: \
                        {traceback.print_exc(limit=None, file=None, chain=True)}")

    def calc_data(self):
        # convertig date-sting
        self.df["date"] = pd.to_datetime(self.df["date"], format="%Y-%m-%d")
        self.df = self.df.set_index(["date", "location"])
        self.df = self.df.astype(int)
        # pd.to_numeric()
        self.diff = self.df.diff(axis=0)
        self.dataframes[self.city] = self.df
        self.diffframes[self.city] = self.diff
        #print(self.df)
        #print(self.diff)
        #print(self.dataframes)


    def is_missing(self, df: pd.DataFrame, date: datetime.date, counter: int) -> int:
        """
        Checks for missing data from a certain date on backwards
        Built recursive - will call itself until day with data is reached
        -> returns number of missing dates
        """

        try:
            # trying to get data
            x = df.loc[pd.to_datetime(pd.to_datetime(datetime.date.today() - date))]

            # if code runs trough at the first try - preventing divide by zero error
            if counter == 0:
                counter = 1
            return counter

        # if data is missing, a KeyError will be raised
        # -> catching and trying for next day
        except KeyError:
            # keeping track of missing days
            counter += 1
            # calling function again for next day
            counter = self.is_missing(df, date - datetime.timedelta(1), counter)

            # passing counter up
            return counter


    def incidence(self, city: str) -> int: # returns incidence value
        """
        Makes a copy of city array and cuts last seven days cut
        Checks if eight day got data, if not the case:
            Dividing seventh days value by number of days missing, to approximate
            how many cases have "really" occurred at that day
        Then all days will be summed up and the incidence will be calculated
        Does not cover the edge case when days last days and 8+ were empty
        -> dividing 'oldest' number in seven days array by number of days 8+
        -> divider will be to small by days missing at the end of the seven days array

        Return: Incidence rounded to two decimal places
        """

        days = self.diffframes[city].copy()

        # getting date from 7 days ago
        seven_days_ago = pd.to_datetime(datetime.date.today() - datetime.timedelta(7))

        # cutting last seven days out
        seven_days = days.loc[seven_days_ago: pd.Timestamp("today")]

        # checking if eighth day was missing
        divider = self.is_missing(days, datetime.timedelta(8), 0)

        # getting date of day seven - need that date type
        last_index = seven_days.index.get_level_values("date")[0]

        # approximating last days infections
        days.loc[last_index]["infected"] = days.loc[last_index]["infected"] / 2 # divider

        # sum of all seven days
        summed = seven_days["infected"].sum()

        # actual incidence
        incidence = summed * 100000 / self.population[city]

        # return rounded value
        return round(incidence, 2)


    def visualize(self, city: str) -> str:  # returns path to image

        #print('Number of colums in Dataframe : ', len(df.columns))
        #print('Number of rows in Dataframe : ', len(df.index))

        path = f"visuals/{city}-{self.date}.png"

        df = self.dataframes[city]
        diff = self.diffframes[city]

        fig, ax = plt.subplots(1)

        # prepare data
        x_data_infected = df.index.get_level_values("date")
        y_data_infected = diff["infected"]

        # plotting data
        fig = plt.bar(x_data_infected, y_data_infected, width=0.8, color=("#e31102"))

        # appearance

        # setting x-labels
        plt.xticks(ticks=x_data_infected, rotation=70)

        # setting y-axis scale
        plt.yticks(np.arange(0, y_data_infected.max() + 1, step=2))

        # grid
        ax.grid(axis="y", which='major', color=("#bdbdbd"),
                linewidth=0.4, linestyle="-")
        ax.set_axisbelow(True)

        #getting incidence
        incidence = self.incidence(city)

        # extending plot for disclaimer
        plt.title(f"Neuinfektionen {city} - Stand {self.date}\n")

        plt.figtext(0.124, 0.89, f"Inzidenz: {incidence}", fontsize="small", color=("#999999"))

        plt.gcf().subplots_adjust(bottom=0.28)
        #plt.gcf().autofmt_xdate()

        plt.figtext(0.5, 0.02, \
'Dies ist eine Visualisierung der vom Kreis Ahrweiler täglich \
auf der Homepage veröffentlichten Fallzahlen. \n \
Tage ohne Aktualisierung der Daten werden ausgelassen. \
Eine Lücke in den Daten führt zu einem "doppelten" Anstieg am Folgetag.\n\
Für die Richtigkeit der Zahlen wird keinerlei Haftung übernommen. \
Dieser Bot ist ein privates Projekt und steht in keiner Verbindung zu einer Behörde.',
            color=("#a8a8a8"), fontsize="xx-small", ha="center") #backgroundcolor=("#dbdbdb")

        plt.figtext(0.95, 0.43, "t.me/aw_covidbot", rotation="vertical", \
                    fontsize="medium", color=("#c9c9c9"), ha="center")
        plt.savefig(path, dpi=300)

        return path


if __name__ == '__main__':
    ana = Analyzer(datetime.date.today() - datetime.timedelta(1))
    ana.incidence("Sinzig")
