import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Instagram Analytics Pro", page_icon="📊", layout="wide")

# --- Premium CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    background-color: #0a0a0a;
    color: #fff;
    font-family: 'Inter', sans-serif;
}

.stApp { background-color: #0a0a0a; }

.hero {
    background: linear-gradient(135deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    padding: 2.5rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 10px 40px rgba(220, 39, 67, 0.3);
}

.hero h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    letter-spacing: 6px;
    color: #fff;
    margin: 0;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
}

.hero p {
    color: #ffdbac;
    margin-top: 0.5rem;
    font-size: 1.1rem;
}

.metric-card {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    padding: 1.5rem;
    border-radius: 15px;
    border: 1px solid #333;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero">
    <h1>INSTAGRAM ANALYTICS PRO</h1>
    <p>Track, Analyze & Grow Your Instagram Performance</p>
</div>
""", unsafe_allow_html=True)

# --- File Upload ---
uploaded_file = st.file_uploader("📁 Upload Instagram Data CSV", type=['csv'])

# --- Sample Data Generator ---
def generate_sample_data():
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    data = {
        'Date': dates,
        'Likes': np.random.randint(500, 5000, 30),
        'Comments': np.random.randint(50, 500, 30),
        'Shares': np.random.randint(20, 300, 30),
        'Saves': np.random.randint(30, 400, 30),
        'Reach': np.random.randint(2000, 20000, 30),
        'Impressions': np.random.randint(3000, 30000, 30),
        'Followers': np.cumsum(np.random.randint(10, 100, 30)) + 10000
    }
    return pd.DataFrame(data)

# --- Load Data ---
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("👆 Upload your CSV or use sample data below")
    if st.button("Load Sample Data"):
        df = generate_sample_data()
        st.session_state['df'] = df
    df = st.session_state.get('df', generate_sample_data())

# --- Data Cleaning & Fix for ValueError ---
try:
    # 1. Convert Date column
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # 2. Drop rows where Date or key metrics are NaN - THIS FIXES THE ERROR
    required_cols = ['Date', 'Likes', 'Comments', 'Reach']
    df = df.dropna(subset=[col for col in required_cols if col in df.columns])

    # 3. Sort and reset index
    df = df.sort_values('Date').reset_index(drop=True)

    # 4. Fill remaining NaN with 0
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

except Exception as e:
    st.error(f"Data processing error: {e}")
    st.stop()

# --- Metrics Row ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_likes = int(df['Likes'].sum())
    st.metric("Total Likes", f"{total_likes:,}", delta=f"{df['Likes'].iloc[-1] - df['Likes'].iloc[-2]:+,}")

with col2:
    total_comments = int(df['Comments'].sum())
    st.metric("Total Comments", f"{total_comments:,}", delta=f"{df['Comments'].iloc[-1] - df['Comments'].iloc[-2]:+,}")

with col3:
    avg_reach = int(df['Reach'].mean())
    st.metric("Avg Reach", f"{avg_reach:,}", delta=f"{((df['Reach'].iloc[-1] / df['Reach'].iloc[-2] - 1) * 100):+.1f}%")

with col4:
    engagement_rate = (df['Likes'].sum() + df['Comments'].sum()) / df['Reach'].sum() * 100
    st.metric("Engagement Rate", f"{engagement_rate:.2f}%")

st.markdown("---")

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📊 Engagement", "🎯 Growth", "📥 Data"])

with tab1:
    st.subheader("Performance Overview")

    # Line Chart - Reach & Impressions
    fig1 = px.line(df, x='Date', y=['Reach', 'Impressions'],
                   title='Reach vs Impressions Over Time',
                   template='plotly_dark',
                   color_discrete_sequence=['#f09433', '#e6683c'])
    fig1.update_layout(hovermode='x unified', paper_bgcolor='#0a0a0a', plot_bgcolor='#1a1a1a')
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        # Bar Chart - Likes by Date
        fig2 = px.bar(df.tail(14), x='Date', y='Likes',
                      title='Likes - Last 14 Days',
                      template='plotly_dark',
                      color_discrete_sequence=['#dc2743'])
        fig2.update_layout(paper_bgcolor='#0a0a0a', plot_bgcolor='#1a1a1a')
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        # Area Chart - Comments Trend
        fig3 = px.area(df.tail(14), x='Date', y='Comments',
                       title='Comments Trend - Last 14 Days',
                       template='plotly_dark',
                       color_discrete_sequence=['#cc2366'])
        fig3.update_layout(paper_bgcolor='#0a0a0a', plot_bgcolor='#1a1a1a')
        st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader("Engagement Breakdown")

    # Pie Chart
    engagement_data = {
        'Metric': ['Likes', 'Comments', 'Shares', 'Saves'],
        'Count': [df['Likes'].sum(), df['Comments'].sum(),
                  df.get('Shares', pd.Series([0])).sum(),
                  df.get('Saves', pd.Series([0])).sum()]
    }
    fig4 = px.pie(engagement_data, values='Count', names='Metric',
                  title='Engagement Distribution',
                  template='plotly_dark',
                  color_discrete_sequence=['#f09433', '#e6683c', '#dc2743', '#bc1888'])
    fig4.update_layout(paper_bgcolor='#0a0a0a')
    st.plotly_chart(fig4, use_container_width=True)

    # Scatter Plot
    fig5 = px.scatter(df, x='Reach', y='Likes', size='Comments',
                      title='Reach vs Likes Correlation',
                      template='plotly_dark',
                      color='Comments',
                      color_continuous_scale='OrRd')
    fig5.update_layout(paper_bgcolor='#0a0a0a', plot_bgcolor='#1a1a1a')
    st.plotly_chart(fig5, use_container_width=True)

with tab3:
    st.subheader("Follower Growth")

    if 'Followers' in df.columns:
        fig6 = px.line(df, x='Date', y='Followers',
                       title='Follower Growth Trend',
                       template='plotly_dark',
                       color_discrete_sequence=['#bc1888'])
        fig6.update_layout(paper_bgcolor='#0a0a0a', plot_bgcolor='#1a1a1a')
        st.plotly_chart(fig6, use_container_width=True)

        # Growth Rate
        df['Growth'] = df['Followers'].diff()
        fig7 = px.bar(df.tail(14), x='Date', y='Growth',
                      title='Daily Follower Growth - Last 14 Days',
                      template='plotly_dark',
                      color='Growth',
                      color_continuous_scale='RdYlGn')
        fig7.update_layout(paper_bgcolor='#0a0a0a', plot_bgcolor='#1a1a1a')
        st.plotly_chart(fig7, use_container_width=True)
    else:
        st.warning("Followers column not found in your data")

with tab4:
    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True, height=400)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Processed CSV",
        data=csv,
        file_name=f"instagram_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

    # Data Stats
    st.subheader("Data Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", len(df))
    col2.metric("Date Range", f"{df['Date'].min().date()} to {df['Date'].max().date()}")
    col3.metric("Columns", len(df.columns))

# --- Footer ---
st.markdown("---")
st.caption("Data source: Instagram CSV Export | Built with Streamlit & Plotly | Premium Dashboard v2.0")
