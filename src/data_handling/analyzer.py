import re
import json
import datetime
import logging
import traceback

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Analyzer:
    def __init__(self, pub_date: datetime.date):
        """
        :param pub_date: latest date data was published

        Class responsible for analyzing and plotting the data read from generated JSONs
        - reads JSONs
        - loads data to dataframes
        - calculates vales e.g. diff from new infections
        - plots data using matplotlib
        - saved figure as image
        """
        self.cities = ["Adenau", "Altenahr", "Bad Breisig", "Brohltal",
                       "Grafschaft", "Bad Neuenahr-Ahrweiler", "Remagen", "Sinzig"]

        # Source: https://infothek.statistik.rlp.de/MeineHeimat/index.aspx?id=102&l=2&g=07131&tp=1025
        # Source 2: https://infothek.statistik.rlp.de/MeineHeimat/content.aspx?id=101&l=1&g=07131&tp=2
        # Numbers are from 31.12.2019
        self.population = {
            "Adenau": 13022,
            "Altenahr": 10910,
            "Bad Breisig": 13530,
            "Brohltal": 18433,
            "Grafschaft": 10977,
            "Bad Neuenahr-Ahrweiler": 28468,
            "Remagen": 17116,
            "Sinzig": 17630,
            "Kreis": 130036,
        }

        self.date = pub_date  # date latest date of data

        self.days = 20  # days to look back

        self.dataframes = {}  # holds data frames for each city
        self.diffframes = {}  # holds difference dataframes for each city

        for city in self.cities:
            self.city = city
            self.df = pd.DataFrame()

            self.read_data()

            self.calc_data()

            # self.visualize()

        self.add_kreis()

    def read_data(self):
        """
        Reads multiple JSON-Files in data-frame
        Saves data-frame in self.df
        """

        # staring at latest date we want to cover - counting dates up
        start_date = self.date - datetime.timedelta(self.days - 1)
        for t in range(self.days):
            date = start_date + datetime.timedelta(t)
            try:
                with open(f"data/ahrweiler-{date}.json") as f:
                    # loading data, getting fist 'main' key (date)
                    data = json.load(f)

                    key = list(data.keys())[0]  # getting main key to access JSON

                    # 'cropping' json to only one city
                    city_dict = data[key][0][self.city][0]

                    dt = pd.json_normalize(city_dict)

                    # building dataframe
                    if self.df.size > 0:
                        self.df = self.df.append(dt)

                    else:  # if df is empty
                        self.df = pd.DataFrame(dt)

            except FileNotFoundError as e:
                logging.warning(f"data/ahrweiler-{date}.json -- NOT FOUND")
                print(f"data/ahrweiler-{date}.json -- not found")

            except json.decoder.JSONDecodeError as e:
                logging.error(f"Error Encoding json for {date} - {e}")

            except Exception as exc:
                traceback.print_exc(limit=None, file=None, chain=True)
                logging.error(f"Error in Analyzer: \
                        {traceback.print_exc(limit=None, file=None, chain=True)}")

    def calc_data(self):
        """
        Prepares data by:
        - setting date and location as indices
        - converting data to integers
        - calculating diff to previous day
        Saves data-frames in class-dictionaries using city as key
        """

        # setting indices
        self.df["date"] = pd.to_datetime(self.df["date"], format="%Y-%m-%d")
        self.df = self.df.set_index(["date"])
        # dropping location column that contains the name of the location in each row
        self.df = self.df.drop(columns="location")

        # converting date-string
        self.df = self.df.astype(float)
        # pd.to_numeric()

        # calculating difference to previous day
        diff = self.df.diff(axis=0)

        # saving dataframes to dictionaries using city as keys
        self.dataframes[self.city] = self.df
        self.diffframes[self.city] = diff

    def add_kreis(self):
        """
       Special calculation for 'Kreis'-dataframe which is the sum of all other dataframes
       The function iterates over all dataframes and calculates the added dataframes and diffframes
       """

        df = 0
        diff = 0
        for k in self.dataframes.keys():
            df += self.dataframes[k]
            diff += self.diffframes[k]

        self.dataframes["Kreis"] = df
        self.diffframes["Kreis"] = diff

    def incidence(self, city: str) -> int:  # returns incidence value
        """
        :param city: name of df-index to address

        Makes a copy of city array and cuts last seven days cut

        Then all days will be summed up and the incidence will be calculated\n
        Does not cover the edge case of missing data at the "end" of the seven days\n

        :return: Incidence rounded to two decimal places
        """

        days = self.diffframes[city].copy()

        # getting date from 7 days ago
        seven_days_ago = pd.to_datetime(self.date - datetime.timedelta(6))

        # cutting last seven days out
        seven_days = days.loc[seven_days_ago: pd.Timestamp(self.date)]

        # sum of all seven days
        summed = seven_days["infected"].sum()

        # actual incidence
        incidence = summed * 100000 / self.population[city]

        # return rounded value
        return round(incidence)

    def visualize(self, city: str) -> str:  # returns path to image
        """
        :param city: key to dict with dataframes

        - Generates bar-plot of infections from diff-dataframe
        - Saves them as png

        :return: name of file
        """

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
        plt.xticks(ticks=x_data_infected, rotation=80)

        # setting y-axis scale
        plt.yticks(np.arange(0, y_data_infected.max() + 1, step=2))

        # grid
        ax.grid(axis="y", which='major', color=("#bdbdbd"),
                linewidth=0.4, linestyle="-")
        ax.set_axisbelow(True)

        # getting incidence
        incidence = self.incidence(city)

        # extending plot for disclaimer
        plt.title(f"Neuinfektionen {city} - Stand {self.date}\n")

        # red
        color = "#f2291b" if incidence >= 100 else "#8c8c8c"
        plt.figtext(0.124, 0.89, f"Inzidenz: {incidence}", fontsize="small", color=color)

        plt.gcf().subplots_adjust(bottom=0.28)
        # plt.gcf().autofmt_xdate()

        # 'water mark' on the right side
        plt.figtext(0.95, 0.43, "t.me/aw_covidbot", rotation="vertical",
                    fontsize="medium", color=("#adadad"), ha="center")

        plt.figtext(0.975, 0.457, "open telegram bot", rotation="vertical",
                    fontsize="x-small", color=("#cccccc"), ha="center")

        # bottom disclaimer
        plt.figtext(0.5, 0.02,
                    'Dies ist eine Visualisierung der vom Kreis Ahrweiler täglich'
                    'auf der Homepage veröffentlichten Fallzahlen. \n'
                    f'Für die Inzidenz wurde eine Einwohnerzahl von {self.population[city]} angenommen. '
                    'Tage ohne Aktualisierung sind durch fehlende Beschriftung dargestellt.\n'
                    'Für die Richtigkeit der Zahlen wird keinerlei Haftung übernommen. '
                    'Dieser Bot ist ein Open-Source Projekt und steht in keiner Verbindung zu einer Behörde.',
                    color=("#a8a8a8"), fontsize="xx-small", ha="center")  # backgroundcolor=("#dbdbdb")

        # saving plot to disk
        try:
            plt.savefig(path, dpi=300)
        except Exception as e:
            logging.error(f"FAILED SAVING PLOT {path}\n{traceback.format_exc()}")

        return path


if __name__ == '__main__':
    date = datetime.date(2021, 3, 21)
    # lists for populations and and incidences
    their_pop = []
    our_pop = []
    their_inc = []
    our_inc = []
    infected = []
    dates = []

    # iterate trough last days
    for i in range(18):
        d = date - datetime.timedelta(i)
        # %Y-%m-%d
        dates.append(d.strftime("%d.%m"))
        # get incidence from saved file
        try:
            with open(f"../data/ahrweiler-{d}_raw.txt") as f:
                read = f.read()
                find = re.search(r"Die Sieben-Tage-Inzidenz für den Kreis Ahrweiler liegt bei (\d+) Neuinfektionen", read)
                official_inc = int(find.group(1))
        except FileNotFoundError:
            continue
        their_inc.append(official_inc)

        # load dataframe from specific date
        ana = Analyzer(d)
        frame: pd.DataFrame = ana.diffframes["Kreis"]
        # slice 7 days for incidence
        slc = frame["infected"][len(frame)-7: len(frame)]
        slc_sum = slc.sum()

        infected.append(slc_sum)

        # Own incidence
        own_inc = ana.incidence("Kreis")
        our_inc.append(round(own_inc))

        # Used population: infected * 100k / official incidence
        tp = int(slc_sum * 100000 / round(own_inc))

        their_pop.append(tp)
        our_pop.append(ana.population["Kreis"])

    print("Infected:")
    print(f"DT: {dates}")
    print(f"IF: {infected}")
    print()
    print("Incidences:")
    print(f"TI: {their_inc}")
    print(f"OI: {our_inc}")
    print(f"DF: {np.array(their_inc) - np.array(our_inc)}")
    print()
    print("Population:")
    print(f"TP: {their_pop}")
    print(f"OP: {our_pop}")
    print(f"DF: {np.array(their_pop) - np.array(our_pop)}")


