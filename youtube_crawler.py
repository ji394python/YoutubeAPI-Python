import requests
import json
import pandas as pd
from datetime import datetime
from tqdm import tqdm, trange
import copy
import pdb

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
        '新聞挖挖哇': 'UURYM7X1WTLZeFHf4uuqkYCQ',
        '少康戰情室': 'UULZBXiS9ZrIXgKBs_SMfGBQ',
        
        '新聞深喉嚨': 'UUdp5pYDJCpl5WFk3jFEjWHw',
        '國民大會': 'UU1WBRpr2G-NQvm_-jv-i6gg',
        '年代向前看': 'UUBuHkb1AS_yRQ71meFNQ3VQ',
        '新台灣加油': 'UUpmAcCUZtDEZNQWmqwX7DxQ',
        '鄭知道了': 'UULG2sbIo3Rktb77h6q9yuDw',
    }

    # Authorization Key
    AUTH_KEY = "AIzaSyBMr2Fyv59DzYjN-MppVQR-ZmFIYY8Avqs"

    ## Example 1： Get all video from specific channel
    ###############################################################
    # video_df  = api.requset_playlistItems(channel_key,AUTH_KEY) #
    ###############################################################
    video_df  = api.requset_playlistItems(channels_dict['鄭知道了'],AUTH_KEY)

    ## Example 2： Get all comment from specific video
    #################################################################################
    # comment_df = api.request_videoComment(AUTH_KEY,videoId,channelTitle)  #
    #################################################################################
    comment_df = api.request_videoComment(AUTH_KEY,video_df['videoId'][0],'鄭知道了') 


    ## Example 3： Get all channel's video and all video comments at same time
    #################################################################################
    #                                                                               #
    #################################################################################
    for k,v in channels_dict.items():
        video_df  = api.requset_playlistItems(v,AUTH_KEY)
        for row in trange(len(video_df)):
            row = video_df.iloc[row,:]
            channelTitle = row['channelTitle']
            videoId = row['videoId']
            comment_df = api.request_videoComment(AUTH_KEY,videoId,channelTitle) 