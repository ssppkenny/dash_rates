import dash
import asyncio
from fxtop import get_rates
from dash import html, Input, Output, callback
from dash import dcc
import pandas as pd
import plotly.express as px
import webbrowser
from threading import Timer


def create_df(years):
    dfs = asyncio.run(get_rates(years))
    return pd.concat(dfs)


def create_figure(df):
    return px.line(df, x="Date", y="Rate", title="Exchange Rates")


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="graph", figure=create_figure(create_df(1)), style={"width": "50%"}
        ),
        html.Label(["Years"]),
        dcc.Dropdown([1, 2, 3, 4, 5], 1, id="years", style={"width": "50%"}),
    ]
)


@app.callback(
    Output(component_id="graph", component_property="figure"),
    Input(component_id="years", component_property="value"),
)
def update_graph(value):
    return create_figure(create_df(int(value)))


port = 8050


def open_browser():
    webbrowser.open_new(f"http://localhost:{port}")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run_server(debug=False, port=port)
