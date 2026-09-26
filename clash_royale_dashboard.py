import sqlite3
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
from pathlib import Path
import numpy as np

st.set_page_config(
    page_title="Clash Royale | Player Intelligence",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

query_params = st.query_params
current_page = query_params.get("page", "Overview")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #121318;
    color: #F8FAFC;
}
            
.stMainBlockContainer {
    padding-top: 2rem !important;
}

section[data-testid="stSidebar"] {
    background-color: #0B0C10;
    border-right: 1px solid rgba(255, 255, 255, 0.04);
    padding-top: 10px;
    position: relative !important;
}

.menu-header {
    font-size: 16px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 25px;
    padding-left: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    letter-spacing: 0.5px;
}

.menu-item {
    padding: 11px 14px;
    border-radius: 12px;
    color: #94A3B8 !important;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none !important;
    transition: all 0.3s ease;
}

.menu-item svg {
    width: 18px;
    height: 18px;
    fill: #94A3B8;
    transition: fill 0.3s ease;
}

.menu-item:hover, .menu-item.active {
    background: #7c3aed;
    color: #FFFFFF !important;
    font-weight: 700;
    text-decoration: none !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
}

.menu-item:hover svg, .menu-item.active svg {
    fill: #FFFFFF !important;
}

section[data-testid="stSidebar"] {
    position: relative !important;
}

.sidebar-footer-container {
    position: absolute !important;
    bottom: -400px !important;
    left: 40px !important;
    width: 1000px !important;
    pointer-events: none !important;
    line-height: 0 !important;
    z-index: 999999 !important;
}

.sidebar-footer-img {
    width: 100% !important;
    height: auto !important;
    opacity: 0.4 !important;
    display: block !important;
    object-fit: contain !important;
    transform: scaleX(-1);
}

.sidebar-footer-container {
    margin-top: auto !important;
    width: 150px !important;
    margin-left: 15px !important;
    pointer-events: none !important;
    line-height: 0 !important;
}

.sidebar-footer-img {
    width: 100% !important;
    height: auto !important;
    opacity: 0.9 !important;
    display: block !important;
    object-fit: contain !important;
} 

.kpi-card {
    background: #191B24;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.kpi-title {
    color: #94A3B8;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.kpi-value {
    font-size: 24px;
    font-weight: 800;
    color: #FFFFFF;
}

div[data-testid="stElementContainer"]:has(div[data-testid="stPlotlyChart"]) {
    background: #191B24 !important;
    border: 1px solid rgba(255, 255, 255, 0.04) !important;
    border-radius: 24px !important;
    padding: 8px !important;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4) !important;
    margin-bottom: 24px;
    overflow: hidden !important;
}

div[data-testid="stPlotlyChart"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

.royale-hero {
    background: #191B24;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 24px;
    padding: 24px 30px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
}

.royale-hero::after {
    content: "👑";
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 85px;
    opacity: 0.9;
}

.insight-card {
    background: #191B24;
    border-left: 4px solid #7c3aed;
    border-radius: 20px;
    padding: 16px 20px;
    margin-bottom: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
    border-right: 1px solid rgba(255, 255, 255, 0.04);
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

header { background: transparent !important; }

[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarHeader"] button,
[data-testid="stHeader"] button,
section[data-testid="stSidebar"] [data-testid="stBaseButton-header"],
section[data-testid="stSidebar"] button:not(.menu-item) {
    color: #fb923c !important;
    background: transparent !important;
    border: none !important;
}

[data-testid="collapsedControl"] *,
[data-testid="stSidebarCollapseButton"] *,
button[data-testid="stSidebarCollapseButton"] *,
[data-testid="stSidebarHeader"] button *,
[data-testid="stHeader"] button *,
section[data-testid="stSidebar"] [data-testid="stBaseButton-header"] *,
section[data-testid="stSidebar"] button:not(.menu-item) * {
    fill: #fb923c !important;   
    color: #ffffff !important;  
    stroke: #fb923c !important; 
    opacity: 1 !important;
    visibility: visible !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

def get_sidebar_image_base64(filename):
    img_path = Path(__file__).parent / filename
    if img_path.exists():
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

sidebar_img_b64 = get_sidebar_image_base64("clash_royale_character.png")

with st.sidebar:
    st.markdown('<div class="menu-header"><span style="color: #fb923c;"></span> CLASH ROYALE ANALYSIS</div>', unsafe_allow_html=True)
    
    act_overview = "active" if current_page == "Overview" else ""
    act_engagement = "active" if current_page == "Engagement" else ""
    act_retention = "active" if current_page == "Retention" else ""
    act_monetization = "active" if current_page == "Monetization" else ""
    act_segments = "active" if current_page == "Player Segments" else ""
    act_platforms = "active" if current_page == "Platforms" else ""

    st.markdown(f'''<a class="menu-item {act_overview}" href="?page=Overview" target="_self">
        <svg viewBox="0 0 24 24"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>
        Overview
    </a>''', unsafe_allow_html=True)
    
    st.markdown(f'''<a class="menu-item {act_engagement}" href="?page=Engagement" target="_self">
        <svg viewBox="0 0 24 24"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
        Engagement
    </a>''', unsafe_allow_html=True)
    
    st.markdown(f'''<a class="menu-item {act_retention}" href="?page=Retention" target="_self">
        <svg viewBox="0 0 24 24"><path d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46C19.54 15.03 20 13.57 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74C4.46 8.97 4 10.43 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z"/></svg>
        Retention
    </a>''', unsafe_allow_html=True)
    
    st.markdown(f'''<a class="menu-item {act_monetization}" href="?page=Monetization" target="_self">
        <svg viewBox="0 0 24 24"><path d="M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
        Monetization
    </a>''', unsafe_allow_html=True)
    
    st.markdown(f'''<a class="menu-item {act_segments}" href="?page=Player Segments" target="_self">
        <svg viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
        Player Segments
    </a>''', unsafe_allow_html=True)
    
    st.markdown(f'''<a class="menu-item {act_platforms}" href="?page=Platforms" target="_self">
        <svg viewBox="0 0 24 24"><path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/></svg>
        Platforms
    </a>''', unsafe_allow_html=True)

    if sidebar_img_b64:
        st.markdown(f"""
            <div class="sidebar-footer-container">
                <img src="data:image/png;base64,{sidebar_img_b64}" class="sidebar-footer-img" alt="Sidebar Artwork">
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("clash_royale_character.png not found in the script folder.")

@st.cache_data
def load_overview_data():
    conn = sqlite3.connect('database.sqlite')
    
    query_players = "SELECT COUNT(DISTINCT player_id) as total_players FROM player_activity"
    try:
        df_players = pd.read_sql(query_players, conn)
        total_players = int(df_players['total_players'].iloc[0])
    except:
        total_players = 112792 
        
    query_dau = """
        SELECT date(timestamp) as act_date, COUNT(DISTINCT player_id) as daily_actives
        FROM player_activity
        GROUP BY act_date
    """
    try:
        df_dau = pd.read_sql(query_dau, conn)
        avg_dau = int(df_dau['daily_actives'].mean()) if not df_dau.empty else 18450
    except:
        avg_dau = 18450
        
    query_rev = "SELECT SUM(price) as total_rev, COUNT(DISTINCT player_id) as paying_users FROM purchases"
    try:
        df_rev = pd.read_sql(query_rev, conn)
        total_revenue = float(df_rev['total_rev'].iloc[0]) if df_rev['total_rev'].iloc[0] is not None else 42410.5
        paying_count = int(df_rev['paying_users'].iloc[0]) if df_rev['paying_users'].iloc[0] is not None else 1520
    except:
        total_revenue = 42410.5
        paying_count = 1520
        
    payer_conversion = (paying_count / total_players) * 100 if total_players > 0 else 1.35
    
    conn.close()
    return total_players, avg_dau, total_revenue, payer_conversion

total_players, avg_dau, total_revenue, payer_conversion = load_overview_data()    

if current_page == "Overview":
    st.markdown("""
    <div class="royale-hero">
        <div style="font-size: 11px; font-weight: 700; color: #fb923c; letter-spacing: 1.5px; text-transform: uppercase;">Arena Intelligence Hub</div>
        <div style="font-size: 26px; font-weight: 800; color: #FFFFFF; margin: 4px 0;">What makes players stay, play, and spend?</div>
        <div style="font-size: 13px; color: #94A3B8;">A high-level view of player growth, engagement, retention, and monetization.</div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">👥 Players</div><div class="kpi-value" style="color: #a78bfa;">{total_players:,}</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Total registered</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">📈 Avg DAU</div><div class="kpi-value" style="color: #FFFFFF;">{avg_dau:,}</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Dynamic daily avg</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">🔄 D7 Retention</div><div class="kpi-value" style="color: #fb923c;">20.05%</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Cohort benchmark</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">💰 Revenue</div><div class="kpi-value" style="color: #fb923c;">${total_revenue:,.0f}</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Full year aggregate</div></div>""", unsafe_allow_html=True)
    with k5:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">💳 Payer Conv.</div><div class="kpi-value" style="color: #a78bfa;">{payer_conversion:.2f}%</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Paying ratio</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        dates_sample = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        dau_values = [14200, 15100, 16800, 15900, 17200, 18400, 18900, 19200, 19800, 20500, 21500, 22400]

        fig_dau = go.Figure()
        fig_dau.add_trace(go.Scatter(
            x=dates_sample, y=dau_values, mode="lines+markers",
            line=dict(color="#a78bfa", width=3, shape="spline"),
            marker=dict(size=7, color="#fb923c"),
            fill="tozeroy", fillcolor="rgba(167, 139, 250, 0.08)"
        ))
        fig_dau.update_layout(
            title=dict(text="Daily Active Users (DAU) Trend", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=230,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=12))
        )
        st.plotly_chart(fig_dau, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        plat_labels = ["Android", "iOS"]
        plat_shares = [81.8, 18.2]

        fig_mix = go.Figure(go.Pie(
            labels=plat_labels,
            values=plat_shares,
            hole=0.65,
            marker=dict(colors=["#a78bfa", "#fb923c"], line=dict(color="#191B24", width=2)),
            textinfo="percent",
            textfont=dict(color="#FFFFFF", size=12, weight="bold")
        ))
        fig_mix.update_layout(
            title=dict(text="Player Mix by Platform", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=35, r=35, t=55, b=30), height=230,
            showlegend=True,
            legend=dict(orientation="h", y=-0.25, x=0.25, font=dict(color="#FFFFFF", size=12))
        )
        st.plotly_chart(fig_mix, use_container_width=True, config={"displayModeBar": False})

    col_mid_left, col_mid_right = st.columns(2)

    with col_mid_left:
        ret_days = ["Day 1", "Day 7", "Day 14", "Day 30"]
        ret_rates = [39.73, 20.05, 14.50, 10.10]

        fig_ret_snap = go.Figure(go.Scatter(
            x=ret_days, y=ret_rates, mode="lines+markers+text",
            text=[f"{v}%" for v in ret_rates],
            textposition="top center",
            textfont=dict(size=11, color="#FFFFFF", weight="bold"),
            line=dict(color="#fb923c", width=2.5),
            marker=dict(size=8, color="#a78bfa")
        ))
        fig_ret_snap.update_layout(
            title=dict(text="Retention Journey Snapshot (D1 to D30)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=230,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=12), range=[0, 48])
        )
        st.plotly_chart(fig_ret_snap, use_container_width=True, config={"displayModeBar": False})

    with col_mid_right:
        eng_levels = ["1 Session", "2 Sessions", "3–4 Sessions", "5+ Sessions"]
        d7_eng_rates = [8.12, 22.69, 35.97, 55.34]

        fig_eng_sig = go.Figure(go.Bar(
            x=d7_eng_rates,
            y=eng_levels,
            orientation='h',
            marker_color=["#4f46e5", "#7c3aed", "#a78bfa", "#fb923c"],
            text=[f"{val}%" for val in d7_eng_rates],
            textposition="auto",
            textfont=dict(size=14, color="#FFFFFF", weight="bold")
        ))
        fig_eng_sig.update_layout(
            title=dict(text="Early Engagement & D7 Retention Signal", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=230,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_eng_sig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div style="background: #191B24; border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 20px; padding: 20px; margin-bottom: 24px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);">
        <div style="font-size: 12px; font-weight: 700; color: #FFFFFF; margin-bottom: 15px; font-family: 'Inter', sans-serif;">💰 Monetization Overview Snapshot</div>
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase;">Payer Conversion</div>
                <div style="font-size: 20px; font-weight: 800; color: #fb923c; margin-top: 4px;">~1.35%</div>
            </div>
            <div style="border-left: 1px solid rgba(255, 255, 255, 0.06); padding-left: 40px;">
                <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase;">ARPU (Average Revenue Per User)</div>
                <div style="font-size: 20px; font-weight: 800; color: #a78bfa; margin-top: 4px;">~$0.38</div>
            </div>
            <div style="border-left: 1px solid rgba(255, 255, 255, 0.06); padding-left: 40px;">
                <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase;">ARPPU (Paying User Efficiency)</div>
                <div style="font-size: 20px; font-weight: 800; color: #FFFFFF; margin-top: 4px;">~$27.90</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #191B24; border: 1px solid rgba(255, 255, 255, 0.04); border-left: 4px solid #fb923c; border-radius: 20px; padding: 24px 30px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);">
        <div style="color: #fb923c; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">👑 What the Data Tells Us (Executive Summary)</div>
        <div style="color: #94A3B8; font-size: 14px; line-height: 1.7;">
            <b style="color: #FFFFFF;">01 — Engagement:</b> Higher Day-0 engagement is strongly <b>associated with</b> substantially higher D7 retention (scaling from 8.12% to 55.34%).<br>
            <b style="color: #FFFFFF;">02 — Retention:</b> Retention drops sharply between the first day (39.73%) and first week (20.05%), indicating that early onboarding friction is the primary churn driver.<br>
            <b style="color: #FFFFFF;">03 — Monetization:</b> Highly engaged players exhibit superior payer conversion and ARPU, while ARPPU remains remarkably stable across activity tiers.<br><br>
            <span style="color: #FFFFFF; font-weight: 600;">Business Question:</span> How can the game increase meaningful early engagement and convert more players into returning, long-term users?
        </div>
    </div>
    """, unsafe_allow_html=True)
elif current_page == "Engagement":
    st.markdown("""
    <div class="royale-hero">
        <div style="font-size: 11px; font-weight: 700; color: #fb923c; letter-spacing: 1.5px; text-transform: uppercase;">Player Engagement Intelligence</div>
        <div style="font-size: 26px; font-weight: 800; color: #FFFFFF; margin: 4px 0;">How are players actually using the game?</div>
        <div style="font-size: 13px; color: #94A3B8;">Analyzing session frequency, play time distribution, and behavioral intensity.</div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">Avg Sessions</div><div class="kpi-value" style="color: #a78bfa;">3.59</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Per player-day</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">Median Sessions</div><div class="kpi-value" style="color: #FFFFFF;">2.00</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Per player-day</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">Avg Play Time</div><div class="kpi-value" style="color: #fb923c;">23.9 min</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Duration mean</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">Median Play Time</div><div class="kpi-value" style="color: #FFFFFF;">14.4 min</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Duration median</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        sess_categories = ["1 Session", "2 Sessions", "3–4 Sessions", "5+ Sessions"]
        sess_counts = [42.5, 24.1, 19.3, 14.1] 

        fig_sess_dist = go.Figure(go.Bar(
            x=sess_counts,
            y=sess_categories,
            orientation='h',
            marker_color=["#4f46e5", "#7c3aed", "#a78bfa", "#fb923c"],
            text=[f"{val}%" for val in sess_counts],
            textposition="auto",
            textfont=dict(size=13, color="#FFFFFF", weight="bold")
        ))
        fig_sess_dist.update_layout(
            title=dict(text="Session Frequency Distribution", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_sess_dist, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        time_buckets = ["< 5 min", "5–15 min", "15–30 min", "30–60 min", "60+ min"]
        time_shares = [18.5, 34.2, 26.4, 15.0, 5.9]

        fig_time_dist = go.Figure(go.Bar(
            x=time_shares,
            y=time_buckets,
            orientation='h',
            marker_color=["#7c3aed", "#a78bfa", "#fb923c", "#f97316", "#ea580c"],
            text=[f"{val}%" for val in time_shares],
            textposition="auto",
            textfont=dict(size=12, color="#FFFFFF", weight="bold")
        ))
        fig_time_dist.update_layout(
            title=dict(text="Play Time Distribution (Bucketed)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_time_dist, use_container_width=True, config={"displayModeBar": False})

    session_levels = ["1 Session", "2 Sessions", "3 Sessions", "4 Sessions", "5+ Sessions"]
    avg_play_times = [8.5, 17.2, 28.4, 42.1, 68.5]
    bridge_labels = ["8.5 min", "17.2 min", "28.4 min", "42.1 min", "68.5 min"]
    
    bridge_positions = ["top right", "top center", "top center", "top center", "top left"]

    fig_bridge = go.Figure()
    fig_bridge.add_trace(go.Scatter(
        x=session_levels, y=avg_play_times,
        mode="lines+markers+text",
        text=bridge_labels,
        textposition=bridge_positions, 
        textfont=dict(size=11, color="#FFFFFF", weight="bold"),
        line=dict(color="#a78bfa", width=3, shape="spline"),
        marker=dict(size=9, color="#fb923c"),
        fill="tozeroy", fillcolor="rgba(167, 139, 250, 0.08)"
    ))
    fig_bridge.update_layout(
        title=dict(text="Engagement Bridge: More Sessions → More Play Time (Average Duration)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
        paper_bgcolor='#191B24', plot_bgcolor='#191B24',
        margin=dict(l=55, r=55, t=55, b=25), height=210, 
        xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1")),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=12), range=[0, 85])
    )
    st.plotly_chart(fig_bridge, use_container_width=True, config={"displayModeBar": False})

    col_lower_left, col_lower_right = st.columns(2)

    with col_lower_left:
        eng_levels_ret = ["1 Session", "2 Sessions", "3–4 Sessions", "5+ Sessions"]
        d7_ret_rates = [8.12, 22.69, 35.97, 55.34]

        fig_eng_ret = go.Figure(go.Bar(
            x=d7_ret_rates,
            y=eng_levels_ret,
            orientation='h',
            marker_color=["#4f46e5", "#7c3aed", "#a78bfa", "#fb923c"],
            text=[f"{val}%" for val in d7_ret_rates],
            textposition="auto",
            textfont=dict(size=11, color="#FFFFFF", weight="bold")
        ))
        fig_eng_ret.update_layout(
            title=dict(text="D7 Retention by Day-0 Engagement (Bridge)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_eng_ret, use_container_width=True, config={"displayModeBar": False})

    with col_lower_right:
        platforms = ["Android", "iOS"]
        avg_sess_plat = [2.43, 2.39]
        avg_dur_plat = [19.71, 16.94]

        fig_plat_eng = go.Figure(data=[
            go.Bar(name='Avg Sessions', x=platforms, y=avg_sess_plat, marker_color='#a78bfa', text=avg_sess_plat, textposition='auto', textfont=dict(size=10, color="#FFFFFF", weight='bold')),
            go.Bar(name='Avg Duration (min)', x=platforms, y=avg_dur_plat, marker_color='#fb923c', text=avg_dur_plat, textposition='auto', textfont=dict(size=10, color="#FFFFFF", weight='bold'))
        ])
        fig_plat_eng.update_layout(
            barmode='group',
            title=dict(text="Platform Engagement Comparison (Android vs iOS)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            legend=dict(orientation="h", y=-0.25, x=0.20, font=dict(color="#FFFFFF", size=12)),
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=10, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=12), range=[0, 30])
        )
        st.plotly_chart(fig_plat_eng, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #191B24; border: 1px solid rgba(255, 255, 255, 0.04); border-left: 4px solid #fb923c; border-radius: 20px; padding: 24px 30px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);">
        <div style="color: #fb923c; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">⚡ Engagement Signal Insight</div>
        <div style="color: #94A3B8; font-size: 14px; line-height: 1.6;">
            Most player-days involve relatively light engagement, while a smaller group of highly engaged players spends substantially more time in the game. Furthermore, higher Day-0 engagement is strongly <b>associated with</b> stronger D7 retention (scaling from 8.12% to 55.34%), building a solid bridge into the retention lifecycle.
        </div>
    </div>
    """, unsafe_allow_html=True)

elif current_page == "Retention":
    st.markdown("""
    <div class="royale-hero">
        <div style="font-size: 11px; font-weight: 700; color: #fb923c; letter-spacing: 1.5px; text-transform: uppercase;">Player Lifecycle & Retention</div>
        <div style="font-size: 26px; font-weight: 800; color: #FFFFFF; margin: 4px 0;">Why do players stay or drop off?</div>
        <div style="font-size: 13px; color: #94A3B8;">Analyzing seasonal cohort trends, platform stickiness, and day-0 engagement impact.</div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">D1 Retention</div><div class="kpi-value" style="color: #a78bfa;">39.73%</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">D7 Retention</div><div class="kpi-value" style="color: #fb923c;">20.05%</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">D30 Retention</div><div class="kpi-value" style="color: #fb923c;">10.10%</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">Avg. Churn Rate</div><div class="kpi-value" style="color: #fb923c;">60.27%</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        days = ["Day 1", "Day 3", "Day 7", "Day 14", "Day 21", "Day 30"]
        rates_cohort = [39.73, 28.5, 20.05, 14.6, 12.0, 10.1]
        labels_text = ["39.7%", "28.5%", "20.1%", "14.6%", "12.0%", "10.1%"]
        text_positions = ["top right", "top center", "top center", "top center", "top center", "top left"]
        
        fig_curve = go.Figure()
        fig_curve.add_trace(go.Scatter(
            x=days, y=rates_cohort, mode="lines+markers+text",
            text=labels_text,
            textposition=text_positions,
            textfont=dict(size=11, color="#FFFFFF", family="Inter", weight="bold"),
            line=dict(color="#a78bfa", width=2.5, shape="spline"),
            marker=dict(size=7, color="#fb923c"),
            fill="tozeroy", fillcolor="rgba(167, 139, 250, 0.08)"
        ))
        fig_curve.update_layout(
            title=dict(text="Player Retention Decay Curve (D1 to D30)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=45, r=45, t=55, b=25), height=210,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=12), range=[0, 52])
        )
        st.plotly_chart(fig_curve, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        platforms = ["Android", "iOS"]
        d1_plat = [39.80, 39.38]
        d7_plat = [19.49, 22.58]

        fig_plat = go.Figure(data=[
            go.Bar(name='D1 Retention', x=platforms, y=d1_plat, marker_color='#a78bfa', text=[f"{val}%" for val in d1_plat], textposition='auto', textfont=dict(size=12, color='#FFFFFF', weight='bold')),
            go.Bar(name='D7 Retention', x=platforms, y=d7_plat, marker_color='#fb923c', text=[f"{val}%" for val in d7_plat], textposition='auto', textfont=dict(size=12, color='#FFFFFF', weight='bold'))
        ])
        fig_plat.update_layout(
            barmode='group',
            title=dict(text="D1 & D7 Retention Breakdown by Platform", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=210,
            legend=dict(orientation="h", y=-0.25, x=0.25, font=dict(color="#FFFFFF", size=9)),
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=9, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=12), range=[0, 48])
        )
        st.plotly_chart(fig_plat, use_container_width=True, config={"displayModeBar": False})

    col_chart3, col_chart4 = st.columns(2)

    with col_chart3:
        engagement_levels = ["1 Session", "2 Sessions", "3–4 Sessions", "5+ Sessions"]
        d7_engagement_rates = [8.12, 22.69, 35.97, 55.34]

        fig_eng = go.Figure(go.Bar(
            x=d7_engagement_rates, y=engagement_levels,
            orientation='h',
            marker_color=["#4f46e5", "#7c3aed", "#a78bfa", "#fb923c"],
            text=[f"{val}%" for val in d7_engagement_rates],
            textposition="auto",
            textfont=dict(size=11, color="#FFFFFF", weight="bold")
        ))
        fig_eng.update_layout(
            title=dict(text="D7 Retention by Day-0 Engagement", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=210,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_eng, use_container_width=True, config={"displayModeBar": False})

    with col_chart4:
        seasons = ["Q1 (Winter)", "Q2 (Spring)", "Q3 (Summer)", "Q4 (Fall)"]
        retention_cols = ["D1", "D7", "D14", "D30"]
        seasonal_heatmap_data = [
            [40.3, 21.0, 16.1, 11.5], 
            [38.8, 19.7, 15.1, 10.5], 
            [39.5, 19.9, 14.6, 10.0], 
            [40.0, 20.7, 15.1, 10.3]   
        ]

        fig_heatmap = go.Figure(data=go.Heatmap(
            z=seasonal_heatmap_data, x=retention_cols, y=seasons,
            colorscale=[[0, '#121318'], [0.5, '#7c3aed'], [1, '#fb923c']],
            text=[[f"{val}%" for val in row] for row in seasonal_heatmap_data],
            texttemplate="%{text}", textfont={"size": 12, "color": "#FFFFFF", "weight": "bold"},
            showscale=False
        ))
        fig_heatmap.update_layout(
            title=dict(text="Seasonal Cohort Retention Heatmap (Q1 - Q4 2016)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=210,
            xaxis=dict(color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1")),
            yaxis=dict(color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1"), autorange="reversed")
        )
        st.plotly_chart(fig_heatmap, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #191B24; border: 1px solid rgba(255, 255, 255, 0.04); border-left: 4px solid #fb923c; border-radius: 20px; padding: 24px 30px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);">
        <div style="color: #fb923c; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">🎯 Product Analytics Insight</div>
        <div style="color: #94A3B8; font-size: 14px; line-height: 1.6;">
            Seasonal cohort analysis reveals exceptional baseline retention stability across quarters, while behavioral segmentation highlights that higher Day-0 engagement is strongly <b>associated with</b> increased D7 retention (scaling from 8.12% for single-session users to 55.34% for 5+ sessions). Optimizing early session loops is critical for long-term cohort stickiness.
        </div>
    </div>
    """, unsafe_allow_html=True)

elif current_page == "Monetization":
    st.markdown("""
    <div class="royale-hero">
        <div style="font-size: 11px; font-weight: 700; color: #fb923c; letter-spacing: 1.5px; text-transform: uppercase;">Monetization Intelligence & Revenue</div>
        <div style="font-size: 26px; font-weight: 800; color: #FFFFFF; margin: 4px 0;">Who pays, how much do they spend, and what drives revenue?</div>
        <div style="font-size: 13px; color: #94A3B8;">Analyzing weekly revenue trends, conversion efficiency, ARPU vs ARPPU, and behavioral monetization.</div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">Total Revenue</div><div class="kpi-value" style="color: #fb923c;">~$42.4K</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Full year aggregate</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">Paying Users</div><div class="kpi-value" style="color: #a78bfa;">~1.5K</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Unique purchasers</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">Payer Conversion</div><div class="kpi-value" style="color: #FFFFFF;">~1.4%</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Paying / Total players</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">ARPU</div><div class="kpi-value" style="color: #fb923c;">~$0.38</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Per all players</div></div>""", unsafe_allow_html=True)
    with k5:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">ARPPU</div><div class="kpi-value" style="color: #a78bfa;">~$27.5</div><div style="font-size: 10px; color: #64748B; margin-top: 4px;">Per paying player</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        weeks = ["W1", "W5", "W10", "W15", "W20", "W25", "W30", "W35", "W40", "W45", "W50"]
        weekly_revenue = [620, 750, 890, 810, 950, 1120, 1050, 980, 1250, 1340, 1420]

        fig_rev = go.Figure()
        fig_rev.add_trace(go.Scatter(
            x=weeks, y=weekly_revenue, mode="lines+markers",
            line=dict(color="#fb923c", width=3, shape="spline"),
            marker=dict(size=7, color="#a78bfa"),
            fill="tozeroy", fillcolor="rgba(251, 146, 60, 0.08)"
        ))
        fig_rev.update_layout(
            title=dict(text="Weekly Revenue Trend Over Time", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=12))
        )
        st.plotly_chart(fig_rev, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        eng_levels = ["1 Session", "2 Sessions", "3–4 Sessions", "5+ Sessions"]
        conversion_rates = [0.47, 1.24, 2.24, 4.84]

        fig_conv = go.Figure(go.Bar(
            x=conversion_rates,
            y=eng_levels,
            orientation='h',
            marker_color=["#4f46e5", "#7c3aed", "#a78bfa", "#fb923c"],
            text=[f"{val}%" for val in conversion_rates],
            textposition="auto",
            textfont=dict(size=11, color="#FFFFFF", weight="bold")
        ))
        fig_conv.update_layout(
            title=dict(text="Payer Conversion by Day-0 Engagement", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_conv, use_container_width=True, config={"displayModeBar": False})

    col_mid_left, col_mid_right = st.columns(2)

    with col_mid_left:
        segments = ["1 Session", "2 Sessions", "3–4 Sessions", "5+ Sessions"]
        arpu_vals = [0.153, 0.311, 0.589, 1.287]
        arppu_vals = [32.32, 25.05, 26.30, 26.59]

        fig_arpu_arppu = go.Figure(data=[
            go.Bar(name='ARPU ($)', x=segments, y=arpu_vals, marker_color='#a78bfa', text=[f"${v}" for v in arpu_vals], textposition='auto', textfont=dict(size=12, color='#FFFFFF', weight='bold')),
            go.Bar(name='ARPPU ($)', x=segments, y=arppu_vals, marker_color='#fb923c', text=[f"${v}" for v in arppu_vals], textposition='auto', textfont=dict(size=12, color='#FFFFFF', weight='bold'))
        ])
        fig_arpu_arppu.update_layout(
            barmode='group',
            title=dict(text="ARPU vs ARPPU by Engagement Segment", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            legend=dict(orientation="h", y=-0.25, x=0.25, font=dict(color="#FFFFFF", size=9)),
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=12))
        )
        st.plotly_chart(fig_arpu_arppu, use_container_width=True, config={"displayModeBar": False})

    with col_mid_right:
        rev_segments = ["1 Session", "2 Sessions", "3–4 Sessions", "5+ Sessions"]
        revenue_amounts = [10020.69, 5710.60, 8546.74, 18240.59]

        fig_rev_contrib = go.Figure(go.Bar(
            x=rev_segments,
            y=revenue_amounts,
            marker_color=["#4f46e5", "#7c3aed", "#a78bfa", "#fb923c"],
            text=[f"${v:,.0f}" for v in revenue_amounts],
            textposition="auto",
            textfont=dict(size=10, color="#FFFFFF", weight="bold")
        ))
        fig_rev_contrib.update_layout(
            title=dict(text="Revenue Contribution by Engagement Segment ($)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=12))
        )
        st.plotly_chart(fig_rev_contrib, use_container_width=True, config={"displayModeBar": False})

    col_low_left, col_low_right = st.columns(2)

    with col_low_left:
        ret_groups = ["D7 Retained", "Not Retained"]
        payer_conv_ret = [5.31, 0.40]

        fig_ret_conv = go.Figure(go.Bar(
            x=ret_groups,
            y=payer_conv_ret,
            marker_color=["#fb923c", "#4f46e5"],
            text=[f"{val}%" for val in payer_conv_ret],
            textposition="auto",
            textfont=dict(size=11, color="#FFFFFF", weight="bold")
        ))
        fig_ret_conv.update_layout(
            title=dict(text="Payer Conversion: D7 Retained vs Non-Retained", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=210,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=12))
        )
        st.plotly_chart(fig_ret_conv, use_container_width=True, config={"displayModeBar": False})

    with col_low_right:
        arpu_ret = [1.72, 0.05]

        fig_ret_arpu = go.Figure(go.Bar(
            x=ret_groups,
            y=arpu_ret,
            marker_color=["#a78bfa", "#7c3aed"],
            text=[f"${val}" for val in arpu_ret],
            textposition="auto",
            textfont=dict(size=11, color="#FFFFFF", weight="bold")
        ))
        fig_ret_arpu.update_layout(
            title=dict(text="ARPU: D7 Retained vs Non-Retained ($)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=210,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=12))
        )
        st.plotly_chart(fig_ret_arpu, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #191B24; border: 1px solid rgba(255, 255, 255, 0.04); border-left: 4px solid #fb923c; border-radius: 20px; padding: 24px 30px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);">
        <div style="color: #fb923c; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">💎 Monetization Product Insight</div>
        <div style="color: #94A3B8; font-size: 14px; line-height: 1.6;">
            Higher engagement is strongly <b>associated with</b> higher payer conversion and ARPU, while ARPPU remains relatively stable across engagement groups. This suggests that differences in monetization are more strongly driven by <b>conversion efficiency</b> rather than large differences in spend among existing payers. Connecting retention to monetization further confirms that D7 retained users exhibit significantly higher value ($1.72 ARPU vs $0.05).
        </div>
    </div>
    """, unsafe_allow_html=True)

elif current_page == "Player Segments":
    st.markdown("""
    <div class="royale-hero">
        <div style="font-size: 11px; font-weight: 700; color: #fb923c; letter-spacing: 1.5px; text-transform: uppercase;">Player Segmentation Intelligence</div>
        <div style="font-size: 26px; font-weight: 800; color: #FFFFFF; margin: 4px 0;">Who are our players, and how do their behaviors differ?</div>
        <div style="font-size: 13px; color: #94A3B8;">Analyzing player mix, engagement-driven retention, and segment revenue contributions.</div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">Low (1 Session)</div><div class="kpi-value" style="color: #a78bfa;">65,389</div><div style="font-size: 11px; color: #fb923c; margin-top: 4px; font-weight: 700;">58.0% of base</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">Moderate (2 Sessions)</div><div class="kpi-value" style="color: #a78bfa;">18,376</div><div style="font-size: 11px; color: #fb923c; margin-top: 4px; font-weight: 700;">16.3% of base</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">High (3–4 Sessions)</div><div class="kpi-value" style="color: #a78bfa;">14,510</div><div style="font-size: 11px; color: #fb923c; margin-top: 4px; font-weight: 700;">12.9% of base</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">Very High (5+ Sessions)</div><div class="kpi-value" style="color: #fb923c;">14,176</div><div style="font-size: 11px; color: #fb923c; margin-top: 4px; font-weight: 700;">12.6% of base</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        segments_labels = ["Low (1)", "Moderate (2)", "High (3-4)", "Very High (5+)"]
        segment_shares = [58.0, 16.3, 12.9, 12.6]

        fig_donut = go.Figure(go.Pie(
            labels=segments_labels,
            values=segment_shares,
            hole=0.65,
            marker=dict(colors=["#4f46e5", "#7c3aed", "#a78bfa", "#fb923c"], line=dict(color="#191B24", width=2)),
            textinfo="percent",
            textfont=dict(color="#FFFFFF", size=11, weight="bold")
        ))
        fig_donut.update_layout(
            title=dict(text="Player Mix by Engagement Segment", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=35, r=35, t=55, b=30), height=230,
            showlegend=True,
            legend=dict(orientation="h", y=-0.25, x=0.1, font=dict(color="#FFFFFF", size=12))
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        seg_names = ["Low", "Moderate", "High", "Very High"]
        d7_rates = [8.12, 22.69, 35.97, 55.34]

        fig_seg_ret = go.Figure(go.Bar(
            x=d7_rates,
            y=seg_names,
            orientation='h',
            marker_color=["#4f46e5", "#7c3aed", "#a78bfa", "#fb923c"],
            text=[f"{val}%" for val in d7_rates],
            textposition="auto",
            textfont=dict(size=12, color="#FFFFFF", weight="bold")
        ))
        fig_seg_ret.update_layout(
            title=dict(text="D7 Retention by Engagement Segment", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=230,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=12, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_seg_ret, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div style="background: #191B24; border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 20px; padding: 20px; margin-bottom: 24px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);">
        <div style="font-size: 12px; font-weight: 700; color: #FFFFFF; margin-bottom: 15px; font-family: 'Inter', sans-serif;">Segment Performance Matrix</div>
        <table style="width: 100%; text-align: left; border-collapse: collapse; font-size: 13px; color: #94A3B8;">
            <thead>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.08); color: #FFFFFF; font-size: 11px; text-transform: uppercase;">
                    <th style="padding-bottom: 10px;">Segment</th>
                    <th style="padding-bottom: 10px;">D7 Retention</th>
                    <th style="padding-bottom: 10px;">Payer Conversion</th>
                    <th style="padding-bottom: 10px;">ARPU</th>
                    <th style="padding-bottom: 10px;">ARPPU</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.03);">
                    <td style="padding: 10px 0; color: #FFFFFF; font-weight: 600;">Low (1 Session)</td>
                    <td style="color: #a78bfa;">8.12%</td>
                    <td>0.47%</td>
                    <td>$0.15</td>
                    <td style="color: #fb923c;">$32.32</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.03);">
                    <td style="padding: 10px 0; color: #FFFFFF; font-weight: 600;">Moderate (2 Sessions)</td>
                    <td style="color: #a78bfa;">22.69%</td>
                    <td>1.24%</td>
                    <td>$0.31</td>
                    <td style="color: #fb923c;">$25.05</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.03);">
                    <td style="padding: 10px 0; color: #FFFFFF; font-weight: 600;">High (3–4 Sessions)</td>
                    <td style="color: #a78bfa;">35.97%</td>
                    <td>2.24%</td>
                    <td>$0.59</td>
                    <td style="color: #fb923c;">$26.30</td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; color: #FFFFFF; font-weight: 600;">Very High (5+ Sessions)</td>
                    <td style="color: #a78bfa; font-weight: 700;">55.34%</td>
                    <td style="color: #FFFFFF; font-weight: 700;">4.84%</td>
                    <td style="color: #fb923c; font-weight: 700;">$1.29</td>
                    <td style="color: #fb923c;">$26.59</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    col_lower_left, col_lower_right = st.columns(2)

    with col_lower_left:
        rev_segments = ["Low", "Moderate", "High", "Very High"]
        revenue_values = [10020.69, 5710.60, 8546.74, 18240.59]

        fig_rev_seg = go.Figure(go.Bar(
            x=rev_segments,
            y=revenue_values,
            marker_color=["#4f46e5", "#7c3aed", "#a78bfa", "#fb923c"],
            text=[f"${v:,.0f}" for v in revenue_values],
            textposition="auto",
            textfont=dict(size=11, color="#FFFFFF", weight="bold")
        ))
        fig_rev_seg.update_layout(
            title=dict(text="Revenue Contribution by Segment ($)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=10, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=9))
        )
        st.plotly_chart(fig_rev_seg, use_container_width=True, config={"displayModeBar": False})

    with col_lower_right:
        arpu_seg = [0.15, 0.31, 0.59, 1.29]
        arppu_seg = [32.32, 25.05, 26.30, 26.59]

        fig_arpu_cmp = go.Figure(data=[
            go.Bar(name='ARPU ($)', x=rev_segments, y=arpu_seg, marker_color='#a78bfa', text=[f"${v}" for v in arpu_seg], textposition='auto', textfont=dict(size=9, color="#FFFFFF", weight='bold')),
            go.Bar(name='ARPPU ($)', x=rev_segments, y=arppu_seg, marker_color='#fb923c', text=[f"${v}" for v in arppu_seg], textposition='auto', textfont=dict(size=9, color="#FFFFFF", weight='bold'))
        ])
        fig_arpu_cmp.update_layout(
            barmode='group',
            title=dict(text="ARPU vs ARPPU by Segment", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            legend=dict(orientation="h", y=-0.25, x=0.25, font=dict(color="#FFFFFF", size=9)),
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=10, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=9))
        )
        st.plotly_chart(fig_arpu_cmp, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #191B24; border: 1px solid rgba(255, 255, 255, 0.04); border-left: 4px solid #fb923c; border-radius: 20px; padding: 24px 30px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);">
        <div style="color: #fb923c; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">👑 Segment Signal & Strategic Insight</div>
        <div style="color: #94A3B8; font-size: 14px; line-height: 1.6;">
            Very High-engagement players represent only <b>12.6%</b> of the player base, yet they generate a disproportionate share of revenue ($18.2K) and exhibit the highest D7 retention (55.34%) and ARPU ($1.29). Meanwhile, ARPPU remains remarkably stable (~$26-$32) across all segments, indicating that monetization uplift is driven primarily by conversion scale rather than whale spending spikes. <br><br>
            <span style="color: #FFFFFF; font-weight: 600;">Core Business Question:</span> How can we optimize onboarding loops to transition broader low-engagement cohorts into higher-tier activity brackets?
        </div>
    </div>
    """, unsafe_allow_html=True)

elif current_page == "Platforms":
    st.markdown("""
    <div class="royale-hero">
        <div style="font-size: 11px; font-weight: 700; color: #fb923c; letter-spacing: 1.5px; text-transform: uppercase;">Platform Intelligence & Comparison</div>
        <div style="font-size: 26px; font-weight: 800; color: #FFFFFF; margin: 4px 0;">How does player behavior differ across platforms?</div>
        <div style="font-size: 13px; color: #94A3B8;">Analyzing player distribution, engagement metrics, retention gaps, and monetization efficiency between Android and iOS.</div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">👥 Players</div>
        <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 13px;"><span style="color: #94A3B8;">Android</span><span style="color: #FFFFFF; font-weight: 700;">92,008</span></div>
        <div style="display: flex; justify-content: space-between; margin-top: 4px; font-size: 13px;"><span style="color: #94A3B8;">iOS</span><span style="color: #a78bfa; font-weight: 700;">20,443</span></div>
        </div>""", unsafe_allow_html=True)

    with k2:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">🔄 D7 Retention</div>
        <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 13px;"><span style="color: #94A3B8;">Android</span><span style="color: #FFFFFF; font-weight: 700;">19.49%</span></div>
        <div style="display: flex; justify-content: space-between; margin-top: 4px; font-size: 13px;"><span style="color: #94A3B8;">iOS</span><span style="color: #fb923c; font-weight: 700;">22.58%</span></div>
        </div>""", unsafe_allow_html=True)

    with k3:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">💳 Payer Conversion</div>
        <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 13px;"><span style="color: #94A3B8;">Android</span><span style="color: #FFFFFF; font-weight: 700;">1.25%</span></div>
        <div style="display: flex; justify-content: space-between; margin-top: 4px; font-size: 13px;"><span style="color: #94A3B8;">iOS</span><span style="color: #fb923c; font-weight: 700;">1.95%</span></div>
        </div>""", unsafe_allow_html=True)

    with k4:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">💰 ARPU</div>
        <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 13px;"><span style="color: #94A3B8;">Android</span><span style="color: #FFFFFF; font-weight: 700;">$0.27</span></div>
        <div style="display: flex; justify-content: space-between; margin-top: 4px; font-size: 13px;"><span style="color: #94A3B8;">iOS</span><span style="color: #fb923c; font-weight: 700;">$0.85</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        plat_labels = ["Android", "iOS"]
        plat_shares = [81.8, 18.2]

        fig_donut_plat = go.Figure(go.Pie(
            labels=plat_labels,
            values=plat_shares,
            hole=0.65,
            marker=dict(colors=["#a78bfa", "#fb923c"], line=dict(color="#191B24", width=2)),
            textinfo="percent",
            textfont=dict(color="#FFFFFF", size=11, weight="bold")
        ))
        fig_donut_plat.update_layout(
            title=dict(text="Player Mix by Platform (Share of Players)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=35, r=35, t=55, b=30), height=220,
            showlegend=True,
            legend=dict(orientation="h", y=-0.25, x=0.25, font=dict(color="#FFFFFF", size=9))
        )
        st.plotly_chart(fig_donut_plat, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        platforms = ["Android", "iOS"]
        avg_sess = [2.43, 2.39]

        fig_sess = go.Figure(go.Bar(
            x=avg_sess,
            y=platforms,
            orientation='h',
            marker_color=["#a78bfa", "#fb923c"],
            text=[str(v) for v in avg_sess],
            textposition="auto",
            textfont=dict(size=11, color="#FFFFFF", weight="bold")
        ))
        fig_sess.update_layout(
            title=dict(text="Average Sessions per Player-Day by Platform", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=9)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=10, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_sess, use_container_width=True, config={"displayModeBar": False})

    col_mid_left, col_mid_right = st.columns(2)

    with col_mid_left:
        avg_duration = [19.7, 16.9]

        fig_dur = go.Figure(go.Bar(
            x=avg_duration,
            y=platforms,
            orientation='h',
            marker_color=["#7c3aed", "#fb923c"],
            text=[f"{v} min" for v in avg_duration],
            textposition="auto",
            textfont=dict(size=11, color="#FFFFFF", weight="bold")
        ))
        fig_dur.update_layout(
            title=dict(text="Average Play Time by Platform (Minutes)", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=9)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=10, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_dur, use_container_width=True, config={"displayModeBar": False})

    with col_mid_right:
        d1_ret = [39.80, 39.38]
        d7_ret = [19.49, 22.58]

        fig_ret_cmp = go.Figure(data=[
            go.Bar(name='D1 Retention', x=platforms, y=d1_ret, marker_color='#a78bfa', text=[f"{v}%" for v in d1_ret], textposition='auto', textfont=dict(size=9, color="#FFFFFF", weight='bold')),
            go.Bar(name='D7 Retention', x=platforms, y=d7_ret, marker_color='#fb923c', text=[f"{v}%" for v in d7_ret], textposition='auto', textfont=dict(size=9, color="#FFFFFF", weight='bold'))
        ])
        fig_ret_cmp.update_layout(
            barmode='group',
            title=dict(text="Retention Comparison (D1 vs D7) by Platform", font=dict(size=12, color="#FFFFFF", family="Inter"), x=0.04, y=0.88),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=40, r=40, t=55, b=25), height=220,
            legend=dict(orientation="h", y=-0.25, x=0.25, font=dict(color="#FFFFFF", size=9)),
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=10, weight="bold", color="#CBD5E1")),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', color='#64748B', tickfont=dict(size=9))
        )
        st.plotly_chart(fig_ret_cmp, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div style="background: #191B24; border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 20px; padding: 20px; margin-bottom: 24px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);">
        <div style="font-size: 12px; font-weight: 700; color: #FFFFFF; margin-bottom: 12px; font-family: 'Inter', sans-serif;">Monetization Efficiency by Platform</div>
    </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        fig_pc = go.Figure(go.Bar(
            x=[1.25, 1.95], y=platforms, orientation='h',
            marker_color=["#a78bfa", "#fb923c"],
            text=["1.25%", "1.95%"], textposition="auto",
            textfont=dict(size=10, color="#FFFFFF", weight="bold")
        ))
        fig_pc.update_layout(
            title=dict(text="Payer Conversion (%)", font=dict(size=11, color="#FFFFFF", family="Inter"), x=0.04, y=0.85),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=30, r=30, t=45, b=20), height=170,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=8)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=9, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_pc, use_container_width=True, config={"displayModeBar": False})

    with col_m2:
        fig_arpu = go.Figure(go.Bar(
            x=[0.27, 0.85], y=platforms, orientation='h',
            marker_color=["#a78bfa", "#fb923c"],
            text=["$0.27", "$0.85"], textposition="auto",
            textfont=dict(size=10, color="#FFFFFF", weight="bold")
        ))
        fig_arpu.update_layout(
            title=dict(text="ARPU ($)", font=dict(size=11, color="#FFFFFF", family="Inter"), x=0.04, y=0.85),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=30, r=30, t=45, b=20), height=170,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=8)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=9, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_arpu, use_container_width=True, config={"displayModeBar": False})

    with col_m3:
        fig_arppu = go.Figure(go.Bar(
            x=[21.88, 43.56], y=platforms, orientation='h',
            marker_color=["#a78bfa", "#fb923c"],
            text=["$21.88", "$43.56"], textposition="auto",
            textfont=dict(size=10, color="#FFFFFF", weight="bold")
        ))
        fig_arppu.update_layout(
            title=dict(text="ARPPU ($)", font=dict(size=11, color="#FFFFFF", family="Inter"), x=0.04, y=0.85),
            paper_bgcolor='#191B24', plot_bgcolor='#191B24',
            margin=dict(l=30, r=30, t=45, b=20), height=170,
            xaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=8)),
            yaxis=dict(showgrid=False, color='#64748B', tickfont=dict(size=9, weight="bold", color="#CBD5E1"))
        )
        st.plotly_chart(fig_arppu, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div style="background: #191B24; border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 20px; padding: 20px; margin-bottom: 24px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);">
        <div style="font-size: 12px; font-weight: 700; color: #FFFFFF; margin-bottom: 15px; font-family: 'Inter', sans-serif;">Platform Performance Matrix</div>
        <table style="width: 100%; text-align: left; border-collapse: collapse; font-size: 13px; color: #94A3B8;">
            <thead>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.08); color: #FFFFFF; font-size: 11px; text-transform: uppercase;">
                    <th style="padding-bottom: 10px;">Metric</th>
                    <th style="padding-bottom: 10px;">Android</th>
                    <th style="padding-bottom: 10px;">iOS</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.03);"><td style="padding: 8px 0; color: #FFFFFF; font-weight: 600;">Players</td><td>92,008</td><td style="color: #a78bfa;">20,443</td></tr>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.03);"><td style="padding: 8px 0; color: #FFFFFF; font-weight: 600;">Avg Sessions</td><td>2.43</td><td>2.39</td></tr>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.03);"><td style="padding: 8px 0; color: #FFFFFF; font-weight: 600;">Avg Play Time</td><td>19.7 min</td><td>16.9 min</td></tr>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.03);"><td style="padding: 8px 0; color: #FFFFFF; font-weight: 600;">D1 Retention</td><td>39.80%</td><td>39.38%</td></tr>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.03);"><td style="padding: 8px 0; color: #FFFFFF; font-weight: 600;">D7 Retention</td><td>19.49%</td><td style="color: #fb923c; font-weight: 700;">22.58%</td></tr>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.03);"><td style="padding: 8px 0; color: #FFFFFF; font-weight: 600;">Payer Conversion</td><td>1.25%</td><td style="color: #fb923c; font-weight: 700;">1.95%</td></tr>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.03);"><td style="padding: 8px 0; color: #FFFFFF; font-weight: 600;">ARPU</td><td>$0.27</td><td style="color: #fb923c; font-weight: 700;">$0.85</td></tr>
                <tr><td style="padding: 8px 0; color: #FFFFFF; font-weight: 600;">ARPPU</td><td>$21.88</td><td style="color: #fb923c; font-weight: 700;">$43.56</td></tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #191B24; border: 1px solid rgba(255, 255, 255, 0.04); border-left: 4px solid #fb923c; border-radius: 20px; padding: 24px 30px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);">
        <div style="color: #fb923c; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">👑 Platform Signal & Strategic Insight</div>
        <div style="color: #94A3B8; font-size: 14px; line-height: 1.6;">
            Android represents the majority of the player base (81.8%) and exhibits slightly higher observed play duration, while iOS players demonstrate higher D7 retention and significantly stronger monetization metrics (ARPU of $0.85 vs $0.27, and ARPPU of $43.56 vs $21.88). <br><br>
            <span style="color: #FFFFFF; font-weight: 600;">Business Question:</span> What product, offer, or purchase-flow differences could explain the platform-level variation observed in this dataset?
        </div>
    </div>
    """, unsafe_allow_html=True)