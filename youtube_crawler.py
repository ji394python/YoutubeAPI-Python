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
        'HelloCatie':'UUxls4ftUSbEcrDR1zQWIwfA',
        'ImCharlie': 'UUyD3eaCai2yyWZEuczgZ-fw',
        'GINAHELLO!': 'UUSR9CHNMIg7YoNezbv4bh0A',
        'TheKellyYang': 'UUZxPrEAHOkNdS2FkaLIGniw',
        'SHOPAHOLIC凱利依法': 'UUwVuFOcZMZqxvxU40WkJhAg'
    }

    # Authorization Key
    AUTH_KEY = "Your Key"

    # ## Example 1： Get all video from specific channel
    for i in channels_dict.keys():
        video_df  = api.requset_playlistItems(channels_dict[i],AUTH_KEY)

    # ## Example 2： Get all comment from specific video
    # comment_df = api.request_videoComment(AUTH_KEY,video_df['videoId'][0],'鄭知道了') 

    ## Example 3： Get all channel's video and all video comments at same time
    for k,v in channels_dict.items():
        video_df  = api.requset_playlistItems(v,AUTH_KEY)
        for row in trange(len(video_df)):
            row = video_df.iloc[row,:]
            channelTitle = row['channelTitle']
            videoId = row['videoId']
            comment_df = api.request_videoComment(AUTH_KEY,videoId,channelTitle) 
