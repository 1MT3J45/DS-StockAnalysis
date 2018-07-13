# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 10:57:21 2018
Program returns stock that goes together with a particular stock name
@author: Yogita
"""

import xlrd
import xlwt
import xlsxwriter
import os
import glob
# ------------------------------------------------------------------------------

# import pandas as pd
# import os
#
# list_of_excel_sheets = os.listdir('BIRCH_Output')
# list_of_excel_sheets.sort()
#
# total_excel_files = len(list_of_excel_sheets)
#
# for i in range(len(list_of_excel_sheets)):
#     excel1 = pd.ExcelFile('BIRCH_Output/'+list_of_excel_sheets[i])
#     total_excel_workbooks = len(excel1.sheet_names)
#     print '> Excelbook:', list_of_excel_sheets[i]
#     for j in range(len(excel1.sheet_names)):
#         print "|---",excel1.sheet_names[j]
#         work_book = excel1.parse(excel1.sheet_names[j], header=None)
#
# ------------------------------------------------------------------------------


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
            result.append(list(set(list1) | set(list2)))
    return result

if os.uname()[0] is 'Linux':
    filenames = get_filenames('BIRCH_Output')
else:
    filenames = get_filenames('C:\Users\Yogita\Desktop\DS-StockAnalysis_U1\DS-StockAnalysis-master\BIRCH_Output')

ofxls = []  # open file type xls
for i in range(len(filenames)):
    ofxls.append(xlrd.open_workbook(filenames[i]))

StockLists = []
CountLists = []
SheetCount = []
filenames.sort()
Input = raw_input('Enter Stock Name:').upper()
for i in range(0, len(filenames)):  # Iteration over each data file
    DayListCount = []
    DayStockList = []
    StockList = []
    Day = ofxls[i]
    DaySheetCount = Day.nsheets
    DayClusterNames = Day.sheet_names()
    print '>', filenames[i]
    for j in range(DaySheetCount):  #
        Cluster = Day.sheet_by_index(j)
        StockList = []
        for k in range(0, Cluster.nrows):  # ((1, Cluster.nrows-3)
            if k == 3:
                StockList.append(Input.upper())
            else:
                StockList.append(str(Cluster.cell(k, 0).value))

        print '|--- ClusterName', DayClusterNames[j], 'StockList length', len(StockList)
        DayStockList.append(StockList)
    DayListCount.append(Cluster.nrows - 4)
    StockLists.append(DayStockList)
    SheetCount.append(DaySheetCount)

RefStockList = StockLists[0][0]
RefLen = len(RefStockList)
print('Reference list length', RefLen)
print('Reference Stock list', RefStockList)

for i in range(1, len(StockLists)):
    ResultList = []
    length = []
    ResultLists = []
    for j in range(len(StockLists[i])):
        ResultList = common_elements([Input], StockLists[i][j])
        # ResultLists.append(ResultList)
        # length.append(len(ResultList))

    # print(length)
    # Max = max(length)
    # print('Max', Max)
    # Idx =length.index(max(length))
    # print("Idx_Max", Idx)
    # RefStockList = ResultLists[Idx]
    # RefLen = len(RefStockList)
    # print('Reference list length', RefLen, 'for loop Number', i)
    print 'Stock list which behaves same as input stock', ResultList
    # Write output to file