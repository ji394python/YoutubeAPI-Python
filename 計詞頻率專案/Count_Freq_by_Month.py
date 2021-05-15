# -*- coding: utf-8 -*-
"""
Created on Mon May 10 16:43:50 2021

@author: Luis Fan 19980521
"""
import pandas as pd
import os


def count_words_by_month(word_list:list, filename_list:list):
    for i in words_list:
        res = pd.DataFrame()
        for j in filename_list:
            df = pd.read_csv(j) 
            if i in df.columns:
                sumbymonth = df.groupby(df['publishedAt'].str[:7])[i].sum()
                res_dict = {i:j for i, j in zip(sumbymonth.index, sumbymonth)}
                res_df = pd.DataFrame(res_dict, index = [j])
                res = res.append(res_df)
            else:
                pass 
        res.to_csv("結果/" + i + ".csv", encoding = "utf-8-sig")
        print(i+"---Finished")
#%% function end        
        

#給定要計算之單詞    
words_list = ["核四", "核電", "以核養綠", "同性婚姻"]
#讀取當前位置的所有頻道csv檔
filename_list = [i for i in os.listdir() if ".csv" in i]
#也可以自行輸入要讀的csv檔名
# filename_list = []

#執行後，計詞頻率結果在「結果」資料夾中
count_words_by_month(words_list, filename_list)
