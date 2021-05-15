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


channels_dict = json.load(open('config/channelDict.json','r+',encoding='utf-8')) # uploadId not channelId 

api.pathControl(channels_dict.keys()) #create directory for each channel 

AUTH_KEY = [ i for i in open('config/key.txt','r+',encoding='utf-8').readlines() ] # Authorization Key



## 上面為不需要修改的部分
if __name__ == '__main__':
    ## 範例一：先爬完所有頻道的所有影片資訊，再逐一爬取各影片留言
    ## Example 1：Get all channel's videos first,and the crawler commentThreads for each video
    for k,v in channels_dict.items():
        api.requset_playlistItems(k,v,AUTH_KEY)

    api.get_videoComment(AUTH_KEY,['關鍵時刻'],'2010-01-03', '2021-05-05',False)
