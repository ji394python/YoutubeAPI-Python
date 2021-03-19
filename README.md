# YoutubeAPI-Python
<hr>

### 輸出目錄結構
<pre>
└頻道列表 
  └該頻道影片列表 
     │  ChannelID_所有影片列表.csv 
     │  
     └─影片留言 
	      videoId_所有留言列表.csv 
</pre>

<hr>

### 呼叫範例
- `requset_playlistItems(channel_uploadID,AUTH_KEY)`：獲取指定頻道下所有影片資訊
- `request_videoComment(AUTH_KEY,videoID,channelTitle)`：獲取指定影片下所有留言 (包含巢狀留言)

```python
import API as api
video_df  = api.requset_playlistItems(channelID,AUTH_KEY)  
comment_df = api.request_videoComment(AUTH_KEY,videoID,channelTitle) 
```

<hr>

### 輸入參數介紹
- AUTH_Key：去Google申請API KEY後再放入
- Channel_uploadID：注意！此非頻道的ID,而是播放清單的ID (建議取影片全部播放的playlistId,仿間上用channelID取playlistID的作法會有少抓影片的邏輯問題)
- ![Image of Yaktocat](https://github.com/ji394python/YoutubeAPI-Python/blob/main/youtube.png)
- VideoID：找到指定影片ID後再放入 

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
  - parentID：父留言ID (針對留言中的流言所設計)
  - authorDisplayName：留言者名稱
  - textOriginal：留言內容
  - likeCount：留言喜歡數
  - publishedAt：發布時間
  - updateAt：更新時間
  - totalReplayCount：子留言數量

<hr>
