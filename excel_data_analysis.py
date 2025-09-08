import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# Path to the Excel file
excel_file = 'betting_summary.xlsx'

def read_data():
    # Read the Excel file
    df = pd.read_excel(excel_file)
    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
    return df

def plot_charts(df):
    # Clear all figures
    plt.close('all')

    # Pie chart: Distribution of Events
    fig1, ax1 = plt.subplots()
    event_counts = df['Event'].value_counts()
    ax1.pie(event_counts, labels=event_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Event Distribution')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Bar chart: Sum of Amount Invested by Event
    fig2, ax2 = plt.subplots()
    invested_by_event = df.groupby('Event')['Amount Invested'].sum()
    invested_by_event.plot(kind='bar', ax=ax2)
    ax2.set_title('Total Amount Invested by Event')
    ax2.set_ylabel('Amount Invested')
    ax2.set_xlabel('Event')

    # Line chart: Cumulative Profit over Date
    fig3, ax3 = plt.subplots()
    df_sorted = df.sort_values('Date')
    ax3.plot(df_sorted['Date'], df_sorted['Cumulative Profit'], marker='o')
    ax3.set_title('Cumulative Profit Over Time')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Cumulative Profit')
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)

    plt.tight_layout()

def update(frame):
    if os.path.exists(excel_file):
        df = read_data()
        if not df.empty:
            plot_charts(df)

if __name__ == '__main__':
    # Initial plot
    if os.path.exists(excel_file):
        df = read_data()
        if not df.empty:
            plot_charts(df)
    
    # Use FuncAnimation to update charts dynamically every 10 seconds
    ani = FuncAnimation(plt.gcf(), update, interval=10000, cache_frame_data=False)
    plt.show()
