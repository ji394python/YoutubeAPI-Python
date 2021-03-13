import pandas as pd
import requests
import json
from tqdm import tqdm, trange
import os 


# API
playlistItemsAPI = "https://www.googleapis.com/youtube/v3/playlistItems"
commentThreadsAPI = "https://www.googleapis.com/youtube/v3/commentThreads"

## Get youtube api to take all video basic information
## also dataframe save to csv 
def requset_playlistItems(channel_uploadId:str,key:str) -> pd.DataFrame:
    res = []
    params = {
        'key': key, ##我的API KEY
        'part': 'snippet',
        'playlistId': channel_uploadId,
        'maxResults': 50, # max
    }
    try:
        resp = requests.get(playlistItemsAPI, params)
        resp_json = json.loads(resp.text)
        totalResults = resp_json['pageInfo']['totalResults']
        res = get_channel_video_lists(resp_json)

        if totalResults > 50 :
            nextPageToken = resp_json['nextPageToken']
            for page in trange(totalResults//50-1):
                params['pageToken'] = nextPageToken
                resp = requests.get(playlistItemsAPI, params)
                resp_json = json.loads(resp.text)
                res.extend(get_channel_video_lists(resp_json))

                try:
                    nextPageToken = resp_json['nextPageToken']
                except:
                    # No next page
                    break
        
        video_df = pd.DataFrame(res)
        video_df['publishedAt'] = pd.to_datetime(video_df['publishedAt'])
        video_df['publishedAt'] = video_df['publishedAt'].dt.tz_localize(None) # remove timezone

        if not os.path.exists('頻道列表'):
            os.mkdir('頻道列表')
            os.mkdir('頻道列表/%s' %video_df.channelTitle[0])
            video_df.to_csv('頻道列表/%s/%s_影片列表.csv' % (video_df.channelTitle[0],video_df.channelTitle[0]) ,index=False,encoding='utf-8-sig')
        else:
            if not os.path.exists('頻道列表/%s' %video_df.channelTitle[0]):
                os.mkdir('頻道列表/%s' %video_df.channelTitle[0])
                video_df.to_csv('頻道列表/%s/%s_影片列表.csv' % (video_df.channelTitle[0],video_df.channelTitle[0]) ,index=False,encoding='utf-8-sig')
            else:
                video_df.to_csv('頻道列表/%s/%s_影片列表.csv' % (video_df.channelTitle[0],video_df.channelTitle[0]) ,index=False,encoding='utf-8-sig')

        return video_df
    except:
        print(params)

#### Extract data from json file for channel video
def get_channel_video_lists(resp_json:dict) -> list:
    cols = ['channelId','channelTitle','title','publishedAt','description','videoId']
    res = []
    for item in resp_json['items']:
        data = {col:'' for col in cols}
        data['channelId'] = item['snippet']['channelId']
        data['channelTitle'] = item['snippet']['channelTitle']
        data['videoId'] = item['snippet']['resourceId']['videoId']
        data['publishedAt'] = item['snippet']['publishedAt']
        data['title'] = item['snippet']['title']
        data['description'] = item['snippet']['description']
        res.append(data)
        
    return res


## Get youtube api to take all comment for specific videoID
## also dataframe save to csv 
def request_videoComment(key:str,videoID:str,channelTitle:str) -> pd.DataFrame:
    res = []
    params = {
        'key': key, ##我的API KEY
        'part': 'snippet,replies',
        'videoId': videoID,
        'maxResults': 100, # max
    }
    try:
        resp = requests.get(commentThreadsAPI, params)
        resp_json = json.loads(resp.text)
        totalResults = resp_json['pageInfo']['totalResults']
        res = get_video_comment_list(resp_json)
        if  resp_json.get('nextPageToken',-1) != -1:
            nextPageToken = resp_json['nextPageToken']
            for page in trange(totalResults//100-1):
                params['pageToken'] = nextPageToken #到下一頁
                resp = requests.get(commentThreadsAPI, params)
                resp_json = json.loads(resp.text)
                res.extend(get_channel_video_lists(resp_json))

                try:
                    nextPageToken = resp_json['nextPageToken']
                except:
                    # No next page
                    break
        elif totalResults == 0:
            print("【無留言："+videoID+"】")
            return ""

        comment_df = pd.DataFrame(res)
        #print(comment_df,resp_json,params)
        comment_df['publishedAt']  = pd.to_datetime(comment_df['publishedAt'])

        comment_df['publishedAt']  = comment_df['publishedAt'].dt.tz_localize(None) # remove timezone

        if not os.path.exists('頻道列表'):
            os.mkdir('頻道列表')
            os.mkdir('頻道列表/%s' %channelTitle)
            os.mkdir('頻道列表/%s/影片留言' %channelTitle)
            comment_df.to_csv('頻道列表/%s/影片留言/%s.csv' % (channelTitle,videoID) ,index=False,encoding='utf-8-sig')
        else:
            if not os.path.exists('頻道列表/%s' %channelTitle):
                os.mkdir('頻道列表/%s' %channelTitle)
                os.mkdir('頻道列表/%s/影片留言' %channelTitle)
                comment_df.to_csv('頻道列表/%s/影片留言/%s.csv' % (channelTitle,videoID) ,index=False,encoding='utf-8-sig')
            else:
                if not os.path.exists('頻道列表/%s/影片留言' %channelTitle):
                    os.mkdir('頻道列表/%s/影片留言' %channelTitle)
                    comment_df.to_csv('頻道列表/%s/影片留言/%s.csv' % (channelTitle,videoID) ,index=False,encoding='utf-8-sig')
                else:
                    comment_df.to_csv('頻道列表/%s/影片留言/%s.csv' % (channelTitle,videoID) ,index=False,encoding='utf-8-sig')

        return comment_df
    except:
        print(params)


#### Extract data from json file for videoID all comment
def get_video_comment_list(resp_json:dict) -> list:
    cols = ['videoId','commenterId','parentId','authorDisplayName','textOriginal','likeCount','publishedAt','updatedAt','totalReplyCount']
    res = []
    for item in resp_json['items']:
        data = {col:'' for col in cols}
        data['videoId'] = item['snippet']['videoId']
        data['commenterId'] = item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
        data['parentId'] = ''
        data['authorDisplayName'] = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        data['textOriginal'] = item['snippet']['topLevelComment']['snippet']['textOriginal']
        data['likeCount'] = item['snippet']['topLevelComment']['snippet']['likeCount']
        data['publishedAt'] = item['snippet']['topLevelComment']['snippet']['publishedAt']
        data['updatedAt'] = item['snippet']['topLevelComment']['snippet']['updatedAt']
        data['totalReplyCount'] = item['snippet']['totalReplyCount']
        res.append(data)
        if data['totalReplyCount'] > 0:
            for nest_item in item['replies']['comments']:
                nest_data = {col:'' for col in cols}
                nest_data['videoId'] = nest_item['snippet']['videoId']
                nest_data['commenterId'] = nest_item['snippet']['authorChannelId']['value']
                nest_data['parentId'] = data['commenterId']
                nest_data['authorDisplayName'] = nest_item['snippet']['authorDisplayName']
                nest_data['textOriginal'] = nest_item['snippet']['textOriginal']
                nest_data['likeCount'] = nest_item['snippet']['likeCount']
                nest_data['publishedAt'] = nest_item['snippet']['publishedAt']
                nest_data['updatedAt'] = nest_item['snippet']['updatedAt']
                nest_data['totalReplyCount'] = 0 #可以在改善的地方,或可以用Tag來做
                res.append(nest_data)
    return res
