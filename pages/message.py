import streamlit as st
from db import log_message
from db import query_message
from datetime import datetime, timezone
import pandas as pd
from db import DatabaseController
import os 
from nav import navigation
import html as html_utils
from streamlit.components.v1 import html
from db import check_permission

#Page Config
st.set_page_config(
    layout = "wide",
    page_title="Announcement Board",
    page_icon = "./assets/favi.ico",
)

def time_ago(dt):
    """Convert datetime to relative time like '17 minutes ago'."""
    now = datetime.now(dt.tzinfo)
    delta = now - dt

    seconds = delta.total_seconds()
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 2592000:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 31104000:
        months = int(seconds // 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds // 31104000)
        return f"{years} year{'s' if years != 1 else ''} ago"

def display_chat():
    rows = query_message()
    message_df = pd.DataFrame(rows, columns=["First Name", "Last Name", "Message", "Timestamp"])

    # --- Sort messages newest first ---
    message_df = message_df.sort_values(by="Timestamp", ascending=False)

    # --- Display tally under pinned header ---
    total_announcements = len(message_df)
    st.markdown(f"""
    <div style="
        text-align:center;
        color:#7db3ff;
        font-size:1.1rem;
        margin:8px 0 20px 0;
        font-family: 'Inter', sans-serif;
    ">
        Total Announcements: <strong>{total_announcements}</strong>
    </div>
    """, unsafe_allow_html=True)

    # --- Build all messages HTML at once ---
    messages_html = """
    <div id="chat-container" style="max-height:600px; overflow-y:auto; overflow-x:hidden; padding:10px;">
    """

    for idx, row in message_df.iterrows():
        first_initial = row['First Name'][0].upper() if row['First Name'] else '?'
        last_initial = row['Last Name'][0].upper() if row['Last Name'] else '?'
        initials = f"{first_initial}{last_initial}"

        dt = datetime.strptime(str(row["Timestamp"]), "%Y-%m-%d %H:%M:%S.%f")
        dt = dt.replace(tzinfo=timezone.utc).astimezone()
        nice_time = time_ago(dt)  # relative time

        latest_class = "latest" if idx == message_df.index[0] else ""
        badge_class = "message-badge latest" if idx == message_df.index[0] else "message-badge"
        badge_text = "Latest" if idx == message_df.index[0] else "Announcement"

        messages_html += f"""
        <div class="message-card {latest_class}" style="font-family:'Inter',sans-serif;">
            <div class="message-header">
                <div class="message-author">
                    <span class="author-icon">{initials}</span>
                    <span>{row['First Name']} {row['Last Name']}</span>
                </div>
                <div class="{badge_class}">{badge_text}</div>
            </div>
            <div class="message-body">{row['Message']}</div>
            <div class="message-footer">
                <div class="message-time">
                    <span class="time-icon">🕒</span>
                    <span>{nice_time}</span>
                </div>
            </div>
        </div>
        <div class="divider"></div>
        """

    messages_html += "</div>"

    # --- Full CSS + JS ---
    full_html = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }

        #chat-container {
            padding: 10px; 
            overflow-y: auto; 
            overflow-x: hidden; 
            max-height: 600px;
        }

        .message-card {
            position: relative;
            background: linear-gradient(145deg, #1a1a1a, #252525);
            border: 1px solid rgba(93, 160, 255, 0.2);
            border-left: 5px solid #5da0ff;
            padding: 24px 28px;
            margin: 20px 0;
            border-radius: 16px;
            box-shadow: 
                0 4px 16px rgba(0, 0, 0, 0.3),
                0 1px 3px rgba(93, 160, 255, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.03);
            transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
            animation: fadeInUp 0.5s ease-out;
            backdrop-filter: blur(10px);
            overflow: visible;
            font-family: 'Inter', sans-serif;
        }

        .message-card.latest { border-left:5px solid #ff7b50; }

        .message-card::before {
            content:''; position:absolute; top:0; left:-100%;
            width:100%; height:100%;
            background: linear-gradient(90deg, transparent, rgba(93,160,255,0.08), transparent);
            transition:left 0.5s ease;
        }

        .message-card:hover::before { left:100%; }

        .message-card:hover {
            transform: translateY(-2px) scale(1.01);
            box-shadow: 0 12px 28px rgba(0,0,0,0.5),
                        0 4px 12px rgba(93,160,255,0.2),
                        inset 0 1px 0 rgba(255,255,255,0.05);
            border-color: rgba(93,160,255,0.4);
        }

        .message-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; padding-bottom:12px; border-bottom:1px solid rgba(255,255,255,0.06); }
        .message-author { display:flex; align-items:center; gap:10px; font-weight:700; font-size:1.15rem; color:#f0f0f0; letter-spacing:0.4px; text-shadow:0 2px 4px rgba(0,0,0,0.3); }
        .author-icon { display:inline-flex; align-items:center; justify-content:center; width:36px; height:36px; background:linear-gradient(135deg, #5da0ff, #4a8cdb); border-radius:50%; font-size:1rem; box-shadow:0 3px 8px rgba(93,160,255,0.3); }
        .message-body { font-size:1.05rem; color:#e0e0e0; line-height:1.7; white-space:pre-wrap; padding:12px 16px; margin:12px 0; background:rgba(0,0,0,0.2); border-radius:10px; border-left:3px solid rgba(93,160,255,0.3); position:relative; }
        .message-footer { display:flex; align-items:center; justify-content:space-between; margin-top:14px; padding-top:10px; }
        .message-time { display:flex; align-items:center; gap:6px; font-size:0.85rem; color:#999; font-style:italic; letter-spacing:0.3px; }
        .time-icon { opacity:0.7; }
        .message-badge { display:inline-flex; align-items:center; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; background:rgba(93,160,255,0.15); border:1px solid rgba(93,160,255,0.3); color:#7db3ff; }
        .message-badge.latest { background:rgba(255,123,80,0.2); border-color:#ff7b50; color:#ff7b50; }
        .divider { height:2px; background:linear-gradient(to right, transparent, rgba(93,160,255,0.3) 20%, rgba(93,160,255,0.5) 50%, rgba(93,160,255,0.3) 80%, transparent); margin:25px 0 30px 0; position:relative; }
        .divider::after { content:'◆'; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); background:#1a1a1a; color:#5da0ff; padding:0 12px; font-size:0.7rem; opacity:0.6; }

        /* Hide scrollbars */
        #chat-container::-webkit-scrollbar { display: none; }
        #chat-container { -ms-overflow-style: none; scrollbar-width: none; }
    </style>

    <script>
        const chatContainer = document.getElementById('chat-container');
        if(chatContainer) { chatContainer.scrollTop = 0; }
    </script>
    """

    # --- Render everything ---
    html(messages_html + full_html, height=650)





#Checking Log In State
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")
    
#Navigation Bar
with st.sidebar:
    navigation()
    

#Page Header    
st.markdown("<h1 style='text-align: center;'>📢 Announcement Board</h1>", unsafe_allow_html=True)


#Chat Message Box
if check_permission(st.user["email"],'send_bulletin') ==  True:
    prompt = st.chat_input(
        "Say something"   
    ) 
    if prompt:
        prompt = html_utils.escape(prompt)
        log_message(html_utils.escape(prompt), datetime.now(timezone.utc),st.user.get("name").split(" ")[0], st.user.get("name").split(" ")[-1])
else:
    st.empty()
    st.warning("🔒 You do not have permission to post messages.")
    

display_chat()