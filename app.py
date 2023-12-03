import dash
import asyncio
from fxtop import get_rates
from dash import html
from dash import dcc
import pandas as pd
import plotly.express as px


def create_df():
    dfs = asyncio.run(get_rates(1))
    return pd.concat(dfs)

def create_figure(df):
    return px.line(df, x="Date", y="Rate", title="Exchange Rates")
    


app = dash.Dash(__name__)

app.layout = html.Div([
     dcc.Graph(id='graph', figure=create_figure(create_df()))
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
