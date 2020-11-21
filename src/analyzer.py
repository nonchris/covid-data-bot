import json
import datetime
import logging
import traceback

import pandas as pd
import matplotlib.pyplot as plt

class Analyzer:
    def __init__(self, date: datetime.date):
        self.cities = ["Adenau", "Altenahr", "Bad Breisig", "Brohltal", \
         "Grafschaft", "Bad Neuenahr-Ahrweiler", "Remagen", "Sinzig"]

        self.date = date

        self.days = 20

        self.dataframes = {}
        self.diffframes = {}

        for city in self.cities:
            self.city = city
            self.df = pd.DataFrame()

            self.read_data()

            self.calc_data()

            #self.visualize()



    def read_data(self):

        start_date = self.date - datetime.timedelta(self.days-1)
        for t in range(20):
            date = start_date + datetime.timedelta(t)
            try:
                with open(f"data/ahrweiler-{date}.json") as f:
                    #loading data, getting fist 'main' key (date)
                    data = json.load(f)
                    #print(data)
                    key = list(data.keys())[0]
                    

                    #getting 'sub keys' (locations)
                    sub_keys = data[key][0]
                    sub_keys = list(sub_keys.keys())

                    #print(sub_keys)
                    #'croppig' json to only one city
                    city_dict = data[key][0][self.city][0]
                    
                    dt = pd.json_normalize(city_dict)
                    #print(dt)
                    #building dataframe
                    if self.df.size > 0:
                        self.df = self.df.append(dt)

                    else: #if df is empty
                        self.df = pd.DataFrame(dt)

            except FileNotFoundError as e:
                #print(f"data/ahrweiler-{date}.json -- not found")
                pass

            except json.decoder.JSONDecodeError as e:
                logging.error(f"Error Encoding json for {date} - {e}")

            except Exception as exc:
                traceback.print_exc(limit=None, file=None, chain=True)
                logging.error(f"Error in Analyzer: \
                        {traceback.print_exc(limit=None, file=None, chain=True)}")
                


    def calc_data(self):
        #convertig date-sting
        self.df["date"] = pd.to_datetime(self.df["date"], format="%Y-%m-%d")
        self.df = self.df.set_index(["date", "location"])
        self.df = self.df.astype(int)
        #pd.to_numeric()
        self.diff = self.df.diff(axis=0)
        self.dataframes[self.city] = self.df
        self.diffframes[self.city] = self.diff
        #print(self.df)
        #print(self.diff)
        #print(self.dataframes)


    def visualize(self, city:str) -> str: #returns path to image

        #print('Number of colums in Dataframe : ', len(df.columns))
        #print('Number of rows in Dataframe : ', len(df.index))
        #print(df)
        #print(df["infected"])
        path = f"visuals/{city}-{self.date}.png"

        df = self.dataframes[city]
        diff = self.diffframes[city]

        fig, ax = plt.subplots(1)

        #prepare data
        x_data = df.index.get_level_values("date")
        y_data = diff["infected"]

        #colors
        # mask1 = y_data < 2
        # mask2 = y_data >= 2

        #plotting data
        fig = plt.bar(x_data, y_data, width=0.8, color=("#e31102"))
        #fig = plt.bar(x_data[mask2], y_data[mask2], width=0.8, color=("r"))
        #ax.plot(x_data, y_data, "rx", label="infected")

        #aestetics
        plt.xticks(ticks=x_data, rotation=70)
        plt.title(f"Neuinfektionen {city} - Stand {self.date}")
        plt.gcf().subplots_adjust(bottom=0.28)
        #plt.gcf().autofmt_xdate()
        
        plt.figtext(0.5, 0.02, \
"Tage ohne Aktualisierung der Daten werden ausgelassen.\n \
Dies ist eine Visualisierung der vom Kreis Ahrweiler täglich \
auf der Homepage veröffentlichten Fallzahlen. \n \
Für die Richtigkeit der Zahlen wird keinerlei Haftung übernommen. \
Dieser Bot ist ein privates Projekt und steht in keiner Verbindung zu einer Behörde.",
            color=("#a8a8a8"), fontsize="xx-small", ha="center") #backgroundcolor=("#dbdbdb")

        plt.figtext(0.95, 0.43, "t.me/aw_covidbot", rotation="vertical",\
                fontsize="medium", color=("#c9c9c9"), ha="center")
        plt.savefig(path, dpi=300)

        return path

if __name__ == '__main__':
    ana = Analyzer(datetime.date.today())
