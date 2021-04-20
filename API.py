import pandas as pd
import requests
import json
from tqdm import tqdm, trange
import os 
import traceback
import sys 
import log_manager as log
import time
from datetime import datetime,timedelta

# API
playlistItemsAPI = "https://www.googleapis.com/youtube/v3/playlistItems"
commentThreadsAPI = "https://www.googleapis.com/youtube/v3/commentThreads"
videoAPI = "https://www.googleapis.com/youtube/v3/videos"


## Get youtube api to take all video basic information
## also dataframe save to csv 
def requset_playlistItems(chaneel_name:str,channel_uploadId:str,key:str) -> pd.DataFrame:
    '''
        利用播放清單的ID去取得該播放清單下的所有影片
    '''
    log.processLog('========================================================')
    log.processLog(f'[{chaneel_name}] 開始爬取所有影片')
    log.processLog(f'[{chaneel_name}] 執行requset_playlistItems()')
    res = [] 
    params = {
        'key': key, ##你的API KEY
        'part': 'snippet',
        'playlistId': channel_uploadId,
        'maxResults': 50, # max
    }
    log.processLog(f'[{chaneel_name}] 本次初始參數{json.dumps(params)}')
    try:
        resp = requests.get(playlistItemsAPI, params)
        resp_json = json.loads(resp.text)
        totalResults = resp_json['pageInfo']['totalResults']
        log.processLog(f'[{chaneel_name}] 共有{totalResults}支影片')  
        res = get_channel_video_lists(resp_json)
        log.processLog(f'[{chaneel_name}] 開始爬取影片基本資訊')  
        log.processLog(f'-----> 第1~{len(res)}支影片 Done <-----')
        if totalResults > 50 :
            nextPageToken = resp_json['nextPageToken']
            for page in trange(totalResults//50):
                lenBefore = len(res)
                params['pageToken'] = nextPageToken
                resp = requests.get(playlistItemsAPI, params)
                resp_json = json.loads(resp.text)
                res.extend(get_channel_video_lists(resp_json))
                try:
                    nextPageToken = resp_json['nextPageToken']
                except:
                    log.processLog(f'-----> 第{lenBefore+1}~{len(res)}支影片 Done <-----')
                    # No next page
                    break
                log.processLog(f'-----> 第{lenBefore+1}~{len(res)}支影片 Done <-----')
                
        
        video_df = pd.DataFrame(res)
        video_df['publishedAt'] = pd.to_datetime(video_df['publishedAt'])
        video_df['publishedAt'] = video_df['publishedAt'].dt.tz_localize(None) # remove timezone
        
        ## Get Video Statistic
        log.processLog(f'[{chaneel_name}] 開始爬取影片統計資訊')  
        viewCount,likeCount,dislikeCount,commentCount = [],[],[],[]
        
        for row in trange(len(video_df)//40):
            string = ','.join(video_df['videoId'].values[40*row:40*(row+1)])
            resp_statistic_json = request_videoStatistic(key,string)
            lenViewBefore = len(viewCount)
            for item in resp_statistic_json:
                viewCount.append(item['statistics'].get('viewCount',-1))
                likeCount.append(item['statistics'].get('likeCount',-1))
                dislikeCount.append(item['statistics'].get('dislikeCount',-1))
                commentCount.append(item['statistics'].get('commentCount',-1))
            log.processLog(f'-----> 第{lenViewBefore+1}~{len(viewCount)}支影片 Done <-----')
            

        string = ','.join(video_df['videoId'].values[40*(len(video_df)//40):])
        resp_statistic_json = request_videoStatistic(key,string)
        lenViewBefore = len(viewCount)
        for item in resp_statistic_json:
            viewCount.append(item['statistics'].get('viewCount',-1))
            likeCount.append(item['statistics'].get('likeCount',-1))
            dislikeCount.append(item['statistics'].get('dislikeCount',-1))
            commentCount.append(item['statistics'].get('commentCount',-1))
        log.processLog(f'-----> 第{lenViewBefore+1}~{len(viewCount)}支影片 Done <-----')
        video_df['viewCount'] = viewCount
        video_df['likeCount'] = likeCount
        video_df['dislikeCount'] = dislikeCount
        video_df['commentCount'] = commentCount

        ## Check Path
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
        log.processLog('--------------------------------------------------------')
        return video_df
    except:
        log.processLog(f'[{chaneel_name}]  執行 requset_playlistItems() 發生錯誤，請查看錯誤LOG檔')

        log.errorLog('====================================================')
        log.errorLog(f'[{chaneel_name}] 錯誤函式:requset_playlistItems()')
        log.errorLog('【錯誤參數】')
        log.errorLog(log.processLog(json.dumps(params,indent=4)))
        log.errorLog('【錯誤訊息】')
        log.errorLog(traceback.print_exc())
        log.errorLog('----------------------------------------------------')
        return video_df
    
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


def request_videoStatistic(key:str,video_ID:str) -> dict:
    params_statistic = {
            'key': key,
            'part':'statistics',
            'id':video_ID
        }
    resp_statistic = requests.get(videoAPI, params_statistic)
    resp_statistic_json = json.loads(resp_statistic.text)
    return resp_statistic_json['items']

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
        res.extend(get_video_comment_list(resp_json))

        while resp_json.get('nextPageToken',-1) != -1:
            params['pageToken'] = resp_json['nextPageToken'] #到下一頁
            resp = requests.get(commentThreadsAPI, params)
            resp_json = json.loads(resp.text)
            res.extend(get_video_comment_list(resp_json))


        comment_df = pd.DataFrame(res)
        #print(comment_df,resp_json,params)
        if 'publishedAt' not in comment_df.columns:
            log.processLog(f"=== {videoID}：沒有任何留言 ===")
        else:
            comment_df['publishedAt']  = pd.to_datetime(comment_df['publishedAt'])

            comment_df['publishedAt']  = comment_df['publishedAt'].dt.tz_localize(None) # remove timezone
            comment_df.sort_values('likeCount',ascending=False,inplace=True)
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
        traceback.print_exc()
        return comment_df


#### Extract data from json file for videoID all comment
def get_video_comment_list(resp_json:dict) -> list:
    cols = ['videoId','commentId','commenterChannelId','parentId','authorDisplayName','textOriginal','likeCount','publishedAt','updatedAt','totalReplyCount']
    res = []
    for item in resp_json['items']:
        data = {col:'' for col in cols}
        data['videoId'] = item['snippet']['videoId']
        data['commentId'] = item['snippet']['topLevelComment']['id']
        data['commenterChannelId'] = '' if item['snippet']['topLevelComment']['snippet'].get('authorChannelId',-1) == -1 else item['snippet']['topLevelComment']['snippet']['authorChannelId']['value'] 
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
                nest_data['commentId'] = nest_item['snippet']['authorChannelId']['value']
                nest_data['commenterChannelId'] = nest_item['snippet']['authorChannelId']['value']
                nest_data['parentId'] = data['commentId']
                nest_data['authorDisplayName'] = nest_item['snippet']['authorDisplayName']
                nest_data['textOriginal'] = nest_item['snippet']['textOriginal']
                nest_data['likeCount'] = nest_item['snippet']['likeCount']
                nest_data['publishedAt'] = nest_item['snippet']['publishedAt']
                nest_data['updatedAt'] = nest_item['snippet']['updatedAt']
                nest_data['totalReplyCount'] = 0 #可以在改善的地方,或可以用Tag來做
                res.append(nest_data)
    return res



def get_videoComment(key:str,titleList:list,startDate:str,endDate:str,force:bool)-> pd.DataFrame:
    log.processLog('========================================================')
    log.processLog('========================================================')
    log.processLog(f'開始執行get_videoComment()')
    dd = {'Auth_key':key,'查詢頻道':titleList,'查詢開始日期':startDate,'查詢終止日期':endDate,'強制重來':force}
    log.processLog(f"本次查詢參數：{dd}")
    log.processLog(f"Step1: 判斷前次是否有遇到流量限制的問題：{os.path.exists('log/stopRecord.log')}")
    log.processLog(f"Step2: 是否從前次停止的地方開始：{force}")
    titleList = list(titleList)
    if ((os.path.exists('log/stopRecord.log') == False) | (force)):
        for title in titleList:
            df = pd.read_csv('頻道列表/'+title+'/'+title+'_影片列表.csv')
            channelTitle = df['channelTitle'].values[0]
            data = df[(df.publishedAt >= startDate) & (df.publishedAt <= endDate)]
            log.processLog(f'[{channelTitle}] 頻道影片總數: {len(df)}')
            log.processLog(f'[{channelTitle}] 指定時間內影片總數: {len(data)}')
            log.processLog(f'[{channelTitle}] 本次需爬影片數: {len(data)}')
            log.processLog(f'[{channelTitle}] 開始爬取影片留言')
            try:
                for index in trange(len(data)):
                    row = data.iloc[index,:]
                    videoId = row['videoId']
                    comment_df = request_videoComment(key,videoId,channelTitle)
                    log.processLog(f'[{channelTitle}] 第{index}支影片留言:{videoId} Done')
                log.processLog('--------------------------------------------------------')
                return comment_df
            except:
                log.processLog(f'[{channelTitle}]  執行 get_videoComment() 發生錯誤，請查看錯誤LOG檔')

                log.errorLog('====================================================')
                log.errorLog(f'[{channelTitle}] 錯誤函式:get_videoComment()')
                log.errorLog(f'【錯誤影片ID】{videoId}')
                log.errorLog('【錯誤訊息】')
                log.errorLog(traceback.print_exc())
                log.errorLog('--------------------------------------------------------')
                record_time = time.strftime("%Y%m%d %H:%M:%S")
                with open('log/stopRecord.log','a+',encoding='utf-8') as f:
                    f.write('--------------------------------------------------------'+'\n')
                    f.write(f'{record_time}:終止程序，紀錄最後資訊'+"\n")
                    f.write(f'{record_time}:若要看為何中止請查看errorLog'+"\n")
                    para = {'頻道名稱':channelTitle, '影片ID':videoId
                    ,'查詢開始時間':startDate,'查詢截止時間':endDate}
                    f.write(f"{json.dumps(para,ensure_ascii=False)}"+'\n')
                    f.close()
                return comment_df
    else:
        with open('log/stopRecord.log','r',encoding='utf-8') as f:
            for readline in f.readlines():
                if readline.find('頻道名稱') != -1:
                    s = json.loads(readline)
        log.processLog(f"Step3：取得前次進度儲存進度 {s}")
        log.processLog(f"Step4：進入VideoID比對程序")
        titleIndex = titleList.index(s['頻道名稱'])
        for title in titleList[titleIndex:]:
            df = pd.read_csv('頻道列表/'+title+'/'+title+'_影片列表.csv')
            channelTitle = df['channelTitle'].values[0]
            data = df[(df.publishedAt >= startDate) & (df.publishedAt <= str(datetime.strptime(endDate,'%Y-%m-%d')+timedelta(days=1))[:10] )]
            if data['videoId'].values.tolist().count(s['影片ID']) == 1:
                videoIDStart = data['videoId'].values.tolist().index(s['影片ID']) 
            else:
                videoIDStart = 0
            log.processLog(f'[{channelTitle}] 頻道影片總數: {len(df)}')
            log.processLog(f'[{channelTitle}] 指定時間內影片總數: {len(data)}')
            log.processLog(f'[{channelTitle}] 本次需爬影片數: {len(data)-videoIDStart}')
            log.processLog(f'[{channelTitle}] 開始爬取影片留言')
            # log.processLog(f'{data.columns}')
            # log.processLog(f'{data.head(5)}')
            try:
                for index in trange(len(data)):
                    if index < videoIDStart:
                        continue
                    row = data.iloc[index,:]
                    videoId = row['videoId']
                    comment_df = request_videoComment(key,videoId,channelTitle)
                    log.processLog(f'[{channelTitle}] 第{index}支影片留言:{videoId} Done')
                log.processLog('--------------------------------------------------------')
                return comment_df
            except:
                log.processLog(f'[{channelTitle}]  執行 get_videoComment() 發生錯誤，請查看錯誤LOG檔')

                log.errorLog('====================================================')
                log.errorLog(f'[{channelTitle}] 錯誤函式:get_videoComment()')
                log.errorLog(f'【錯誤影片ID】{videoId}')
                log.errorLog('【錯誤訊息】')
                log.errorLog(traceback.print_exc())
                log.errorLog('--------------------------------------------------------')
                record_time = time.strftime("%Y%m%d %H:%M:%S")
                with open('log/stopRecord.log','a+',encoding='utf-8') as f:
                    f.write('--------------------------------------------------------'+'\n')
                    f.write(f'{record_time}:終止程序，紀錄最後資訊'+"\n")
                    f.write(f'{record_time}:若要看為何中止請查看errorLog'+"\n")
                    para = {'頻道名稱':channelTitle, '影片ID':videoId
                    ,'查詢開始時間':startDate,'查詢截止時間':endDate}
                    f.write(f"{json.dumps(para,ensure_ascii=False)}"+'\n')
                    f.close()
                return comment_df
            

