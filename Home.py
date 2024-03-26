from youtube import*
from Mysql import *
import streamlit as sl
import youtube
sl.set_page_config(layout="wide")

sl.title("Youtube Data Harvesting")

sl.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">',unsafe_allow_html=True)

if "CHANNEL_ID" not in sl.session_state:
    sl.session_state["CHANNEL_ID"]=""
if "name_of_the_channel" not in sl.session_state:
    sl.session_state["name_of_the_channel"]=""
if "subcriber" not in sl.session_state:
    sl.session_state["subcriber"]=""
if "views" not in sl.session_state:
    sl.session_state["views"]=""
if "dp" not in sl.session_state:
    sl.session_state["dp"]=""
if "vd" not in sl.session_state:
    sl.session_state["vd"]=""
if "cd" not in sl.session_state:
    sl.session_state["cd"]=""
if "cm" not in sl.session_state:
    sl.session_state["cm"]=""
if "vd1" not in sl.session_state:
    sl.session_state["vd1"]=""
if "vd2" not in sl.session_state:
    sl.session_state["vd2"]=""
if "pub" not in sl.session_state:
    sl.session_state["pub"]=""
if "lk1" not in sl.session_state:
    sl.session_state["lk1"]="" 
if "lk2" not in sl.session_state:
    sl.session_state["lk2"]=""  
if "vc1" not in sl.session_state:
    sl.session_state["vc1"]="" 
if "vc2" not in sl.session_state:
    sl.session_state["vc2"]=""  
def reset():
    sl.session_state["CHANNEL_ID"]=""
    sl.session_state["name_of_the_channel"]=""
    sl.session_state["subcriber"]=""
    sl.session_state["views"]=""
    sl.session_state["dp"]=""
    sl.session_state["vd"]=""
    sl.session_state["cd"]=""
    sl.session_state["cm"]=""
    sl.session_state["vd1"]=""
    sl.session_state["vd2"]=""
    sl.sessionstate["pub"]=""
rr=sl.text_input("Enter Channel ID or Channel Name")
sl.session_state["CHANNEL_ID"]=rr
cid=sl.session_state["CHANNEL_ID"]
#search=sl.button(label="search") 
i,col1, col2, col3,u= sl.columns([1,0.5,0.5,1,1]) 
with col1:
    search=sl.button(label="Search")
with col2:
    clear=sl.button(label="Clear")
with col3:
    p_database=sl.button(label="Push to Database")
 
if search:
    if sl.session_state["CHANNEL_ID"]=="":
        sl.warning("Please enter channel name or Channel ID")
    else:
        input_find(rr)
        if len(channel_data1["c_name"])!=0:
            sl.session_state["vd"]=youtube.video_data1
            sl.session_state["cd"]=youtube.channel_data1
            sl.session_state["cm"]=youtube.comment_data1
            sl.write(sl.session_state["cd"]["id"][0])
            name_of_the_channel=sl.session_state["cd"]["c_name"][0]
            sl.session_state["name_of_the_channel"]=(f'<h1 style="color:#FB2604;"> {name_of_the_channel}</h1>').upper()
            subcriber=sl.session_state["cd"]["c_subscriber"][0]
            views=sl.session_state["cd"]["c_views"][0]
            sl.session_state["subcriber"]=f'<i class="fa-solid fa-users" style="color: #ea2c0b;"></i>{subcriber}'
            sl.session_state["views"]=f'<i class="fa-solid fa-eye" style="color: #ea2c0b;"></i>{views}'
            dp=sl.session_state["cd"]["c_dp"][0]
            sl.session_state["dp"]=dp
            df=pd.DataFrame(sl.session_state["vd"])
            #df.loc[df["view_count"].max()]
            df1=df.sort_values(by="view_count",ascending=False)
            cc,dd=sl.columns([1,1])
            sl.session_state["vd1"]=df1.iloc[0]["v_url"]
            sl.session_state["vd2"]=df1.iloc[1]["v_url"]
            sl.session_state["lk1"]=df1.iloc[0]["like_count"]
            sl.session_state["lk2"]=df1.iloc[1]["like_count"]
            sl.session_state["vc1"]=df1.iloc[0]["view_count"]
            sl.session_state["vc2"]=df1.iloc[1]["view_count"]
            video_count=len(sl.session_state["vd"])
            sl.write(video_count)
            sl.session_state["pub"]=f'<i class="fa-solid fa-bullhorn fa-shake" style="color: #f70808;"></i>{(sl.session_state["cd"]["c_publish"][0])}'
            
        else:
            sl.error("Invalid search")
if clear:
    reset()
if p_database:
    if not hasattr(youtube,'video_data1'):
        sl.warning("No data availble please search")
    else:
        id_exist(youtube.CHANNEL_ID)
       
                      
sl.write(sl.session_state["name_of_the_channel"],unsafe_allow_html=True)
sl.write(sl.session_state["subcriber"], unsafe_allow_html=True)
sl.write(sl.session_state["views"], unsafe_allow_html=True)
sl.write(sl.session_state["pub"],unsafe_allow_html=True)
if sl.session_state["dp"]!="" :
    with sl.sidebar:
        sl.image(sl.session_state["dp"])
if sl.session_state["vd1"]!="":
    
    sl.subheader("Most visted videos")
    cc,dd=sl.columns([1,1])
    with cc:
        sl.video(sl.session_state["vd1"])
        ivid1,ivid2=sl.columns([1,1])
        with ivid1:
            sl.write(f'<i class="fa-regular fa-thumbs-up"></i>{sl.session_state["lk1"]}',unsafe_allow_html=True)
        with ivid2:
            sl.write(f'<i class="fa-solid fa-eye" style="color: #ea2c0b;"></i>{sl.session_state["vc1"]}',unsafe_allow_html=True)
    with dd:
        sl.video(sl.session_state["vd2"])
        ivid1,ivid2=sl.columns([1,1])
        with ivid1:
            sl.write(f'<i class="fa-regular fa-thumbs-up"></i>{sl.session_state["lk2"]}',unsafe_allow_html=True)
        with ivid2:
            sl.write(f'<i class="fa-solid fa-eye" style="color: #ea2c0b;"></i>{sl.session_state["vc2"]}',unsafe_allow_html=True)
    chan1=sl.radio("Choose Data Frame",["Channel Data", "Video Data", "Comment Data"]) 
    if chan1=="Channel Data":
        sl.subheader("Channel Information")
        sl.dataframe(sl.session_state["cd"],width=1500,hide_index=True)
    if chan1=="Video Data":
        sl.subheader("Video Uploads")
        sl.dataframe(sl.session_state["vd"],width=1500,hide_index=True)
    if chan1=="Comment Data":
        sl.subheader("Overall Public Comment")
        sl.dataframe(sl.session_state["cm"],width=1500,hide_index=True)
