import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = 'Natural Gas Compression Station Performance Dashboard'

# Load data
data_dir = os.path.join(os.path.dirname(__file__), 'data')
real_time_file_path = os.path.join(data_dir, 'aggregated_real_time_data.xlsx')
historical_file_path = os.path.join(
    data_dir, 'aggregated_historical_data.xlsx')

real_time_data = pd.read_excel(real_time_file_path, engine='openpyxl')
historical_data = pd.read_excel(historical_file_path, engine='openpyxl')

# Calculate averages
avg_pressure = real_time_data['pressure'].mean()
avg_temperature = real_time_data['temperature'].mean()
avg_flow_rate = real_time_data['flow_rate'].mean()

# Define the layout of the dashboard
app.layout = html.Div(children=[
    html.Div(
        children=[
            html.H2("Views"),
            html.Hr(),
            html.P("Metrics"),
            dcc.Checklist(
                id='metric-selector',
                options=[
                    {'label': 'Pressure', 'value': 'pressure'},
                    {'label': 'Temperature', 'value': 'temperature'},
                    {'label': 'Flow Rate', 'value': 'flow_rate'}
                ],
                value=['pressure', 'temperature', 'flow_rate']
            ),
            html.Hr(),
            html.P("Time Range"),
            dcc.RadioItems(
                id='time-range-selector',
                options=[
                    {'label': 'Day', 'value': 'D'},
                    {'label': 'Week', 'value': 'W'},
                    {'label': 'Month', 'value': 'M'},
                    {'label': 'Quarter', 'value': 'Q'},
                    {'label': 'Year', 'value': 'Y'}
                ],
                value='D'
            ),
        ],
        style={
            'padding': '20px',
            'flex': '1',
            'backgroundColor': '#f8f9fa',
            'borderRight': '1px solid #ddd'
        }
    ),
    html.Div(
        children=[
            html.H1('Natural Gas Compression Station Dashboard', style={
                    'textAlign': 'center', 'marginBottom': '20px'}),
            html.Div(children=[
                html.Div(children=[
                    html.H3('Average Pressure', style={'marginBottom': '5px'}),
                    html.P(f'{avg_pressure:.2f} barg', style={
                           'fontSize': '24px', 'fontWeight': 'bold', 'color': '#007bff'})
                ], className='card'),

                html.Div(children=[
                    html.H3('Average Temperature', style={
                            'marginBottom': '5px'}),
                    html.P(f'{avg_temperature:.2f} °C', style={
                           'fontSize': '24px', 'fontWeight': 'bold', 'color': '#007bff'})
                ], className='card'),

                html.Div(children=[
                    html.H3('Average Flow Rate', style={
                            'marginBottom': '5px'}),
                    html.P(f'{avg_flow_rate:.2f} mmscfd', style={
                           'fontSize': '24px', 'fontWeight': 'bold', 'color': '#007bff'})
                ], className='card'),
            ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '20px'}),

            dcc.Graph(id='real-time-graph', style={'marginBottom': '20px'}),
            dcc.Graph(id='historical-graph')
        ],
        style={'padding': '20px', 'flex': '4'}
    )
], style={'display': 'flex'})

# Define the card style in the app's CSS
app.css.append_css({
    'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
})

# Define the custom CSS style with fonts
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
            }
            .card h3, .card p {
                font-family: 'Roboto', sans-serif;
            }
            .card {
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                margin: 5px;
                text-align: center;
                flex: 1;
            }
            .container {
                display: flex;
                flex-direction: column;
                justify-content: space-around;
            }
            .filters {
                padding: 20px;
                flex: 1;
                backgroundColor: #f8f9fa;
                borderRight: 1px solid #ddd;
                font-family: 'Roboto', sans-serif;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Callbacks to update the graphs based on selected metrics and time range


@app.callback(
    Output('real-time-graph', 'figure'),
    Output('historical-graph', 'figure'),
    Input('metric-selector', 'value'),
    Input('time-range-selector', 'value')
)
def update_graphs(selected_metrics, selected_time_range):
    # Filter data based on selected time range
    filtered_real_time_data = real_time_data.resample(
        selected_time_range, on='timestamp').mean()
    filtered_historical_data = historical_data.resample(
        selected_time_range, on='timestamp').mean()

    # Create figures
    fig_real_time = px.line(filtered_real_time_data, x='timestamp',
                            y=selected_metrics, title='Real-Time Data')
    fig_historical = px.line(filtered_historical_data, x='timestamp',
                             y=selected_metrics, title='Historical Data')

    return fig_real_time, fig_historical


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
