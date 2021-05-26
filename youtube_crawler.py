##### Introduction #####
# Output will have three folder and multiple csv file 
########################
#   [file structure]   #
# - 頻道列表            #
# -- 各頻道名稱         #
# --- 各影片留言        #
########################

# Author：劉家銘
# Last version：2021/05/26

import requests
import json
import pandas as pd
from datetime import datetime
from tqdm import tqdm, trange
import copy
import pdb
import sys
import API as api  # own function


channels_dict = json.load(open('config/channelDict.json','r+',encoding='utf-8')) # uploadId not channelId 

api.pathControl(channels_dict.keys()) #create directory for each channel 

AUTH_KEY = [ i for i in open('config/key.txt','r+',encoding='utf-8').readlines() ] # Authorization Key



## 上面為不需要修改的部分
if __name__ == '__main__':



    ## 範例一：先爬完所有頻道的所有影片資訊，再逐一爬取各影片留言
    ## Example 1：Get all channel's videos first,and the crawler commentThreads for each video
    for k,v in channels_dict.items():
        api.requset_playlistItems(k,v,AUTH_KEY[0])
    api.get_videoComment(AUTH_KEY[0],channels_dict.keys(),'2016-01-01', '2021-05-31',True)



    ## 範例二：只爬取單一頻道的『影片列表』
    api.requset_playlistItems('少康戰情室','UULZBXiS9ZrIXgKBs_SMfGBQ',AUTH_KEY[0])



    ## 範例三：爬取一個/多個頻道的『所有影片留言』
    # -關於force參數的解釋請詳見共編:https://docs.google.com/document/d/1ds6qbIJ5yAkpkHMP2rin2KWFtkl2YCD2nP-PbmVadGs/edit
    api.get_videoComment(AUTH_KEY[0],['少康戰情室'],'2020-01-01', '2020-12-31',True) #爬取2020年少康戰情室的所有影片的留言
    api.get_videoComment(AUTH_KEY[0],['少康戰情室','關鍵時刻'],'2020-01-01', '2020-12-31',True) #爬取2020年少康戰情室、關鍵時刻的所有影片的留言
    api.get_videoComment(AUTH_KEY[0],channels_dict.keys(),'2020-01-01', '2020-12-31',True) #爬取所有頻道的所有影片留言
    


    ## (Optional)
    ## 範例四：爬取特定支影片所有留言
    api.request_videoComment(AUTH_KEY[0],'WzYNKoWe-xw','頭條開講')