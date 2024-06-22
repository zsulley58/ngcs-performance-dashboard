import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP, "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
])

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
            return html.Div("Overview page content")
        elif button_id == "pressure-link":
            return html.Div("Pressure page content")
        elif button_id == "temperature-link":
            return html.Div("Temperature page content")
        elif button_id == "flow-link":
            return html.Div("Flow page content")
        elif button_id == "day-link":
            return html.Div("Day page content")
        elif button_id == "week-link":
            return html.Div("Week page content")
        elif button_id == "month-link":
            return html.Div("Month page content")
        elif button_id == "quarter-link":
            return html.Div("Quarter page content")
        elif button_id == "year-link":
            return html.Div("Year page content")


if __name__ == "__main__":
    app.run_server(debug=True)
