from collections import defaultdict
from datetime import datetime
import pandas as pd
import googleapiclient.discovery
import threading
from threading import *

#assign database information
host="Enter databse host address"
user="user name"
password="password"
database_name="youtube_harvest"
port=Port name
youtube1=googleapiclient.discovery.build("youtube", "v3", developerKey="Enter Youtube API developer Key")
video_id=defaultdict(list)
channel_data1=defaultdict(list)
tb_name=["channel_data","video_data","comment_data"]
global video_data1,comment_data1
#function for video duration convert to time format
def duration(dur):
    fduration = str(pd.Timedelta(dur)).split()[-1]
    return fduration
#function for date and time to datetime format
def date(dt):
    dt_object = datetime.fromisoformat(dt.replace('Z', '+00:00'))
    date_time=dt_object.strftime("%Y-%m-%d %H:%M:%S")
    return date_time
#search channel name or id differenciate
def input_find(channel_id):
    channelid = youtube1.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id).execute()
    channelname = youtube1.search().list(
                        q=channel_id,
                        part='snippet',
                        type='channel',
                        maxResults=1
                            ).execute()
    if len(channel_id)==24 and all(c in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_' for c in channel_id):
        if "items" in channelid:
            thread(channel_id)
        elif len(channelname["items"])!=0:
            chan_id1=channelname["items"][0]["snippet"]["channelId"]
            thread(chan_id1)
    elif len(channelname["items"])!=0:
        chan_id2=channelname["items"][0]["snippet"]["channelId"]
        thread(chan_id2)

#Function for get channel information               
def data_channel(d_channel_id):
    channelid = youtube1.channels().list(
        part="snippet,contentDetails,statistics",
        id=d_channel_id).execute()
    channel_data1["id"]=[d_channel_id]
    channel_data1["c_name"]=[channelid["items"][0]["snippet"]["title"]]
    channel_data1["c_subscriber"]=[int(channelid["items"][0]["statistics"]["subscriberCount"])]
    channel_data1["c_views"]=[int(channelid["items"][0]["statistics"]["viewCount"])]
    channel_data1["c_description"]=[channelid["items"][0]["snippet"]["description"]]
    channel_data1["c_publish"]=[date(channelid["items"][0]["snippet"]["publishedAt"])]
    channel_data1["c_dp"]=[channelid["items"][0]["snippet"]["thumbnails"]["medium"]["url"]]
    video_list(d_channel_id)
# function for video information       
def get_video(videoid1):       
    videos_1 = youtube1.videos().list(
        part='snippet,statistics,contentDetails', 
        id=videoid1).execute()
    url=f"https://www.youtube.com/watch?v={videoid1}"
    id1=f'{videoid1}'
    c_id=videos_1["items"][0]["snippet"]["channelId"]
    v_title=videos_1["items"][0]["snippet"]["localized"]["title"]
    dur=duration(videos_1["items"][0]["contentDetails"]["duration"])
    try:
        views=int(videos_1["items"][0]["statistics"]["viewCount"])
    except:
        views=0
    try:
        likes=int(videos_1["items"][0]["statistics"]["likeCount"])
    except:
        likes=0
    favourite_count=int(int(videos_1["items"][0]["statistics"]["favoriteCount"]))
    try:
        comment_count=int(videos_1["items"][0]["statistics"]["commentCount"])
        data_comments(videoid1)
    except:
        comment_count=0
    try:
        des=videos_1["items"][0]["snippet"]["description"]
    except:
        des="Nil"
    publishded= date(videos_1["items"][0]["snippet"]["publishedAt"])
    thimbnail=videos_1["items"][0]["snippet"]["thumbnails"]["default"]["url"]
    video_data1["id"].append(id1)
    video_data1["c_id"].append(c_id)
    video_data1["v_name"].append(v_title)
    video_data1["v_description"].append(des)
    video_data1["V_publish"].append(publishded)
    video_data1["view_count"].append(views)
    video_data1["like_count"].append(likes)
    video_data1["favourite_count"].append(favourite_count)
    video_data1["comment_count"].append(comment_count)
    video_data1["duration"].append(dur)
    video_data1["thumbnail"].append(thimbnail)
    video_data1["v_url"].append(url)
#Function for get total video ID    
def video_list(channel_id):
    global comment_data1
    comment_data1=defaultdict(list) 
    global video_data1
    video_data1=defaultdict(list)
    pg_token1=""
    upload = youtube1.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id).execute()
    uploads=upload["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    while True:
        playid=youtube1.playlistItems().list(
                part='contentDetails',
                playlistId=uploads,
                maxResults=100,
                pageToken=pg_token1).execute()
        v_data=playid["items"]
        for v in range(0,len(v_data)):
            id_video1=v_data[v]["contentDetails"]["videoId"]
            get_video(id_video1)
            pg_token1=playid.get("nextPageToken")
        if not pg_token1:
            break
#function for get comments data           
def data_comments(id_video):
    comments = youtube1.commentThreads().list(
        part='id, snippet',
        videoId=id_video,
        maxResults=100).execute()
    for c in range(0,len(comments["items"])):
        comment_data1["id"].append(comments['items'][c]['id'])
        comment_data1["v_id"].append(id_video)
        comment_data1["c_id"].append(comments['items'][c]['snippet']['channelId'])
        comment_data1["comment_text"].append(comments['items'][c]['snippet']['topLevelComment']['snippet']['textOriginal'])
        comment_data1["comment_author"].append(comments['items'][c]['snippet']['topLevelComment']['snippet']['authorDisplayName'])
        comment_data1["comment_published"].append(date(comments['items'][c]['snippet']['topLevelComment']['snippet']['publishedAt']))
def thread(c_id):
    th1=threading.Thread(target=data_channel(c_id))
    th2=threading.Thread(target=video_list(c_id))
    th1.start
    th2.start
    th1.join
    th2.join
    
