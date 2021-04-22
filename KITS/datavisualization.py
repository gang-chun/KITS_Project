import pandas as pd
import plotly.express as px

def get_month(datetime):
    month = datetime.strftime("%m")
    return month

def get_year(datetime):
    year = datetime.strftime("%Y")
    return year

def bar_graph_kit_activity(csv_file, startdate, enddate):

    df = pd.read_csv(file)

    # Count kits that have the same date and action
    data = df.groupby(['Date', 'Action']).size().reset_index().rename(columns={0:'count'})

    # Prepare the bar graph
    graph1 = px.bar(data_frame=data, x="Date", y="count", color="Action", orientation="v", barmode='group',
    color_discrete_sequence = ['#222831', '#325288', '#17a2b8'], title="Overall Kit Activity")

    #Graph formatting stuff
    graph1.update_layout(plot_bgcolor='#dce4e4', autosize=True, margin=dict(l=30, r=30,b=60,t=60,pad=4))
    graph1.update_xaxes(title_text='Date (month-year)')
    graph1.update_yaxes(title_text='Number of Kits', dtick=1)

    # Prepare the bar graph to suit html format
    html_graph = graph1.to_html(full_html=False)
    return html_graph




