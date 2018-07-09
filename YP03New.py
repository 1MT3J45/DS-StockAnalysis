# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 10:57:21 2018
Program returns stock that goes together for N days
@author: Yogita
"""

import xlrd
import xlwt
import xlsxwriter
import os
import glob


def excel_file_filter(filename, extensions=['.xls', '.xlsx']):
    return any(filename.endswith(e) for e in extensions)


def get_filenames(root):
    filename_list = []
    for path, subdirs, files in os.walk(root):
        for filename in filter(excel_file_filter, files):
            filename_list.append(os.path.join(path, filename))
    return filename_list


def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result


filenames = get_filenames('BIRCH_Output')

ofxls = []  # open file type xls
no_of_days = int(input('Last how many days:'))
for i in range(len(filenames[-no_of_days:])):
    ofxls.append('')
    ofxls[i] = xlrd.open_workbook(filenames[i])

StockLists = []
CountLists = []
SheetCount = []
for i in range(0, len(ofxls)):  # Iteration over each data file
    DayListCount = []
    DayStockList = []
    StockList = []
    Day = ofxls[i]
    DaySheetCount = Day.nsheets
    DayClusterNames = Day.sheet_names()
    for j in range(DaySheetCount):  #
        Cluster = Day.sheet_by_index(j)
        StockList = []
        for k in range(0, Cluster.nrows):  # ((1, Cluster.nrows-3)
            StockList.append(str(Cluster.cell(k, 0).value))
        print('ClusterName', DayClusterNames[j], 'StockList length', len(StockList))
        DayStockList.append(StockList)
    DayListCount.append(Cluster.nrows - 4)
    StockLists.append(DayStockList)
    SheetCount.append(DaySheetCount)

import pandas as pd
columns = ['Cluster', 'Stock_List']
df = pd.DataFrame(columns=columns)
for k in range(len(StockLists[0])):
    RefStockList = StockLists[0][k]
    RefLen = len(RefStockList)
    print('----------------Cluster-------------------------:', k)
    print('Reference list length', RefLen)
    print('Reference Stock list', RefStockList)
    for i in range(1, len(StockLists)):
        ResultList = []
        length = []
        ResultLists = []
        res = []
        for j in range(len(StockLists[i])):
            ResultList = common_elements(RefStockList, StockLists[i][j])
            ResultLists.append(ResultList)
            length.append(len(ResultList))
        print(length)
        Max = max(length)
        print('Max', Max)
        Idx = length.index(max(length))
        print("Idx_Max", Idx)
        RefStockList = ResultLists[Idx]
        RefLen = len(RefStockList)
        print('Reference list length', RefLen, 'for loop Number', i)
        print('Reference Stock list', RefStockList)
        if i == len(StockLists)-1:
            stocks = ', '.join(RefStockList)
            df = df.append({'Cluster': k, 'Stock_List': stocks}, ignore_index=True)
df.to_csv('Results/ClusterResults.csv', index=False)

# Write output to file:It write only result for last cluster in xls file.


# Create an new Excel file and add a worksheet.
flist = [os.path.basename(x) for x in glob.glob(os.getcwd() + '\\*.txt')]
workbook = xlsxwriter.Workbook('YP03NewRes.xls')

for sh in flist:
    worksheet = workbook.add_worksheet(sh)
    with open(sh, 'rb') as f:
        for k in range(0, len(RefStockList)):
            worksheet.write(k, 0, RefStockList[k])
# worksheet = workbook.add_worksheet(i)
# Col_cell = 0
# #Write some simple text.
# for k in range(0, len(RefStockList)):
# worksheet.write(k,Col_cell,RefStockList[k])
# #Col_cell=Col_cell+1
# worksheet = workbook.add_worksheet()


workbook.close()

# TODO N = Day wise (in Descending order) [OFXLS : Decides the Days from User]
# TODO N = Could also be in Start & End Date
