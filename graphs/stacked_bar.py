import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from classes.read_csv import Data

reader = Data()

dfs = reader.get_dfs_for_all_files()

# df = dfs[0]

print(dfs)

df = pd.read_excel(
    "https://github.com/chris1610/pbpython/blob/master/data/salesfunnel.xlsx?raw=True"
)



pv = pd.pivot_table(df, index=['Name'], columns=["Status"], values=[
                    'Quantity'], aggfunc=sum, fill_value=0)


trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declined')], name='Declined')
trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presented')], name='Presented')
trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'won')], name='Won')

bar_chart = dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace1, trace2, trace3, trace4],
            'layout':
            go.Layout(title='Order Status by Customer', barmode='stack')
        })
