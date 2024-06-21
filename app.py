import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output

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
            dbc.NavbarBrand("AMCS PERFORMANCE REPORT DASHBOARD",
                            className="mx-auto"),
        ],
        fluid=True,
    ),
    dark=True,
    className="navbar custom-navbar"
)

# Define the sidebar
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [html.I(className="fas fa-tachometer-alt mr-2"), "Pressure"],
            href="/pressure", id="pressure-link", className="nav-link"
        ),
        dbc.NavLink(
            [html.I(className="fas fa-thermometer-half mr-2"), "Temperature"],
            href="/temperature", id="temperature-link", className="nav-link"
        ),
        dbc.NavLink(
            [html.I(className="fas fa-water mr-2"), "Flow"],
            href="/flow", id="flow-link", className="nav-link"
        ),
        html.Hr(),
        html.P("Select Time Range:", className="sidebar-title"),
        dbc.RadioItems(
            options=[
                {"label": [
                    html.I(className="fas fa-calendar-day mr-2"), "Day"], "value": "day"},
                {"label": [
                    html.I(className="fas fa-calendar-week mr-2"), "Week"], "value": "week"},
                {"label": [
                    html.I(className="fas fa-calendar-alt mr-2"), "Month"], "value": "month"},
                {"label": [html.I(
                    className="fas fa-calendar-quarter mr-2"), "Quarter"], "value": "quarter"},
                {"label": [html.I(className="fas fa-calendar mr-2"),
                           "Year"], "value": "year"},
            ],
            value="day",
            id="time-range",
            className="radio-items"
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
    Output("page-content", "children"),
    [Input("pressure-link", "n_clicks"),
     Input("temperature-link", "n_clicks"),
     Input("flow-link", "n_clicks"),
     Input("time-range", "value")]
)
def display_page(pressure_clicks, temperature_clicks, flow_clicks, time_range):
    ctx = dash.callback_context

    if not ctx.triggered:
        return html.Div("Welcome to the AMCS PERFORMANCE REPORT DASHBOARD")
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "pressure-link":
            return html.Div(f"Pressure page content - Time Range: {time_range}")
        elif button_id == "temperature-link":
            return html.Div(f"Temperature page content - Time Range: {time_range}")
        elif button_id == "flow-link":
            return html.Div(f"Flow page content - Time Range: {time_range}")
        elif button_id == "time-range":
            # Update based on the currently selected page
            current_page = [p["props"]["children"]
                            for p in sidebar.children if "active" in p["props"]["className"]]
            if current_page:
                return html.Div(f"{current_page[0]} page content - Time Range: {time_range}")
            else:
                return html.Div("Welcome to the AMCS PERFORMANCE REPORT DASHBOARD")


if __name__ == "__main__":
    app.run_server(debug=True)
