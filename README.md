# YoutubeAPI-Python
<hr>


### [輸出目錄結構]
<pre>
└頻道列表 
  └該頻道影片列表 
     │  ChannelID_所有影片列表.csv 
     │  
     └─影片留言 
	      videoId_所有留言列表.csv 
</pre>

### [輸入]
- Key：去申請後在放入程式檔中
- ChannelID：找到目標頻道ID後再放入
- VideoID：找到指定影片ID後再放入

### [輸出]
- 皆會存成pd.DataFrame
- 預先處理了JSON、日期..etc

### 【呼叫範例】
- requset_playlistItems：獲取指定頻道下所有影片資訊
- request_videoComment：獲取指定影片下所有留言 (包含巢狀留言)
```python
import API as api
video_df  = api.requset_playlistItems(channelID,AUTH_KEY)  
comment_df = api.request_videoComment(AUTH_KEY,videoID,'可自定義的頻道名稱') 
```
