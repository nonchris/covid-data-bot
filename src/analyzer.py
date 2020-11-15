import json
import datetime

import pandas as pd
import matplotlib.pyplot as plt

class Analyzer:
    def __init__(self, date: datetime.date):
        self.cities = ["Adenau", "Altenahr", "Bad Breisig", "Brohltal", \
         "Grafschaft", "Bad Neuenahr-Ahrweiler", "Remagen","Sinzig"]

        self.date = date

        self.days = 20

        for city in self.cities:
            self.city = city
            self.df = pd.DataFrame()

            self.read_data()

            self.calc_data()

            self.visualize()



    def read_data(self):

        start_date = self.date - datetime.timedelta(self.days)
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
                print(f"data/ahrweiler-{date}.json -- not found")

            except Exception as e:
                print(e)


    def calc_data(self):
        self.df = self.df.set_index(["date", "location"])
        self.df = self.df.astype(int)
        #pd.to_numeric()
        self.diff = self.df.diff(axis=0)
        print(self.diff)


    def visualize(self):

        #print('Number of colums in Dataframe : ', len(df.columns))
        #print('Number of rows in Dataframe : ', len(df.index))
        #print(df)
        #print(df["infected"])

        fig, ax = plt.subplots(1)

        #prepare data
        x_data = self.df.index.get_level_values("date")
        y_data = self.diff["infected"]

        #colors
        # mask1 = y_data < 2
        # mask2 = y_data >= 2

        #plotting data
        fig = plt.bar(x_data, y_data, width=0.8, color=("#e31102"))
        #fig = plt.bar(x_data[mask2], y_data[mask2], width=0.8, color=("r"))
        #ax.plot(x_data, y_data, "rx", label="infected")

        #aestetics
        plt.xticks(ticks=x_data, labels=x_data, rotation=70)
        plt.title(f"New cases in {self.city}")
        plt.savefig(f"visuals/{self.city}-{self.date}.png", dpi=300)

if __name__ == '__main__':
    ana = Analyzer(datetime.date.today())
