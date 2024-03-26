from Home import *
from Mysql import *
from youtube import*
sl.set_page_config(layout="wide")
#sl.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">”>',unsafe_allow_html=True)
#sl.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script',unsafe_allow_html=True)
#sl.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>',unsafe_allow_html=True)
if "disabled" not in sl.session_state:
    sl.session_state.disabled = True
if "db" not in sl.session_state:
    sl.session_state.db=""
if "channel" not in sl.session_state:
    sl.session_state.channel=""
sl.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">',unsafe_allow_html=True)    
db=pd.read_sql_query("""SELECT * FROM channel_data""",engine.connect())
dbv=pd.read_sql_query(f'SELECT * FROM video_data',con=engine.connect())
dbc=pd.read_sql_query(f'SELECT * FROM comment_data',con=engine.connect())
dbc=pd.DataFrame(db)
c_id=""

channel=sl.selectbox("Choose Channel name:",dbc.c_name,placeholder="Select a channel",index=None)
if channel is not None:
    cha=dbc[dbc["c_name"]==channel].iloc[0]
    c_id=(dbc[dbc["c_name"]==channel].iloc[0])["id"]
video_db=pd.DataFrame(dbv)
#sl.write(id)
if channel:
    sl.session_state.channel=channel
if channel is None:
    sl.session_state["disabled"]=True
else:
    sl.session_state["disabled"]=False
    sl.write(f'<h1 style="color:#FB2604;"> {(dbc.loc[dbc["id"]==c_id,"c_name"].iloc[0]).upper()}</h1>',unsafe_allow_html=True)
    sl.write(dbc.loc[dbc["id"]==c_id,"c_description"].iloc[0])
    row=dbc[dbc["id"]==c_id].iloc[0]
    with sl.sidebar:
        sl.image(cha["c_dp"])
    one,two,three,four,five=sl.columns([1,1,1,1,1])
    with one:
        sl.write(f'<i class="fa-solid fa-users" style="color: #ea2c0b;"></i>{int(cha["c_subscriber"])}',unsafe_allow_html=True)
    with two:
        sl.write(f'<i class="fa-solid fa-eye" style="color: #ea2c0b;"></i>{int(cha["c_views"])}',unsafe_allow_html=True)
        sl.write(f'<p><i class="fa-solid fa-bullhorn fa-shake" style="color: #f70808;"></i>{(cha["c_publish"])}</p>',unsafe_allow_html=True)
    sl.subheader("Most visited Videos")
    vi=pd.DataFrame((video_db[video_db["c_id"]==c_id]).sort_values(by="view_count", ascending=False))
    vid1,vid2=sl.columns([1,1])
    with vid1:
        url=(((vi["v_url"]).values)[0])
        sl.video(url)
        sl.write(((vi["v_name"]).values)[0])
        ivid1,ivid2=sl.columns([1,1])
        with ivid1:
            sl.write(f'<i class="fa-regular fa-thumbs-up"></i>{((vi["like_count"]).values)[0]}',unsafe_allow_html=True)
        with ivid2:
            sl.write(f'<i class="fa-solid fa-eye" style="color: #ea2c0b;"></i>{((vi["view_count"]).values)[0]}',unsafe_allow_html=True)
    with vid2:
        url=(((vi["v_url"]).values)[1])
        sl.video(url)
        sl.write(((vi["v_name"]).values)[1])
        ivid1,ivid2=sl.columns([1,1])
        with ivid1:
            sl.write(f'<i class="fa-regular fa-thumbs-up"></i>{((vi["like_count"]).values)[1]}',unsafe_allow_html=True)
        with ivid2:
            sl.write(f'<i class="fa-solid fa-eye" style="color: #ea2c0b;"></i>{((vi["view_count"]).values)[1]}',unsafe_allow_html=True)
    chan1=sl.radio("Choose Data Frame",["Channel Data", "Video Data", "Comment Data"]) 
    if chan1=="Channel Data":
        sl.dataframe(db,width=1500,hide_index=True)
    if chan1=="Video Data":
        sl.dataframe(dbv,width=1500,hide_index=True)
    if chan1=="Comment Data":
        sl.dataframe(dbc,width=1500,hide_index=True)