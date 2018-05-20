#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import pandas as pd

class TableHeader(Label):
    pass


class PlayerRecord(Label):
    pass


class MyGrid(GridLayout):

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.fetch_data_from_excel()
        self.display_scores()

    def fetch_data_from_excel(self):
        # self.data = [
        #     {'name': 'name', 'score': 'score', 'car': 'car'},
        #     {'name': 'przyczajony', 'score': '1337', 'car': 'Fiat 126p'},
        #     {'name': 'Krusader Jake', 'score': '777', 'car': 'Ford'},
        #     {'name': 'dummy', 'score': '0', 'car': 'none'},
        #     {'name': 'dummy', 'score': '0', 'car': 'none'},
        #     {'name': 'dummy', 'score': '0', 'car': 'none'},
        #     {'name': 'dummy', 'score': '0', 'car': 'none'},
        #     {'name': 'dummy', 'score': '0', 'car': 'none'},
        #     {'name': 'dummy', 'score': '0', 'car': 'none'},
        #     {'name': 'dummy', 'score': '0', 'car': 'none'},
        #     {'name': 'dummy', 'score': '0', 'car': 'none'}
        # ]
        df = pd.read_excel('BIRCH_Output/01Jan_Result.xls', header=None)
        df = df.rename(columns={0:'TICKERS', 1:'OPENING', 2: 'CLOSING'})
        df.to_csv('CSVs/01JAN-RES.csv', index=False)
        dfs = pd.read_csv('CSVs/01JAN-RES.csv')
        self.data = dfs.to_dict('records')

    def display_scores(self):
        self.clear_widgets()
        for i in xrange(len(self.data)):
            if i < 1:
                row = self.create_header(i)
            else:
                row = self.create_player_info(i)
            for item in row:
                self.add_widget(item)

    def create_header(self, i):
        first_column = TableHeader(text= 'TICKERS') # str(self.data[i]['TICKERS']))
        second_column = TableHeader(text= 'OPENING') # str(self.data[i]['OPENING']))
        third_column = TableHeader(text= 'CLOSING') # str(self.data[i]['CLOSING']))
        return [first_column, second_column, third_column] # , third_column]

    def create_player_info(self, i):
        first_column = PlayerRecord(text=str(self.data[i]['TICKERS']))
        second_column = PlayerRecord(text=str(self.data[i]['OPENING']))
        third_column = PlayerRecord(text=str(self.data[i]['CLOSING']))
        return [first_column, second_column, third_column] # , third_column]


class Test(App):
    pass


Test().run()