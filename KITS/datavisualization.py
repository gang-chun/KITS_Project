import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta, date

def get_month(datetime):
    month = datetime.strftime("%m")
    return month

def get_year(datetime):
    year = datetime.strftime("%Y")
    return year

def bar_graph_active_studies(file, start, end):
    entries = []

    df = pd.read_csv(file)

    # Count kits that have the same date and action
    data = df.groupby(['Date', 'Action']).size().reset_index().rename(columns={0:'count'})


    # Prepare the bar graph
    graph1 = px.bar(data_frame=data, x="Date", y="count", color="Action", orientation="v", barmode='group',
    color_discrete_sequence = ['#222831', '#325288', '#17a2b8'], title="Overall Kit Activity")
    graph1.update_xaxes(title_text='Date (month-year)')
    graph1.update_yaxes(title_text='Number of Kits')
    # Prepare the bar graph to suit html format
    html_graph = graph1.to_html(full_html=False)
    return html_graph




