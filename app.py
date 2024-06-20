import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os
import pdfkit

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
])
app.title = 'Natural Gas Compression Station Performance Dashboard'

# Load data
data_dir = os.path.join(os.path.dirname(__file__), 'data')
real_time_file_path = os.path.join(data_dir, 'aggregated_real_time_data.xlsx')
historical_file_path = os.path.join(
    data_dir, 'aggregated_historical_data.xlsx')

real_time_data = pd.read_excel(real_time_file_path, engine='openpyxl')
historical_data = pd.read_excel(historical_file_path, engine='openpyxl')

# Ensure the 'timestamp' column exists and is in datetime format
real_time_data['timestamp'] = pd.to_datetime(real_time_data['timestamp'])
historical_data['timestamp'] = pd.to_datetime(historical_data['timestamp'])

# Calculate averages
avg_pressure = real_time_data['pressure'].mean()
avg_temperature = real_time_data['temperature'].mean()
avg_flow_rate = real_time_data['flow_rate'].mean()

# Define the layout of the dashboard
app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(
        children=[
            html.Img(src='/assets/ghanagas_logo.png'),
            html.H1('AMCS PERFORMANCE REPORT DASHBOARD')
        ],
        className='navbar'
    ),
    html.Div(
        children=[
            html.Div('Home', id='breadcrumb', className='breadcrumb'),
            html.Button('Generate PDF Report', id='pdf-button',
                        n_clicks=0, className='pdf-button'),
            html.Div(id='pdf-output', style={'display': 'none'})
        ],
        className='pdf-container'
    ),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H2("Views"),
                    html.Hr(),
                    html.P(
                        [html.I(className="fa fa-tachometer pressure-icon"), " Metrics"]),
                    html.A([html.I(className="fa fa-tachometer pressure-icon"), " Pressure"],
                           href="/metrics/pressure", className="link pressure-link"),
                    html.A([html.I(className="fa fa-thermometer-half temperature-icon"), " Temperature"],
                           href="/metrics/temperature", className="link temperature-link"),
                    html.A([html.I(className="fa fa-tachometer flow-icon"), " Flow Rate"],
                           href="/metrics/flow_rate", className="link flow-link"),
                    html.Hr(),
                    html.P([html.I(className="fa fa-clock-o"), " Time Range"]),
                    html.A([html.I(className="fa fa-sun-o"), " Day"],
                           href="/time/day", className="link"),
                    html.A([html.I(className="fa fa-calendar-o"), " Week"],
                           href="/time/week", className="link"),
                    html.A([html.I(className="fa fa-calendar"), " Month"],
                           href="/time/month", className="link"),
                    html.A([html.I(className="fa fa-calendar-check-o"),
                           " Quarter"], href="/time/quarter", className="link"),
                    html.A([html.I(className="fa fa-calendar-check-o"),
                           " Year"], href="/time/year", className="link"),
                ],
                className='sidebar'
            ),
            html.Div(
                children=[
                    html.Div(children=[
                        html.Div(children=[
                            html.H3('Average Pressure'),
                            html.P(f'{avg_pressure:.2f}', className='card'),
                            html.P('barg', className='lower-card')
                        ], className='card'),

                        html.Div(children=[
                            html.H3('Average Temperature'),
                            html.P(f'{avg_temperature:.2f}', className='card'),
                            html.P('°C', className='lower-card')
                        ], className='card'),

                        html.Div(children=[
                            html.H3('Average Flow Rate'),
                            html.P(f'{avg_flow_rate:.2f}', className='card'),
                            html.P('mmscfd', className='lower-card')
                        ], className='card'),
                    ], className='card-container'),

                    dcc.Graph(id='real-time-graph'),
                    dcc.Graph(id='historical-graph')
                ],
                className='content'
            )
        ],
        className='container'
    )
])

# Callback to update the graphs based on selected metrics and time range


@app.callback(
    Output('real-time-graph', 'figure'),
    Output('historical-graph', 'figure'),
    Output('breadcrumb', 'children'),
    Input('url', 'pathname')
)
def update_graphs(pathname):
    # Determine the selected time range and metrics based on the URL path
    time_range_map = {
        '/time/day': 'Day',
        '/time/week': 'Week',
        '/time/month': 'Month',
        '/time/quarter': 'Quarter',
        '/time/year': 'Year'
    }
    metric_map = {
        '/metrics/pressure': 'Pressure',
        '/metrics/temperature': 'Temperature',
        '/metrics/flow_rate': 'Flow Rate'
    }

    selected_time_range = 'Day'
    selected_metrics = ['Pressure', 'Temperature', 'Flow Rate']

    for key, value in time_range_map.items():
        if key in pathname:
            selected_time_range = value

    for key, value in metric_map.items():
        if key in pathname:
            selected_metrics = [value]

    # Filter data based on selected time range
    filtered_real_time_data = real_time_data.resample(
        selected_time_range[0], on='timestamp').mean()
    filtered_historical_data = historical_data.resample(
        selected_time_range[0], on='timestamp').mean()

    # Create figures
    fig_real_time = px.line(filtered_real_time_data, x='timestamp',
                            y=selected_metrics, title='Real-Time Data')
    fig_historical = px.line(filtered_historical_data, x='timestamp',
                             y=selected_metrics, title='Historical Data')

    # Create breadcrumb
    breadcrumb = html.Div([
        html.A('Home', href='/'),
        ' / ',
        html.Span(f'{selected_metrics[0]} - {selected_time_range}')
    ])

    return fig_real_time, fig_historical, breadcrumb

# Callback to generate PDF


@app.callback(
    Output('pdf-output', 'children'),
    Input('pdf-button', 'n_clicks'),
    prevent_initial_call=True
)
def generate_pdf(n_clicks):
    if n_clicks > 0:
        # Generate PDF of current view
        options = {
            'page-size': 'Letter',
            'encoding': 'UTF-8',
        }
        pdfkit.from_url('http://localhost:8050', 'report.pdf', options=options)
        return html.A('Download PDF', href='/report.pdf')


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
