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
from files import predictive_plot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


reader = Data()
names = reader.get_all_file_names()
dfs = reader.get_dfs_for_all_files()
labels = [filename.split('_')[0] for filename in names]
locations = []




base_path = 'data/Analysis/'
for index, name in enumerate(labels):
    dfs[index].name = name

fig = px.line(dfs[0], x='Datetime', y='Predicted')

lines = []

# for pos in range(0, 5):
# line = px.line(dfs[0], x='Datetime',
#             y='Predicted', color='Actual')
# line.update_traces(mode='markers+lines')
# lines.append(line)



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


app.layout = html.Div(children=[
        html.Div(id='dd-output-container', children=[]),
        predictive,
        dcc.Dropdown(
            id='demo-dropdown',
            options=locations,
            value=names[0],
            multi=True
        )
    ])







# @app.callback(
#     dash.dependencies.Output('dd-output-container', 'children'),
#     [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(filenames):
    """
    Predictive Graph.
    Shows actual and predicted values for the assiciated building.
    """
    base_path = 'data/Analysis/'
    for index, name in enumerate(labels):
        dfs[index].name = name
        print(dfs[index].name)
        print(dfs[index])

    merged = pd.read_csv(base_path + filenames[0])
    merged = merged[['Datetime', 'Actual']]
    merged = merged.rename(columns={"Actual": filenames[0]})

    time = [1, 2, 3, 1, 2, 3]
    fig = px.line(dfs[0], x='Datetime', y='Predicted', color='Actual')

    lines = []

    # for pos in range(0, 5):
    line = px.line(dfs[pos], x='Datetime',
                y='Predicted', color=names[pos])
    line.update_traces(mode='markers+lines')
    lines.append(line)

    # fig.update_traces(mode='markers+lines')

    layout = go.Layout(xaxis={'title': 'Time'},
                    yaxis={'title': 'Produced Units'},
                    margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                    hovermode='closest')

    fig = go.Figure(data=lines, layout=layout)
    predictive = dcc.Graph(
        id='example-graph',
        figure=fig
    )
    return predictive
    

if __name__ == '__main__':
    app.run_server(debug=True)
