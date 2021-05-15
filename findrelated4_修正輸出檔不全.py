# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 12:55:09 2020

@author: user
"""
'''
******************************注意!!!******************************************
第一次執行請到console下載中研院斷詞系統ckip的python package
語法如下：

pip install -U ckiptagger[tf,gdown]

備註：
1. 中研院斷詞系統會用到機器學習模組tensorflow
2. 中研院斷詞系統因為使用深度學習模型，所以執行速度較jieba慢上不少
******************************************************************************
'''
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import os
import jieba
from ckiptagger import WS
import TermFreq as cut


#%% 製作計數表
words_antiCH = ['送中', '香港', '黑警', '香港警察', '暴徒', '中共', '香港民運', 
                '反送中', '示威', '鎮壓', '一國兩制', '統一', '今日香港、明日台灣', 
                '連儂牆', '捍衛台灣', '民主自由', '港獨', '台獨', '亂民', 
                '九二共識', '一中各表', '台灣認同', '芒果乾', '賣台', '惠台條款', 
                '台商', '兩岸經貿', '陸客', '自由行', '小三通', '南向政策']

# words_American = ['川普', '特朗普', '拜登', '美國', '美帝', '總統大選']
#program_list = ["年代向錢看", "新台灣加油", "鄭知道了"]
program_list = ["新聞面對面"]

    
#<jieba版>以關鍵字篩選頻道留言至一個excel，再進行jieba斷詞分析    
for program in program_list:
    data = cut.read_videoID(program, words_antiCH) #讀取該頻道下所有符合篩選字的video
    dataFilter = cut.select_date(data, '2019-03-29', '2020-01-11') #篩選日期
    allissueword = cut.read_keyword_data("issue","party","senti") #載入需要的詞庫
    dataSegment = cut.jieba_cutwords(data,"issueword","partyword","sentiword",language=True) #載入需要的詞庫.txt

    #計算詞頻的function [要被計算詞頻的dataframe,斷詞的欄位名稱,需要被計算的詞庫,都設100]
    Result = cut.seperate_run(dataSegment,'jieba_cut', allissueword, 100)

    #%% 轉出Excel檔
    df = pd.DataFrame(Result)
    df.reset_index(inplace = True, drop = True)
    df.to_csv("[斷詞結果]"+program+".csv",encoding='utf-8-sig')
    #%% 結束語法

#<ckip版>以關鍵字篩選頻道留言至一個excel，再以中研院ckip進行斷詞分析
ws = WS(".\data")
for program in program_list:
    data = cut.read_videoID(program, words_antiCH) #讀取該頻道下所有符合篩選字的video  
    dataFilter = cut.select_date(data,'2019-03-29', '2020-01-11') #篩選日期
    allissueword = cut.read_keyword_data("issue","party","senti") #載入需要的詞庫
    dataSegment = cut.ckipnlp_cutwords(dataFilter, ws, "issueword", "partyword", "sentiword",language=True) #載入需要的詞庫.txt
    
    #計算詞頻的function [要被計算詞頻的dataframe,斷詞的欄位名稱,需要被計算的詞庫,都設100]
    Result = cut.seperate_run(dataSegment, 'ckipnlp_cut', allissueword, 100)

    #%% 轉出Excel檔
    df2 = pd.DataFrame(Result)
    df2.reset_index(inplace = True, drop = True)
    df2.to_csv("[ckip斷詞結果]"+program+".csv",encoding='utf-8-sig')