import requests
import json
import pandas as pd
from datetime import datetime
from tqdm import tqdm, trange
import copy
import pdb
import sys
import API as api  # own function

##### Introduction #####
# Output will have three folder and multiple csv file 
########################
#   [file structure]   #
# - 頻道列表            #
# -- 各頻道名稱         #
# --- 各影片留言        #
########################

if __name__ == '__main__':
    # uploadId not channelId
    channels_dict = {
        '新聞面對面': 'UU8w76cjoqEArF-ns44l_ujA',
        '新聞龍捲風': 'UUMetIbaFeT7AzX1K_YOGEjA',
        '關鍵時刻': 'UUKQVSNdzGBJSXaUmS4TOWww',
        '新聞挖挖哇！': 'UURYM7X1WTLZeFHf4uuqkYCQ',
        '少康戰情室': 'UULZBXiS9ZrIXgKBs_SMfGBQ',

        '新聞深喉嚨': 'UUdp5pYDJCpl5WFk3jFEjWHw',
        '國民大會': 'UU1WBRpr2G-NQvm_-jv-i6gg',
        '年代向前看': 'UUBuHkb1AS_yRQ71meFNQ3VQ',
        '新台灣加油': 'UUpmAcCUZtDEZNQWmqwX7DxQ',
        '鄭知道了': 'UULG2sbIo3Rktb77h6q9yuDw',
    }

    # Authorization Key
    with open('config.txt','r') as f:
        API = [ row.strip() for row in f.readlines()]

    ## 範例一：先爬完所有頻道的所有影片資訊，再逐一爬取各影片留言
    ## Example 1：Get all channel's videos first,and the crawler commentThreads for each video
    for k,v in channels_dict.items():
        api.requset_playlistItems(k,v,AUTH_KEY)

    api.get_videoComment(AUTH_KEY,['新台灣加油'],'2019-07-03', '2019-07-05',False)
