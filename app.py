import dash
import asyncio
from fxtop import get_rates
from dash import html, Input, Output, State, callback
from dash import dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import webbrowser
from threading import Timer


def create_df(years, cur_from, cur_to):
    dfs = asyncio.run(get_rates(years, cur_from, cur_to))
    return pd.concat(dfs)


def create_figure(df):
    fig = px.line(df, x="Date", y="Rate", title="Exchange Rates")
    fig.layout = go.Layout(title= "Exchange Rates", height = 700)
    return fig


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="graph",
            figure=create_figure(create_df(1, "CHF", "RUB")),
            style={"width": "50%"},
        ),
        html.Label(["Years"]),
        dcc.Dropdown([1, 2, 3, 4, 5], 1, id="years", style={"width": "50%"}),
        html.Label(["From Currency"]),
        dcc.Dropdown(
            ["CHF", "USD", "RUB"], "CHF", id="cur_from", style={"width": "50%"}
        ),
        html.Label(["To Currency"]),
        dcc.Dropdown(["CHF", "USD", "RUB"], "RUB", id="cur_to", style={"width": "50%"}),
    ]
)


@app.callback(
    Output(component_id="graph", component_property="figure", allow_duplicate=True),
    Input(component_id="years", component_property="value"),
    State(component_id="cur_from", component_property="value"),
    State(component_id="cur_to", component_property="value"),
    prevent_initial_call=True
)
def update_graph_years(value, cur_from_val, cur_to_val):
    return create_figure(create_df(int(value), cur_from_val, cur_to_val))


@app.callback(
    Output(component_id="graph", component_property="figure", allow_duplicate=True),
    Input(component_id="cur_from", component_property="value"),
    State(component_id="years", component_property="value"),
    State(component_id="cur_to", component_property="value"),
    State(component_id="cur_from", component_property="value"),
    prevent_initial_call=True
)
def update_graph_cur_from(value, years_val, cur_to_val, cur_from_val):
    if cur_from_val != cur_to_val:
        return create_figure(create_df(int(years_val), value, cur_to_val))
    else:
        return dash.no_update



@app.callback(
    Output(component_id="graph", component_property="figure", allow_duplicate=True),
    Input(component_id="cur_to", component_property="value"),
    State(component_id="years", component_property="value"),
    State(component_id="cur_from", component_property="value"),
    State(component_id="cur_to", component_property="value"),
    prevent_initial_call=True
)
def update_graph_cur_to(value, years_val, cur_from_val, cur_to_val):
    if cur_from_val != cur_to_val:
        return create_figure(create_df(int(years_val), cur_from_val, value))
    else:
        return dash.no_update



port = 8050


def open_browser():
    webbrowser.open_new(f"http://localhost:{port}")


if __name__ == "__main__":
    ##Timer(1, open_browser).start()
    app.run_server(debug=True, port=port)
