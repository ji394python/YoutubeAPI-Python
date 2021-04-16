# YoutubeAPI-Python
<hr>

### 輸出目錄結構
<pre>
└頻道列表 
  └該頻道影片列表 
     │  ChannelTitle_所有影片列表.csv 
     │  
     └─影片留言 
	      videoId_所有留言列表.csv 
</pre>

<hr>

### 呼叫範例
- `requset_playlistItems(channel_uploadID,AUTH_KEY)`：獲取指定頻道下所有影片資訊
- `request_videoComment(AUTH_KEY,videoID,channelTitle)`：獲取指定影片下所有留言 (包含巢狀留言)
- `get_videoComment(AUTH_KEY,channelTitle,startDate,endDate,force)`：可控制日期的下載所有指定影片留言 (包含巢狀留言)

```python
import API as api
video_df  = api.requset_playlistItems(channelID['新聞面對面'],AUTH_KEY)  
comment_df = api.request_videoComment(AUTH_KEY,'IWsTTZWcUTQ','鄭知道了') 
comment_df = api.get_videoComment(AUTH_KEY,['年代向錢看','關鍵時刻'],'2018-01-01','2018-12-31',False)
```

<hr>

### 輸入參數介紹
- `AUTH_Key`：去Google申請API KEY後再放入
- `channel_uploadID`：注意！此非頻道的ID,而是播放清單的ID，可接受string
	- ![#1589F0](https://via.placeholder.com/15/1589F0/000000?text=+) `建議取影片全部播放的playlistId,仿間上用channelID取playlistID的作法會有少抓影片的邏輯問題`
- ![Image of Yaktocat](https://github.com/ji394python/YoutubeAPI-Python/blob/main/youtube.png)
- `videoID`：找到指定影片ID後再放入，可接受string
- `channelTitle`：放入要抓的頻道名稱，可接受list or string
- `startDate`：查詢日期 (開始)，接受 '%Y-%m-%d' 的格式，例如 '2020-01-01'
- `endDate`：查詢日期 (結束)，接受 '%Y-%m-%d' 的格式，例如 '2020-12-31'
- `force`：是否從上次終止的地方開始爬 (流量控制使用)，接受boolean

<hr>

### 輸出欄位介紹
- `requset_playlistItems()`：輸出該頻道所有影片資訊 "頻道名稱_影片列表.csv" ，以觀看數作為排序
  - channelId：頻道ID
  - channelTitle：頻道名稱
  - titile：影片標題
  - publishAt：發布時間
  - description：影片描述
  - videoId：影片ID
  - viewCount：觀看數
  - likeCount：喜歡數
  - dislikeCount：不喜歡數
  - commentCount：留言總數

- `request_videoComment()`：輸出指定影片所有留言內容 "videoID.csv"，以喜愛數作為排序
  - videoID：影片ID
  - commentID：留言ID
  - commenterChannelID：留言者頻道ID
  - parentID：父留言ID (針對留言中的留言所設計)
  - authorDisplayName：留言者名稱
  - textOriginal：留言內容
  - likeCount：留言喜歡數
  - publishedAt：發布時間
  - updateAt：更新時間
  - totalReplayCount：子留言數量
 

<hr>

### 版本紀錄

- v2.0：新增流量控制的功能：Process.log、ERROR.log、stopRecord.log
  - Process.log：紀錄爬取過程
  - ERROR.log：若發生錯誤時，記錄錯誤原因
  - stopRecord.log：若發生錯誤時，此檔案用來記錄當下在哪一支videoID發生錯誤，以幫助之後從此抓起
