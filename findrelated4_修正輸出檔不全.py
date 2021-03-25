# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 12:55:09 2020

@author: user
"""

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import os
import jieba
import jiebaCut as jj

#%% 製作計數表
words_antiCH = ['送中', '香港', '黑警', '香港警察', '暴徒', '中共', '香港民運', 
                '反送中', '示威', '鎮壓', '一國兩制', '統一', '今日香港、明日台灣', 
                '連儂牆', '捍衛台灣', '民主自由', '港獨', '台獨', '亂民', 
                '九二共識', '一中各表', '台灣認同', '芒果乾', '賣台', '惠台條款', 
                '台商', '兩岸經貿', '陸客', '自由行', '小三通', '南向政策']

# words_American = ['川普', '特朗普', '拜登', '美國', '美帝', '總統大選']
#program_list = ["年代向錢看", "新台灣加油", "鄭知道了"]
program_list = ["新聞面對面_part"]

for program in program_list:
    data = jj.read_videoID(program, words_antiCH)
    dataFilter = jj.select_date(data,'2020-01-11', '2019-03-29') #篩選日期
    allissueword = jj.read_keyword_data("party","senti") #載入需要的詞庫
    dataSegment = jj.jieba_cutwords(data, "partyword","sentiword") #載入需要的詞庫.txt

    Result = jj.seperate_run(dataSegment,'jieba_cut', allissueword, 100)
    #%% 轉出Excel檔
    df = pd.DataFrame(Result)
    df.reset_index(inplace = True, drop = True)
    df.to_excel("關鍵字/"+program+".xlsx")
    #%% 結束語法


