# -*- coding: utf-8 -*-
"""
Created on Thu May  6 23:13:54 2021

@author: User
"""

import pandas as pd
import os
def read_all(program:str) -> pd.DataFrame:
    pathToFind = '頻道列表/' + program 
    files = os.listdir(pathToFind)
    comment = pd.DataFrame()
    i=0
    for file in files:
        if '.' not in file:
            print("進入資料夾-->" + file)
            tempFiles = os.listdir(pathToFind + '/' + file)
            for tempFile in tempFiles:
                comment_csv = pd.read_csv(pathToFind + '/' + file + '/' + tempFile)
                comment = comment.append(comment_csv)
                i += 1
                print(" count = " + str(i) + "---" + tempFile + "寫入成功")
    data = comment.drop_duplicates()
    data.reset_index(inplace = True, drop = True)
    return data