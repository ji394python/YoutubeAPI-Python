import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import os
import jieba
from datetime import datetime,timedelta
import checkword as check
from ckiptagger import construct_dictionary
import re
from jieba.analyse import extract_tags 


#%% 讀取播放清單檔案 (讀取影片敘述文字)
def read_videoname(program:str) -> pd.DataFrame:
    files = os.listdir('頻道列表/' + program)
    sch = pd.DataFrame()
    for file in files:
        if '影片列表' in file:
            print(file)
            tt = pd.read_csv('頻道列表/' + program +'/'+ file)
            sch = sch.append(tt)
    sch = sch.reset_index(drop = True)
    return sch
# del file, files, tt

#%% 利用關鍵字篩選相關議題影片(找出影片ID)
def find_video(sch:pd.DataFrame, keyword_list:list) -> pd.DataFrame:
    schres = pd.DataFrame()
    for word in keyword_list:
        # print(word)
        titlecont = sch['title'].str.contains(word) #判斷每格字串是否包含word
        descont = sch['description'].str.contains(word)
        unn = np.logical_or(titlecont, descont).fillna(False)
        if unn.any() == True:
            schres = schres.append(sch.loc[unn, :])
        else:
            pass
    schres = schres.reset_index(drop = True)
    return schres
# del word, words_antiCH, words_American, unn, titlecont, descont

#%% 讀取schres之中的影片ID -> 並輸出該影片所有留言至同一dataframe
def read_videoID(program:str,startDate:str, endDate:str, *args:list) -> pd.DataFrame:
    sch = read_videoname(program)
    sch = select_date(sch,startDate,endDate)
    if len(args) == 0:
        schres = sch
    else:
        keyword_list = [ ee for e in args for ee in e]
        schres = find_video(sch, keyword_list)
        print(schres)
    pathToFind = '頻道列表/' + program 
    files = os.listdir(pathToFind)
    videoId = list(schres['videoId'])
    commRelated = pd.DataFrame()
    i=0
    for file in files:
        if '.' not in file:
            print(file)
            tempFiles = os.listdir(pathToFind + '/' + file)
            for tempFile in tempFiles:
                for Id in videoId:
                    if tempFile.find(Id) != -1: #若該影片沒留言則不會被抓進來算
                        i+=1
                        print(tempFile + str(i))
                        comm = pd.read_csv(pathToFind + '/' + file + '/' + tempFile)
                        commRelated = commRelated.append(comm)
    data = commRelated.drop_duplicates()
    data.reset_index(inplace = True, drop = True)
    return data

# del commRelated, Id, tempFile, tempFiles, file, files, comm, i, pathToFind, videoId
#%%===========================================================================================
#讀入正負情緒詞檔案
def read_keyword_data(*args:str) -> dict:
    
    tmp = dict()
    for wordExcel in args:
        df = pd.read_excel('頻道列表/'+wordExcel +'.xlsx',engine='openpyxl')
        for col in df.columns:
            tmp[col] = np.array(df[col].dropna())
    return tmp

# allsentiword = change_df_to_dict(senti)
# del senti
# #%%把詞庫轉成dictionary
def txt_to_dict(wg:str):
    f = open(wg, "r", encoding="utf-8")
    wg_list = f.read().split()
    wg_dict = {}
    for i in wg_list:
        wg_dict[i] = 1 #所有詞權重假設一樣為1
    return wg_dict

# chip tagger 斷詞使用
#%% 斷詞，並新增[ckipnlp_cut、year、month]三個欄位
def ckipnlp_cutwords(data:pd.DataFrame, ws, *args:str, **kwargs) -> pd.DataFrame:
    wg_dict = {}
    for wordPackage in args:
        wg_dict.update(txt_to_dict('頻道列表/'+wordPackage +'.txt'))
    wg_dict = construct_dictionary(wg_dict)
    data2 = data.copy()
    cut = []
    for text in data['textOriginal']:
        comment_cut = ws([text], recommend_dictionary = wg_dict)[0]
        cut.append(comment_cut)
        print(comment_cut)
        # cut.append(ws([text])[0])
    data2['ckipnlp_cut'] = cut
    year_month_cut(data2)
    if kwargs.get('language'): 
        #若有給language這個keyword參數，就會回傳其value(True or False)，沒有給language這個參數將回傳None，等同於False
        data2['traditional'] = [ 1 if check.hasTraditional(s) else 0 for s in data2['textOriginal']]
        data2['simplified'] = [ 1 if check.hasSimplified(s) else 0 for s in data2['textOriginal']]
        data2['english'] = [ 1 if check.hasEnglish(s) else 0 for s in data2['textOriginal']]
    data2.reset_index(inplace = True, drop = True)
    return data2

# Jieba 斷詞使用
#%% 斷詞，並新增[jieba_cut、year、month]三個欄位
def jieba_cutwords(data:pd.DataFrame, *args:str,**kwargs) -> pd.DataFrame:
    for wordPackage in args:
        jieba.load_userdict('頻道列表/'+wordPackage +'.txt')
    
    data2 = data.copy()
    cut = []
    for text in data['textOriginal']:
        # print(text)
        cut.append(list(jieba.cut(str(text))))
    data2['jieba_cut'] = cut
    year_month_cut(data2)
    if (kwargs.get('language',-1)!= -1):
        if kwargs['language'] == True:
            data2['traditional'] = [ 1 if check.hasTraditional(s) else 0 for s in data2['textOriginal']]
            data2['simplified'] = [ 1 if check.hasSimplified(s) else 0 for s in data2['textOriginal']]
            data2['english'] = [ 1 if check.hasEnglish(s) else 0 for s in data2['textOriginal']]
    data2.reset_index(inplace = True, drop = True)
    return data2

def out_count_df(comment:pd.Series, dict_name:dict) -> pd.DataFrame:
    classword_count = dict()
    for dict_class in dict_name:
        classword_count_temp = pd.DataFrame()
        print(dict_class)
        for word in dict_name[dict_class]:
            L = []
            for content in comment:
                L.append(content.count(word))
            classword_count_temp[word] = L
        classword_count[dict_class] = classword_count_temp.sum(axis = 1)
        print('-----')
    return pd.DataFrame(classword_count)

def seperate_run(data:pd.DataFrame,wordCol:str, allsentiword:dict, group_num:int) -> pd.DataFrame:
    N = len(data[wordCol])
    n = N//group_num
    Res = pd.DataFrame()
    print(N,n)
    for i in range(0, N, n): 
        if i == (group_num-1)*n:
            group = data[wordCol][i:]
            groupRes = out_count_df(group, allsentiword)
            Res = Res.append(groupRes, ignore_index=True)
            break
        else:
            group = data[wordCol][i:(i+n)]
            groupRes = out_count_df(group, allsentiword)
            Res = Res.append(groupRes, ignore_index=True)
    Res.reset_index(inplace = True, drop = True)
    return pd.concat([data, Res], axis = 1)

#%% 擷取年度與日期
def year_month_cut(data2:pd.DataFrame) -> pd.DataFrame:
    data2['year'] = data2['publishedAt'].str[:4]
    data2['month'] = data2['publishedAt'].str[5:7]
    data2['date'] = data2['publishedAt'].str[8:10]
    return data2

#%% 篩選日期
def select_date(Result:pd.DataFrame, startDate:str, endDate:str) -> pd.DataFrame:
    Result = Result.loc[Result['publishedAt'] < str(datetime.strptime(endDate,'%Y-%m-%d')+timedelta(days=1))[:10], :]
    Result = Result.loc[Result['publishedAt'] > startDate, :]
    return Result


def tfidf(program:list,startDate:str,endDate:str) -> pd.DataFrame:
    res = pd.DataFrame()
    for file in program:
        data = read_videoname(file)
        data = select_date(data,startDate,endDate)
        res = pd.concat([res,data],ignore_index=True)
    #TF-IDF
    keywords = extract_tags(' '.join(res.title.str.replace('\n','').values.tolist()), topK=50, withWeight=True, allowPOS=())
    df = pd.DataFrame({'詞':[item[0] for item in keywords] , '分數':[item[1] for item in keywords]})
    return df


def hashtag(program:str,startDate:str,endDate:str) -> pd.DataFrame:
    data = read_videoname(program)
    data = select_date(data,startDate,endDate)
    column = data.description.apply(lambda x: str(x).replace('\n',' ').replace('#',' #').split(' '))
    # titles = data.title.values.tolist()
    # count = 0
    res = []
    for items in column:
        res_temp = []
        for item in items:
            if '#' in item:
                sub = re.findall('[\u4e00-\u9fa5a-zA-Z0-9#]+',item,re.S)
                # print(sub[0])
                res_temp.append(sub[0].lstrip())

                # res_temp.append(item)
        res.append(' '.join(res_temp))
    data['hashtag'] = res
        # count +=1
    return data[['channelId', 'channelTitle', 'title', 'publishedAt', 'description','hashtag',
       'videoId', 'viewCount', 'likeCount', 'dislikeCount', 'commentCount']]

