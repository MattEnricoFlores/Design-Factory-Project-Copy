import dash
from dash import dcc, html
from dash.dependencies import Input, Output
# import dash_core_components as dcc
# import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import json

app = dash.Dash(__name__)


# Define the layout of the app
app.layout = html.Div([
    html.H1('Absoplotly'),
 
    html.Button('update', id='update-button'),

    html.Div([
        html.Div(id='average-temp', className='average-box'),  
        html.Div(id='average-humidity', className='average-box'),  
        html.Div(id='average-co2', className='average-box'), 
    ], style={'display': 'flex', 'justify-content': 'center'}), 

    dcc.Graph(id='temp-graph'),
    dcc.Graph(id='humidity-graph'),
    dcc.Graph(id='co2-graph'),
 
])


app.css.append_css({
    'external_url': 'assets/style.css',
})

 
##Plots, Graphs for all measurements
@app.callback(
    Output('temp-graph', 'figure'),
    [Input('update-button', 'n_clicks')]  # Specify the button as an input
)
def update_graph(n_clicks):
    # Read JSON data from room1.json
    with open('room1.json', 'r') as json_file:
        room1_data = json.load(json_file)
    
    # Read JSON data from room2.json
    with open('room2.json', 'r') as json_file:
        room2_data = json.load(json_file)

    # Extract x (timestamps) and y values from both room data
    room1_timestamps = [item[0] for item in room1_data['results'][0]['series'][0]['values']]
    room1_temps =      [item[1] for item in room1_data['results'][0]['series'][0]['values']]
    room2_timestamps = [item[0] for item in room2_data['results'][0]['series'][0]['values']]
    room2_temps = [item[1] for item in room2_data['results'][0]['series'][0]['values']]

    trace1 = go.Scatter(x=room1_timestamps, y=room1_temps, mode='lines+markers', marker={'color': '#51A3A3'}, name='Room 1')
    trace2 = go.Scatter(x=room2_timestamps, y=room2_temps, mode='lines+markers', marker={'color': '#C3E991'}, name='Room 2')
    layout = go.Layout(
        title='Temperature Comparison', 
        xaxis={'title': 'dateTime', 'gridcolor':'gray'}, 
        yaxis={'title': 'temp', 'gridcolor':'gray'}, 
        plot_bgcolor='#161D2F', 
        paper_bgcolor='#161D2F', 
        font={'color':'white'},
    )

    return {'data': [trace1, trace2], 'layout': layout}

@app.callback(
    Output('humidity-graph', 'figure'),
    [Input('update-button', 'n_clicks')]  # Specify the button as an input
)
def update_graph(n_clicks):
    # Read JSON data from room1.json
    with open('room1.json', 'r') as json_file:
        room1_data = json.load(json_file)
    
    # Read JSON data from room2.json
    with open('room2.json', 'r') as json_file:
        room2_data = json.load(json_file)

    # Extract x (timestamps) and y values from both room data
    room1_timestamps = [item[0] for item in room1_data['results'][0]['series'][0]['values']]
    room1_humidity = [item[2] for item in room1_data['results'][0]['series'][0]['values']]
    room2_timestamps = [item[0] for item in room2_data['results'][0]['series'][0]['values']]
    room2_humidity = [item[2] for item in room2_data['results'][0]['series'][0]['values']]

    trace1 = go.Scatter(x=room1_timestamps, y=room1_humidity, mode='lines+markers', marker={'color': 'blue'}, name='Room 1')
    trace2 = go.Scatter(x=room2_timestamps, y=room2_humidity, mode='lines+markers', marker={'color': 'red'}, name='Room 2')
    layout = go.Layout(title='Humidity Comparison', xaxis={'title': 'dateTime'}, yaxis={'title': 'temp'})

    return {'data': [trace1, trace2], 'layout': layout}

@app.callback(
    Output('co2-graph', 'figure'),
    [Input('update-button', 'n_clicks')]  # Specify the button as an input
)
def update_graph(n_clicks):
    # Read JSON data from room1.json
    with open('room1.json', 'r') as json_file:
        room1_data = json.load(json_file)
    
    # Read JSON data from room2.json
    with open('room2.json', 'r') as json_file:
        room2_data = json.load(json_file)

    # Extract x (timestamps) and y values from both room data
    room1_timestamps = [item[0] for item in room1_data['results'][0]['series'][0]['values']]
    room1_co2 = [item[3] for item in room1_data['results'][0]['series'][0]['values']]
    room2_timestamps = [item[0] for item in room2_data['results'][0]['series'][0]['values']]
    room2_co2 = [item[3] for item in room2_data['results'][0]['series'][0]['values']]

    trace1 = go.Scatter(x=room1_timestamps, y=room1_co2, mode='lines+markers', marker={'color': 'blue'}, name='Room 1')
    trace2 = go.Scatter(x=room2_timestamps, y=room2_co2, mode='lines+markers', marker={'color': 'red'}, name='Room 2')
    layout = go.Layout(title='co2 Comparison', xaxis={'title': 'dateTime'}, yaxis={'title': 'temp'})

    return {'data': [trace1, trace2], 'layout': layout}


@app.callback(
    Output('average-temp', 'children'),  # Update the content of the div
    [Input('update-button', 'n_clicks')]  # Specify the button as an input
)
def update_average_temp(n_clicks):
    # Read data from both JSON files
    data = []

    with open('room1.json', 'r') as json_file:
        data.extend(json.load(json_file)['results'][0]['series'][0]['values'])

    with open('room2.json', 'r') as json_file:
        data.extend(json.load(json_file)['results'][0]['series'][0]['values'])

    # Extract temperature values from the merged data
    y_values = [item[1] for item in data]

    # Calculate the average temperature
    average = sum(y_values) / len(y_values)

    if 21.5 <= average <= 23:
        background = 'correct'
    else:
        background = 'wrong'

    return html.Div([
        html.Div(f'Average Temperature:', className='average-label', style={'font-weight': 'bold'}),
        html.Div(f'{average:.2f}', className='average-temp', style={'font-size': '50px'})
    ], className= background)

@app.callback(
    Output('average-humidity', 'children'),  # Update the content of the div
    [Input('update-button', 'n_clicks')]  # Specify the button as an input
)
def update_average_humidity(n_clicks):
       # Read data from both JSON files
    data = []

    with open('room1.json', 'r') as json_file:
        data.extend(json.load(json_file)['results'][0]['series'][0]['values'])

    with open('room2.json', 'r') as json_file:
        data.extend(json.load(json_file)['results'][0]['series'][0]['values'])


    y_values = [item[2] for item in data]


    average = sum(y_values) / len(y_values)

    if 30 <= average <= 45:
        background = 'correct'
    else:
        background = 'wrong'

    return html.Div([
        html.Div(f'Average Humidity:', className='average-label', style={'font-weight': 'bold'}),
        html.Div(f'{average:.2f}', className='average-humidity', style={'font-size': '50px'})
    ], className= background)

@app.callback(
    Output('average-co2', 'children'),  # Update the content of the div
    [Input('update-button', 'n_clicks')]  # Specify the button as an input
)
def update_average_humidity(n_clicks):
       # Read data from both JSON files
    data = []

    with open('room1.json', 'r') as json_file:
        data.extend(json.load(json_file)['results'][0]['series'][0]['values'])

    with open('room2.json', 'r') as json_file:
        data.extend(json.load(json_file)['results'][0]['series'][0]['values'])

 
    y_values = [item[3] for item in data]

   
    average = sum(y_values) / len(y_values)

    if 350 <= average <= 550:
        background = 'correct'
    else:
        background = 'wrong'

    return html.Div([
        html.Div(f'Average co2:', className='average-label', style={'font-weight': 'bold'}),
        html.Div(f'{average:.2f}', className='average-co2', style={'font-size': '50px'})
    ], className=background)

if __name__ == '__main__':
    app.run_server(debug=True)
