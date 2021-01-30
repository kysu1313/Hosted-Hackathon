# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from files.read_csv import Data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


reader = Data()
names = reader.get_all_file_names()
dfs = reader.get_dfs_for_all_files()
labels = [filename.split('_')[0] for filename in names]

base_path = 'data/Analysis/'
for index, name in enumerate(labels):
    dfs[index].name = name

# time = [1, 2, 3, 1, 2, 3]
fig = px.line(dfs[0], x='Datetime', y='Predicted')

lines = []


df = dfs[5]

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009)
fig['layout']['margin'] = {'l': 50, 'r': 50, 'b': 100, 't': 100}

fig.append_trace({'x':df['Datetime'], 'y':df['Actual'], 'type':'scatter', 'name':'Actual'},1,1)
fig.append_trace({'x':df['Datetime'], 'y':df['Predicted'], 'type':'scatter', 'name':'Predicted'},1,1)

# Add range slider
fig.update_layout(
    title=df.name,
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="Hour",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="Day",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="Month",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="Year",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
fig.update_layout(hovermode='x unified')

predictive = dcc.Graph(
    id='example-graph',
    figure=fig
)
