import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP, "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
])

# Sample data
np.random.seed(42)
df = pd.DataFrame({
    "Time": pd.date_range(start="2023-01-01", periods=100, freq="D"),
    "Pressure": np.random.randn(100).cumsum(),
    "Temperature": np.random.randn(100).cumsum(),
    "Flow": np.random.randn(100).cumsum(),
    "Pressure_Inlet": np.random.randn(100).cumsum(),
    "Pressure_Outlet": np.random.randn(100).cumsum(),
    "Temperature_Inlet": np.random.randn(100).cumsum(),
    "Temperature_Outlet": np.random.randn(100).cumsum(),
    "Flow_Inlet": np.random.randn(100).cumsum(),
    "Flow_Outlet": np.random.randn(100).cumsum()
})

# Define the navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                html.Img(src="/assets/ghanagas_logo.png",
                         height="60px", className="navbar-logo"),
                href="/",
            ),
            dbc.NavbarBrand(
                [
                    "AMCS PERFORMANCE REPORT DASHBOARD",
                    html.I(className="fas fa-chart-line ml-2")
                ],
                className="mx-auto"
            ),
        ],
        fluid=True,
    ),
    dark=True,
    className="navbar"
)

# Define the sidebar
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [html.I(className="fas fa-chart-line mr-2"),
             html.Span("Overview")],
            href="/overview", id="overview-link", className="nav-link"
        ),
        dbc.NavLink(
            [html.I(className="fas fa-tachometer-alt mr-2"),
             html.Span("Pressure")],
            href="/pressure", id="pressure-link", className="nav-link"
        ),
        dbc.NavLink(
            [html.I(className="fas fa-thermometer-half mr-2"),
             html.Span("Temperature")],
            href="/temperature", id="temperature-link", className="nav-link"
        ),
        dbc.NavLink(
            [html.I(className="fas fa-water mr-2"), html.Span("Flow")],
            href="/flow", id="flow-link", className="nav-link"
        ),
        html.Hr(),
        dbc.NavLink(
            [html.I(className="fas fa-calendar-day mr-2"), html.Span("Day")],
            href="/day", id="day-link", className="nav-link"
        ),
        dbc.NavLink(
            [html.I(className="fas fa-calendar-week mr-2"), html.Span("Week")],
            href="/week", id="week-link", className="nav-link"
        ),
        dbc.NavLink(
            [html.I(className="fas fa-calendar-alt mr-2"), html.Span("Month")],
            href="/month", id="month-link", className="nav-link"
        ),
        dbc.NavLink(
            [html.I(className="fas fa-calendar-week mr-2"),
             html.Span("Quarter")],
            href="/quarter", id="quarter-link", className="nav-link"
        ),
        dbc.NavLink(
            [html.I(className="fas fa-calendar mr-2"), html.Span("Year")],
            href="/year", id="year-link", className="nav-link"
        ),
    ],
    vertical=True,
    pills=True,
    className="sidebar"
)

# Define the layout
app.layout = dbc.Container(
    [
        navbar,
        dbc.Row(
            [
                dbc.Col(sidebar, width=2),
                dbc.Col(html.Div(id="page-content",
                        className="main-content"), width=10),
            ]
        ),
    ],
    fluid=True,
)

# Define the callback for page navigation and time range selection


@app.callback(
    [Output(f"{link}-link", "className") for link in ["overview", "pressure",
                                                      "temperature", "flow", "day", "week", "month", "quarter", "year"]],
    [Input("overview-link", "n_clicks"),
     Input("pressure-link", "n_clicks"),
     Input("temperature-link", "n_clicks"),
     Input("flow-link", "n_clicks"),
     Input("day-link", "n_clicks"),
     Input("week-link", "n_clicks"),
     Input("month-link", "n_clicks"),
     Input("quarter-link", "n_clicks"),
     Input("year-link", "n_clicks")]
)
def update_active_link(*args):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ["nav-link"] * 9
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        return ["nav-link active" if f"{link}-link" == button_id else "nav-link" for link in ["overview", "pressure", "temperature", "flow", "day", "week", "month", "quarter", "year"]]


@app.callback(
    Output("page-content", "children"),
    [Input("overview-link", "n_clicks"),
     Input("pressure-link", "n_clicks"),
     Input("temperature-link", "n_clicks"),
     Input("flow-link", "n_clicks"),
     Input("day-link", "n_clicks"),
     Input("week-link", "n_clicks"),
     Input("month-link", "n_clicks"),
     Input("quarter-link", "n_clicks"),
     Input("year-link", "n_clicks")]
)
def display_page(overview_clicks, pressure_clicks, temperature_clicks, flow_clicks, day_clicks, week_clicks, month_clicks, quarter_clicks, year_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return html.Div("Welcome to the AMCS PERFORMANCE REPORT DASHBOARD")
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "overview-link":
            return create_overview_page()
        elif button_id == "pressure-link":
            return create_pressure_page()
        elif button_id == "temperature-link":
            return create_temperature_page()
        elif button_id == "flow-link":
            return create_flow_page()
        elif button_id == "day-link":
            return create_time_page("Day")
        elif button_id == "week-link":
            return create_time_page("Week")
        elif button_id == "month-link":
            return create_time_page("Month")
        elif button_id == "quarter-link":
            return create_time_page("Quarter")
        elif button_id == "year-link":
            return create_time_page("Year")

# Main content functions


def create_overview_page():
    return html.Div([
        html.H2("Overview"),
        create_chart_card("Pressure", df["Pressure"]),
        create_chart_card("Temperature", df["Temperature"]),
        create_chart_card("Flow", df["Flow"]),
        create_line_chart("Overview", df)
    ])


def create_pressure_page():
    return html.Div([
        html.H2("Pressure"),
        create_chart_card("Avg. Pressure", df["Pressure"]),
        create_line_chart("Pressure Over Time", df, y_column="Pressure"),
        create_bar_chart("Pressure Inlet vs Outlet", df,
                         "Pressure_Inlet", "Pressure_Outlet")
    ])


def create_temperature_page():
    return html.Div([
        html.H2("Temperature"),
        create_chart_card("Avg. Temperature", df["Temperature"]),
        create_line_chart("Temperature Over Time", df, y_column="Temperature"),
        create_bar_chart("Temperature Inlet vs Outlet", df,
                         "Temperature_Inlet", "Temperature_Outlet")
    ])


def create_flow_page():
    return html.Div([
        html.H2("Flow"),
        create_chart_card("Avg. Flow", df["Flow"]),
        create_line_chart("Flow Over Time", df, y_column="Flow"),
        create_bar_chart("Flow Inlet vs Outlet", df,
                         "Flow_Inlet", "Flow_Outlet")
    ])


def create_time_page(time_range):
    return html.Div([
        html.H2(f"{time_range} Report"),
        create_chart_card(f"Avg. {time_range} Pressure", df["Pressure"]),
        create_chart_card(f"Avg. {time_range} Temperature", df["Temperature"]),
        create_chart_card(f"Avg. {time_range} Flow", df["Flow"]),
        create_line_chart(f"{time_range} Report", df)
    ])


def create_chart_card(title, data):
    avg_value = data.mean()
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title"),
            html.P(f"{avg_value:.2f}", className="card-text")
        ]),
        className="mb-3"
    )


def create_line_chart(title, df, y_column="Pressure"):
    fig = px.line(df, x="Time", y=y_column, title=title)
    return dcc.Graph(figure=fig)


def create_bar_chart(title, df, y_column1, y_column2):
    fig = px.bar(df, x="Time", y=[y_column1, y_column2], title=title)
    return dcc.Graph(figure=fig)


if __name__ == "__main__":
    app.run_server(debug=True)
