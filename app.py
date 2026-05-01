import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Instagram Analytics", page_icon="📸", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { background-color: #0a0a1a; color: #fff; font-family: 'Inter', sans-serif; }
.stApp { background-color: #0a0a1a; }
.hero {
    background: linear-gradient(135deg, #E4405F 0%, #FD1D1D 50%, #1a0a4a 100%);
    padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem; text-align: center;
    box-shadow: 0 8px 32px rgba(228,64,95,0.3);
}
.hero h1 { font-family:'Bebas Neue',sans-serif; font-size:3.5rem; letter-spacing:4px; color:#fff; margin:0; }
.hero p { color:#ffb3c1; margin-top:0.5rem; }
.metric-card {
    background: linear-gradient(135deg,#1a1a2e,#16213e); border:1px solid #E4405F;
    border-radius:16px; padding:1.3rem; text-align:center; margin-bottom:1rem;
    box-shadow:0 4px 15px rgba(228,64,95,0.15);
}
.metric-number { font-family:'Bebas Neue',sans-serif; font-size:2.5rem; color:#E4405F; }
.metric-label { color:#aaa; font-size:0.8rem; text-transform:uppercase; letter-spacing:2px; }
.section-title {
    font-family:'Bebas Neue',sans-serif; font-size:1.8rem; color:#E4405F;
    letter-spacing:3px; border-left:4px solid #E4405F; padding-left:12px; margin:1.5rem 0 1rem 0;
}
[data-testid="stSidebar"] { background-color:#0d0d1a !important; border-right:1px solid #E4405F; }
.stTabs [data-baseweb="tab-list"] { background-color:#1a1a2e; border-radius:10px; }
.stTabs [aria-selected="true"] { color:#E4405F !important; border-bottom:2px solid #E4405F; }
.stButton > button {
    background:linear-gradient(135deg,#E4405F,#fd1d1d); color:white; border:none;
    border-radius:10px; font-weight:700; padding:0.6rem 2rem; transition:all 0.2s;
}
.stButton > button:hover { transform:scale(1.03); }
#MainMenu, footer, header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>📸 INSTAGRAM ANALYTICS</h1>
    <p>Growth • Engagement • Performance • Insights</p>
</div>
""", unsafe_allow_html=True)

def generate_instagram_data():
    dates = pd.date_range(start='2024-01-01', end='2025-01-01', freq='D')
    data = []
    followers = 1000
    for date in dates:
        followers += np.random.randint(-50, 150)
        engagement_rate = np.random.uniform(2, 8)
        likes = np.random.randint(100, 5000)
        comments = np.random.randint(10, 500)
        shares = np.random.randint(5, 200)
        
        data.append({
            'Date': date,
            'Followers': max(followers, 1000),
            'Engagement_Rate': engagement_rate,
            'Likes': likes,
            'Comments': comments,
            'Shares': shares,
            'Post_Type': np.random.choice(['Reel', 'Photo', 'Carousel', 'Story'])
        })
    return pd.DataFrame(data)

df = generate_instagram_data()

with st.sidebar:
    st.markdown("## 📊 Profile Analytics")
    st.markdown("---")
    username = st.text_input("👤 Instagram Handle", "your_username")
    time_period = st.selectbox("📅 Time Period", ["Last 30 Days", "Last 90 Days", "Last 6 Months", "All Time"])
    st.markdown("---")
    st.info("📈 Track your Instagram growth & engagement")

period_map = {
    "Last 30 Days": 30,
    "Last 90 Days": 90,
    "Last 6 Months": 180,
    "All Time": None
}
days = period_map[time_period]
filt = df.tail(days) if days else df

current_followers = filt['Followers'].iloc[-1]
prev_followers = filt['Followers'].iloc[0]
follower_growth = current_followers - prev_followers
growth_pct = (follower_growth / prev_followers * 100) if prev_followers > 0 else 0

avg_engagement = filt['Engagement_Rate'].mean()
total_likes = filt['Likes'].sum()
total_comments = filt['Comments'].sum()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-number">{current_followers:,}</div><div class="metric-label">Followers</div></div>', unsafe_allow_html=True)
with c2:
    color = "🟢" if follower_growth >= 0 else "🔴"
    st.markdown(f'<div class="metric-card"><div class="metric-number">{color} {follower_growth:,}</div><div class="metric-label">Growth</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-number">{avg_engagement:.2f}%</div><div class="metric-label">Engagement</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-number">{total_likes:,}</div><div class="metric-label">Total Likes</div></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Growth", "❤️ Engagement", "📊 Posts", "🎯 Best Posts", "🔍 Details"])

PINK = "#E4405F"

with tab1:
    st.markdown('<div class="section-title">FOLLOWER GROWTH</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filt['Date'], y=filt['Followers'],
                            mode='lines', name='Followers',
                            line=dict(color=PINK, width=3),
                            fill='tozeroy', fillcolor='rgba(228,64,95,0.1)'))
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                     font=dict(color="white"), hovermode='x unified',
                     xaxis=dict(gridcolor="#222"), yaxis=dict(gridcolor="#222"))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="section-title">GROWTH METRICS</div>', unsafe_allow_html=True)
    growth_df = pd.DataFrame({
        "Metric": ["Total Growth", "Growth %", "Daily Average", "Highest Day", "Lowest Day"],
        "Value": [
            f"{follower_growth:,}",
            f"{growth_pct:.2f}%",
            f"{follower_growth/len(filt):.0f}",
            f"+{filt['Followers'].diff().max():.0f}",
            f"{filt['Followers'].diff().min():.0f}"
        ]
    })
    st.dataframe(growth_df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown('<div class="section-title">ENGAGEMENT ANALYTICS</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Avg Engagement Rate", f"{avg_engagement:.2f}%")
    with c2:
        st.metric("Total Comments", f"{total_comments:,}")
    with c3:
        st.metric("Total Shares", f"{filt['Shares'].sum():,}")
    
    fig = px.bar(x=filt['Date'], y=['Likes', 'Comments', 'Shares'],
                 barmode='stack', color_discrete_sequence=['#E4405F', '#FD1D1D', '#FF6B9D'],
                 labels={"Date":"Date","value":"Count"})
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                     font=dict(color="white"), xaxis=dict(gridcolor="#222"), yaxis=dict(gridcolor="#222"))
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown('<div class="section-title">POST TYPE ANALYSIS</div>', unsafe_allow_html=True)
    
    post_type_counts = filt['Post_Type'].value_counts()
    fig = px.pie(values=post_type_counts.values, names=post_type_counts.index,
                 color_discrete_sequence=['#E4405F', '#FD1D1D', '#FF6B9D', '#FFB3C1'])
    fig.update_traces(textfont_color="white")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                     font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="section-title">POST PERFORMANCE BY TYPE</div>', unsafe_allow_html=True)
    post_perf = filt.groupby('Post_Type')[['Likes', 'Comments', 'Shares', 'Engagement_Rate']].mean().reset_index()
    post_perf = post_perf.round(2)
    st.dataframe(post_perf, use_container_width=True, hide_index=True)

with tab4:
    st.markdown('<div class="section-title">TOP PERFORMING POSTS</div>', unsafe_allow_html=True)
    filt['Total_Engagement'] = filt['Likes'] + filt['Comments'] + filt['Shares']
    top_posts = filt.nlargest(10, 'Total_Engagement')[['Date', 'Post_Type', 'Likes', 'Comments', 'Shares', 'Engagement_Rate']]
    top_posts['Date'] = top_posts['Date'].dt.date
    st.dataframe(top_posts.reset_index(drop=True), use_container_width=True, hide_index=True, height=300)

with tab5:
    st.markdown('<div class="section-title">DETAILED ANALYTICS</div>', unsafe_allow_html=True)
    display_df = filt[['Date', 'Followers', 'Likes', 'Comments', 'Shares', 'Engagement_Rate', 'Post_Type']].copy()
    display_df['Date'] = pd.to_datetime(display_df['Date']).dt.date
    display_df = display_df.sort_values('Date', ascending=False)
    st.dataframe(display_df.reset_index(drop=True), use_container_width=True, hide_index=True, height=450)
    
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Analytics CSV", csv, "instagram_analytics.csv", "text/csv")

st.markdown("---")
st.markdown('<p style="text-align:center;color:#444;font-size:0.8rem;">📸 Instagram Analytics Dashboard | Track Your Growth</p>', unsafe_allow_html=True)
