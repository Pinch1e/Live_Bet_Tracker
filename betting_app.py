import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit.components.v1 import html

# page config
st.set_page_config(
    page_title="Pinchi's Betting Data Analysis App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Analysis"])

# Home page
if page == "Home":
    st.title("Welcome to Pinchi's Betting Data Analysis App")
    st.image("https://images.pexels.com/photos/590016/pexels-photo-590016.jpeg", use_container_width=True)
    st.markdown("""
    ### About
    This app provides a modern, techy interface to analyze your betting data.
    Use the sidebar to navigate to the Data Analysis page to view interactive charts.
    """)

# Data Analysis page
if page == "Data Analysis":
    st.title("Data Analysis")

    excel_file = 'betting_summary.xlsx'

    @st.cache_data
    def load_data():
        df = pd.read_excel(excel_file)
        df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
        # Calculate % Profit dynamically
        df['% Profit'] = ((df['Amount Left'] - df['Amount Invested']) / df['Amount Invested']) * 100
        return df

    df = load_data()

    st.write("Data Preview:")
    st.dataframe(df)


    # Pie chart: Event Distribution
    event_counts = df['Event'].value_counts()
    pie_fig = go.Figure(data=[go.Pie(labels=event_counts.index, values=event_counts.values, hole=0.3)])
    pie_fig.update_layout(title_text='Event Distribution', margin=dict(l=20, r=20, t=40, b=20), height=300)

    # Bar chart: Total Amount Invested by Event
    invested_by_event = df.groupby('Event')['Amount Invested'].sum()
    bar_fig = go.Figure(data=[go.Bar(x=invested_by_event.index, y=invested_by_event.values)])
    bar_fig.update_layout(title_text='Total Amount Invested by Event', margin=dict(l=20, r=20, t=40, b=20), height=300)

    # Line chart: Cumulative Profit Over Time
    df_sorted = df.sort_values('Date')
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(x=df_sorted['Date'], y=df_sorted['Cumulative Profit'], mode='lines+markers', name='Cumulative Profit'))
    line_fig.update_layout(title_text='Cumulative Profit Over Time', margin=dict(l=20, r=20, t=40, b=20), height=300)

    # Line chart: Losses Over Time
    losses_fig = go.Figure()
    losses_fig.add_trace(go.Scatter(x=df_sorted['Date'], y=df_sorted['Losses'], mode='lines+markers', name='Losses', line=dict(color='red')))
    losses_fig.update_layout(title_text='Losses Over Time', margin=dict(l=20, r=20, t=40, b=20), height=300)

    # Additional Line chart for % Profit Over Time
    profit_fig = go.Figure()
    profit_fig.add_trace(go.Scatter(x=df_sorted['Date'], y=df_sorted['% Profit'], mode='lines+markers', name='% Profit', line=dict(color='green')))
    profit_fig.update_layout(title_text='% Profit Over Time', margin=dict(l=20, r=20, t=40, b=20), height=300)

    # Custom CSS for horizontal scrolling swiper
    st.markdown("""
    <style>
    .swiper-container {
      display: flex;
      overflow-x: auto;
      scroll-snap-type: x mandatory;
      -webkit-overflow-scrolling: touch;
      gap: 10px;
      padding: 10px 0;
    }
    .swiper-slide {
      flex: 0 0 320px;
      scroll-snap-align: start;
      border: 1px solid #ddd;
      border-radius: 8px;
      padding: 10px;
      background: #fff;
      box-sizing: border-box;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display charts in swiper container
    st.markdown('<div class="swiper-container">', unsafe_allow_html=True)

    charts = [pie_fig, bar_fig, line_fig, losses_fig, profit_fig]
    for fig in charts:
        st.markdown('<div class="swiper-slide">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.experimental_rerun()
