# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 14:23:57 2020

@author: kurihara
"""

import os
import glob
from muzinzo import adjust_close_value as loader
from muzinzo import plot_technical_chart as chart
from muzinzo import make_dict as dic

class Muzinzo:
    def __init__(self, database_path):
        self.database_path = database_path
        self.dict = dic.load_dict(self.database_path+'kdic.csv')
    
    def get_database_path(self):
        return self.database_path
    
    def get_dict(self):
        return self.dict
    
    def plot_chart(self, code, term=200,
                  volume=True, stochastic=True, macd=True, mav=True):
        title = str(code)+' '+self.dict[str(code)].name
        code_dir = int(code/1000)*1000
        input_path = self.database_path + str(code_dir) + "/" + str(code) + ".csv"
        df = loader.load_stock_price_csv(input_path, adjust=True, term=term)
        chart.generate_technical_chart(title, df,
            volume=volume, stochastic=stochastic, macd=macd, mav=mav)

    def make_chart(self, code, term=100, path=None):
        #print(code)
        code_dir = int(code/1000)*1000
        input_path = self.database_path + str(code_dir) + "/" + str(code) + ".csv"
        title = str(code)+' '+self.dict[str(code)].name
        df = loader.load_stock_price_csv(input_path, term=term)
        chart.generate_technical_chart(title, df, path=path)

    def get_recent_day(self):
        input_path = self.database_path + "1000/1001.csv"
        df = loader.load_stock_price_csv(input_path, term=80)
        return df.index[len(df)-1]
    
    def check_recent_day(self, recent_day, df):
        return df.index[len(df)-1]==recent_day

    def walk_around(self, process):
        recent_day = self.get_recent_day()
        for i in range(1, 10):
            input_path = self.get_database_path() + str(i*1000) + "/*.csv"
            csv_files = glob.glob(input_path)
            for csv_file in csv_files:
                filename = os.path.basename(csv_file)
                code = int(filename[0:4])
                df = loader.load_stock_price_csv(csv_file, term=100)
                if self.check_recent_day(recent_day, df) and len(df)>75:
                    process(self, code, df)


