from Home import*
sl.set_page_config(layout="wide")
db=pd.read_sql_query("""SELECT * FROM channel_data""",engine.connect())
dbv=pd.read_sql_query(f'SELECT * FROM video_data',con=engine.connect())
dbc=pd.read_sql_query(f'SELECT * FROM comment_data',con=engine.connect())
dbc=pd.DataFrame(db) 
video_db=pd.DataFrame(dbv)
question=["1.What are the names of all the videos and their corresponding channels?",
          "2.Which channels have the most number of videos, and how many videos do they have?",
            "3.What are the top 10 most viewed videos and their respective channels?",
            "4.How many comments were made on each video, and what are their corresponding video names?",
            "5.Which videos have the highest number of likes, and what are their corresponding channel names?",
            "6.What is the total number of likes for each video, and what are their corresponding video names?",
            "7.What is the total number of views for each channel, and what are their corresponding channel names?",
            "8.What are the names of all the channels that have published videos in the year 2022?",
            "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?",
            "10.Which videos have the highest number of comments, and what are their corresponding channel names?"
          ]
q=sl.selectbox(label="choose Question",options=question,index=None,placeholder="Choose question")   
if q==question[0]:
    data=pd.DataFrame(pd.read_sql_query("SELECT v_name, channel_data.c_name FROM video_data INNER JOIN channel_data on channel_data.id = video_data.c_id",con=engine.connect()))
    coun=((len(data)+1)*35)+3
    sl.dataframe(data,width=1500,height=coun,hide_index=True)
elif q==question[1]:
    j=(pd.DataFrame(((video_db.c_id).value_counts()))).sort_values(by="count",ascending=False)
    k=j.idxmax(0)[0]
    v=(j.values[0])[0]
    sl.subheader(f'In database channel name of most no of videos uploaded is {(dbc["c_name"].values[dbc["id"]==k])[0]} and its have {v} videos') 
elif q==question[2]:
    sort=video_db.sort_values(by="view_count",ascending=False)
    video,channel=sl.columns([1,3])
    url=(sort["v_url"].head(10)).values
    name_of_video=(sort["v_name"].head(10)).values
    name=(sort["c_id"].head(10)).values
    nn=[]
    count=(sort["view_count"].head(10)).values
    for i in name:
        nn.append((dbc["c_name"][dbc["id"]==i]).iloc[0])
    dd=pd.DataFrame({"url":url,"video_name":name_of_video,"name":name,"cname":nn,"viewcoun":count})
    one,two,three,four=sl.columns([1,1,1,1])
    iteration={"one":[1,2,3],"two":[4,5,6],"three":[7,8,9]}
    for i in range(0,10):
        sl.write(f'<p style="text-align:center; color: red; text-transform:uppercase; border-style: solid;">{dd["video_name"][i]}</p>',unsafe_allow_html=True)
        sl.video(dd["url"][i])
        sl.write(f'<p style="text-align:center; color: red; text-transform:uppercase; ">{dd["cname"][i]}<i class="fa-solid fa-eye" style="color: #ea2c0b;"></i>{dd["viewcoun"][i]}</p>',unsafe_allow_html=True)
elif q==question[3]:
     cmc=pd.read_sql_query(f'SELECT v_id,video_data.v_name,count(*) as Comment_Count FROM comment_data inner join video_data on comment_data.v_id=video_data.id group by v_id',con=engine.connect())
     coun=((len(cmc)+1)*35)+3
     sl.dataframe(cmc,width=1500,height=coun,hide_index=True)   
elif q==question[4]:
    vd=video_db.sort_values(by="like_count",ascending=False)
    sl.write(f'Name of the video is {(vd["v_name"].head(1)).iloc[0]} is got {(vd["like_count"].head(1)).iloc[0]} likes in the channel name of {((dbc["c_name"][dbc.id==(vd["c_id"].head(1)).iloc[0]]).iloc[0])} ')
    sl.write("Video is Below")
    sl.video((vd["v_url"].head(1)).iloc[0] )
elif q==question[5]:
    lik=video_db[["id","v_name","like_count"]]
    coun=((len(lik)+1)*35)+3
    sl.dataframe(lik,width=1500,height=coun,hide_index=True)
elif q==question[6]:
    lik=dbc[["id","c_name","c_views"]]
    coun=((len(lik)+1)*35)+3
    sl.dataframe(lik,width=1500,height=coun,hide_index=True)
elif q==question[7]:
    opt=(video_db["V_publish"].dt.year).values
    option=[]
    for i in opt:
        if i not in option:
            option.append(i)
    select_year=sl.selectbox(label="Select Year",options=option,index=None,placeholder="Select Year")   
    if select_year:
        v_year=pd.DataFrame(video_db[["c_id","v_name","V_publish"]][(video_db["V_publish"].dt.year)==select_year])
        vv_year=pd.merge(v_year,dbc,left_on='c_id',right_on='id',how="inner")
        coun=((len(vv_year)+1)*35)+3
        sl.dataframe(vv_year[["c_id","c_name","v_name","V_publish"]],width=1500,height=coun,hide_index=True)
elif q==question[8]:
    tm=pd.DataFrame(pd.read_sql_query("SELECT video_data.c_id,channel_data.c_name,SEC_TO_TIME(round(AVG(TIME_TO_SEC(duration)))) AS Average_video_duration from video_data inner join channel_data on video_data.c_id=channel_data.id group by c_id",con=engine.connect()))
    sl.write(f'<p>{tm.to_html()}</p>',unsafe_allow_html=True)
elif q==question[9]:
    cmc=pd.read_sql_query(f'SELECT v_id,video_data.v_name,video_data.c_id,channel_data.c_name,count(*) as count FROM comment_data inner join video_data on comment_data.v_id=video_data.id inner join channel_data on video_data.c_id=channel_data.id  group by v_id',con=engine.connect())
    cmd=cmc.sort_values(by="count",ascending=False)
    jj=cmd.head(1)
    rr=(cmd[cmd["count"]==jj["count"].iloc[0]])
    coun=((len(rr)+1)*35)+3
    sl.dataframe(rr,width=1500,height=coun,hide_index=True)
