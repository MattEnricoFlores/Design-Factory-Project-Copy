import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json
import schedule
import time
import datetime
from datetime import datetime
import pytz

app = dash.Dash(__name__)

timer_value = 15 * 60  # 15 minutes
image_path = '/img/Waltikka.png'

# Define the layout of the app
app.layout = html.Div([

    html.Div(id='auto-refresh-text', style={'font-size': '10px'}),
   
    html.H1('Hotelli Waltikka'),
    # html.Button('Update', id='update-button'),  # Reinstated update button

    dcc.Interval(
        id='update-button',
        interval=1 * 1000,  # in milliseconds (15 minutes)
        n_intervals=0
    ),
    # Create a dynamic layout for displaying data for each room
    # html.Div(id='room-name-data-container', children=[]),
    html.Div(id='date-time'),
    html.Div(id='weather-data-container', children=[]),
    
    html.Div(id='room-data-container', children=[]),
    
])

# app.css.append_css({
#     'external_url': 'assets/style.css',
# })

@app.callback(
    Output('auto-refresh-text', 'children'),
    Input('update-button', 'n_intervals')
)
def update_auto_refresh_text(n_intervals):
    return f"Page last refreshed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"  # Use datetime.datetime


### THE ROOM DATA

@app.callback(
    Output('room-data-container', 'children'),  # Update the content of this container
    [Input('update-button', 'n_intervals')]  # Specify the button as an input
)
def update_room_data(n_clicks):
    # Read data from the JSON file containing data for all rooms
    with open('Brain\\data.json', 'r') as json_file:
        data = json.load(json_file)
        
    # Create a list of HTML div elements for each room's data
    room_divs = []
    for room_name, room_data in data.items():

        ## temp 21-23 , humidity 30 - 45, co2  350 - 550  

        temperature = room_data[0]["Temperature"]
        temperature_class = 'average-box correct' if 21 <= temperature <= 23 else 'average-box wrong'

        co2 = room_data[0]["CO2"]
        if co2 is not None:
            co2_class = 'average-box correct' if co2 <= 550 else 'average-box wrong'
        else:
            co2_class = 'average-box unknown'

        room_div = html.Div([
            html.H2(room_name),
            html.Div([
                html.Div([
                    html.Div([f'Lämpötila: ',], className='room1-label', style={'font-weight': 'bold', 'padding-top': '21px'}),
                    html.Div(f'{temperature}', style={'font-size': '20px', 'padding-bottom': '13px'}),
                ], className=temperature_class),
                html.Div([
                    html.Div(f'Kosteus:', className='room1-label', style={'font-weight': 'bold', 'padding-top':'21px'}),
                    html.Div(f'{room_data[0]["Humidity"]}', style={'font-size': '20px', 'padding-bottom': '13px'}),
                ], className="average-box"),
                html.Div([
                    html.Div(f'Hiilidioksidi:', className='room1-label', style={'font-weight': 'bold', 'padding-top':'21px'}),
                    html.Div(f'{co2}', style={'font-size': '20px', 'padding-bottom': '13px'}), 
                ], className=co2_class),
            ], className="average-box-container"),
            # Add more measurements as needed
        ], className='room-container')
        room_divs.append(html.A(room_div, href='http://127.0.0.1:8888/', target='_blank', style={'color':'white', 'text-decoration':'none'}))
        

    return room_divs


@app.callback(
    Output('weather-data-container', 'children'),  # Update the content of this container
    [Input('update-button', 'n_intervals')]  # Specify the button as an input
)
def update_the_weather(n_clicks):
     with open('Brain\\weather.json', 'r') as json_file:
        data = json.load(json_file)
    
        humidity = data.get("humidity")
        temperature = data.get("temperature")

        finlandTz = pytz.timezone("Europe/Helsinki") 
        timeInFinland = datetime.now(finlandTz)
        currentTimeInFinland = timeInFinland.strftime("%H:%M:%S")


        currentDate = datetime.now().strftime('%A, %d %b %Y')
        

        weather_div = html.Div([
            html.Div([
                # html.Div(f'{currentTimeInFinland}'),
                html.Div(f'{currentDate}'),
            ], className='date-time'),
            html.H3("Valkeakoski", style={"font-size":'20px','font-weight': 'bold;'}),
            html.Div([
                html.Div(f'Outside: {temperature}°C, {humidity}%' ,style={"font-size":"18px"}),
            ],className='weather-values'),
        ], className="weather_container")
            
        return weather_div
     
     

# @app.callback(
#     Output('date-time', 'children'),
#     Input('update-button', 'n_intervals')
# )
# def actual_date_time(n_intervals):
#     finlandTz = pytz.timezone("Europe/Helsinki") 
#     timeInFinland = datetime.now(finlandTz)
#     currentTimeInFinland = timeInFinland.strftime("%H:%M:%S")


#     currentDate = datetime.now().strftime('%A.%d.%b.%Y')
#     date_Div = html.Div([
#         html.Div(f'{currentDate}'),
#         html.Div(f'{currentTimeInFinland}'),
#     ], className='date_time')

#     return date_Div

if __name__ == '__main__':
    app.run_server(debug=True)
    
