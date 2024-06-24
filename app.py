"""
This module creates a Plant Performance Dashboard using Dash.
The dashboard includes a navbar, sidebar, and main content area
with cards displaying current values of parameters, a line graph
showing trends over time, historical comparison graphs, and a bar chart
and donut chart showing averages of these parameters.
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

# Load the data from the Excel file
FILE_PATH = 'raw_cleaned_data.xlsx'
data = pd.read_excel(FILE_PATH)

# Print the column names to verify
print(data.columns)

# Use 'Day' as the date column
DATE_COLUMN = 'Day'

# Convert the date column to datetime format
data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

# Initialize the Dash app
app = dash.Dash(__name__)

# Navbar
navbar = html.Div(
    className='navbar',
    children=[
        html.Img(src='/assets/ghanagas_logo.png', className='logo'),
        html.H1('Plant Performance Dashboard')
    ]
)

# Sidebar
sidebar = html.Div(
    className='sidebar',
    children=[
        html.H2('Navigation'),
        dcc.Link('Overview', href='/overview', className='sidebar-link'),
        dcc.Link('Pressure', href='/pressure', className='sidebar-link'),
        dcc.Link('Temperature', href='/temperature', className='sidebar-link'),
        dcc.Link('Flow', href='/flow', className='sidebar-link'),
        html.H2('Time Range'),
        dcc.RadioItems(
            id='time-range',
            options=[
                {'label': 'Day', 'value': 'D'},
                {'label': 'Week', 'value': 'W'},
                {'label': 'Month', 'value': 'ME'},
                {'label': 'Quarter', 'value': 'Q'},
                {'label': 'Year', 'value': 'A'},
            ],
            value='ME',  # Month-end
            className='radio-items'
        )
    ]
)

# Main Content
main_content = html.Div(
    className='main-content',
    children=[
        html.Div(
            className='cards',
            children=[
                html.Div(id='pressure-card', className='card'),
                html.Div(id='temperature-card', className='card'),
                html.Div(id='flow-card', className='card')
            ]
        ),
        dcc.Graph(id='line-graph'),
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='donut-chart'),
        dcc.Graph(id='comparison-graph')
    ]
)

# App Layout
app.layout = html.Div(
    className='container',
    children=[
        navbar,
        sidebar,
        main_content
    ]
)


@app.callback(
    [Output('pressure-card', 'children'),
     Output('temperature-card', 'children'),
     Output('flow-card', 'children'),
     Output('line-graph', 'figure'),
     Output('bar-chart', 'figure'),
     Output('donut-chart', 'figure'),
     Output('comparison-graph', 'figure')],
    [Input('time-range', 'value')]
)
def update_dashboard(time_range):
    """
    Update the dashboard based on the selected time range.

    Parameters:
    time_range (str): The selected time range for resampling the data.

    Returns:
    tuple: Updated values for the pressure, temperature, and flow cards,
           and updated figures for the line graph, bar chart, donut chart,
           and historical comparison graph.
    """
    # Adjust the time range to use 'ME' for month-end
    time_range = 'ME' if time_range == 'M' else time_range

    # Filter data based on the selected time range
    filtered_data = data.set_index(DATE_COLUMN).resample(
        time_range).mean().reset_index()

    # Get the latest values for the cards
    pressure = filtered_data['Inlet Pressure (barg)'].iloc[-1]
    temperature = filtered_data['Inlet Temperature °C'].iloc[-1]
    flow = filtered_data['Inlet Flow (MMscfd)'].iloc[-1]

    # Create cards content
    pressure_card = f'Pressure: {pressure:.2f}'
    temperature_card = f'Temperature: {temperature:.2f}'
    flow_card = f'Flow: {flow:.2f}'

    # Create line graph
    line_fig = px.line(
        filtered_data, x=DATE_COLUMN,
        y=['Inlet Pressure (barg)', 'Inlet Temperature °C',
           'Inlet Flow (MMscfd)'],
        title='Parameters Over Time'
    )

    # Create bar chart
    avg_pressure = filtered_data['Inlet Pressure (barg)'].mean()
    avg_temperature = filtered_data['Inlet Temperature °C'].mean()
    avg_flow = filtered_data['Inlet Flow (MMscfd)'].mean()
    bar_fig = go.Figure(
        data=[go.Bar(x=['Pressure', 'Temperature', 'Flow'],
                     y=[avg_pressure, avg_temperature, avg_flow])]
    )
    bar_fig.update_layout(title='Average Parameters')

    # Create donut chart
    donut_fig = go.Figure(
        data=[go.Pie(labels=['Pressure', 'Temperature', 'Flow'],
                     values=[avg_pressure, avg_temperature, avg_flow], hole=.3)]
    )
    donut_fig.update_layout(title='Parameters Distribution')

    # Create historical comparison graph
    # Compare with the previous period
    if time_range == 'ME':
        prev_period_data = data.set_index(DATE_COLUMN).resample(
            'M').mean().shift(1).reset_index()
    elif time_range == 'A':
        prev_period_data = data.set_index(DATE_COLUMN).resample(
            'A').mean().shift(1).reset_index()
    elif time_range == 'Q':
        prev_period_data = data.set_index(DATE_COLUMN).resample(
            'Q').mean().shift(1).reset_index()
    elif time_range == 'W':
        prev_period_data = data.set_index(DATE_COLUMN).resample(
            'W').mean().shift(1).reset_index()
    elif time_range == 'D':
        prev_period_data = data.set_index(DATE_COLUMN).resample(
            'D').mean().shift(1).reset_index()
    else:
        prev_period_data = data.set_index(DATE_COLUMN).resample(
            'ME').mean().shift(1).reset_index()

    comparison_fig = go.Figure()
    comparison_fig.add_trace(go.Scatter(x=filtered_data[DATE_COLUMN], y=filtered_data['Inlet Pressure (barg)'],
                                        mode='lines', name='Current Period Pressure'))
    comparison_fig.add_trace(go.Scatter(x=prev_period_data[DATE_COLUMN], y=prev_period_data['Inlet Pressure (barg)'],
                                        mode='lines', name='Previous Period Pressure', line=dict(dash='dash')))
    comparison_fig.add_trace(go.Scatter(x=filtered_data[DATE_COLUMN], y=filtered_data['Inlet Temperature °C'],
                                        mode='lines', name='Current Period Temperature'))
    comparison_fig.add_trace(go.Scatter(x=prev_period_data[DATE_COLUMN], y=prev_period_data['Inlet Temperature °C'],
                                        mode='lines', name='Previous Period Temperature', line=dict(dash='dash')))
    comparison_fig.add_trace(go.Scatter(x=filtered_data[DATE_COLUMN], y=filtered_data['Inlet Flow (MMscfd)'],
                                        mode='lines', name='Current Period Flow'))
    comparison_fig.add_trace(go.Scatter(x=prev_period_data[DATE_COLUMN], y=prev_period_data['Inlet Flow (MMscfd)'],
                                        mode='lines', name='Previous Period Flow', line=dict(dash='dash')))
    comparison_fig.update_layout(title='Historical Comparison')

    return (
        pressure_card,
        temperature_card,
        flow_card,
        line_fig,
        bar_fig,
        donut_fig,
        comparison_fig
    )


if __name__ == '__main__':
    app.run_server(debug=True)
