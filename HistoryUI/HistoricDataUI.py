import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/historystyle.css'],
    suppress_callback_exceptions=True
)

app.layout = dbc.Row(
    [
        dbc.Row(
            [
        html.H1(id='room-title'),
    ]),
        dbc.Row(
            [
                dbc.Col([
                    dbc.Row([
                        dbc.Button("Etusivulle", href="http://127.0.0.1:8050/", external_link=True, className="me-1 button"),
                    ],
                     className="d-grip gap-2 d-md-flex justify-content-md-center"),
                    dbc.Row([
                        dcc.Dropdown(
                            options=[
                                {'label': '24 tuntia', 'value': '24_hours'},
                                {'label': 'Viikko', 'value': '1_week'},
                                {'label': 'Kuukausi', 'value': '1_month'},
                                {'label': '6 Kuukautta', 'value': '6_month'},
                                {'label': '1 vuosi', 'value': '1_year'},
                            ],
                            value="24_hours",
                            id="data",
                            className="timeOptions"
                        )
                    ], align='center'),
                    dbc.Row([
                        dcc.Dropdown(
                            options=[
                                {'label': 'Ala-aula', 'value': 'Ala aula'},
                                {'label': 'Huone 209', 'value': 'Huone 209'},
                                {'label': 'Ravintolasali', 'value': 'Ravintolasali'},
                                {'label': 'Huone 109', 'value': 'Huone 109'},
                                {'label': 'Huone 307', 'value': 'Huone 307'},
                                {'label': 'Alaravintola', 'value': 'Alaravintola'},
                                {'label': 'Vuolle 1 neuvottelutila', 'value': 'Vuolle 1 neuvottelutila'},
                                {'label': 'Ala-aulan narikka', 'value': 'Ala-aulan narikka'},
                                {'label': '2. kerroksen aulatila', 'value': '2. kerroksen aulatila'},
                                {'label': 'Ylaravintola lavan oikea puoli', 'value': 'Ylaravintola lavan oikea puoli'},
                                {'label': 'Linno 1 ja 2 neuvottelutila', 'value': 'Linno 1 ja 2 neuvottelutila'},
                                {'label': 'Huone 129', 'value': 'Huone 129'},
                                {'label': 'Huone 126', 'value': 'Huone 126'},
                                {'label': 'Huone 229', 'value': 'Huone 229'},
                                {'label': 'Huone 226', 'value': 'Huone 226'},
                                {'label': 'Huone 326', 'value': 'Huone 326'},
                                {'label': 'Huone 327', 'value': 'Huone 327'},
                            ],
                            value="Ala aula",
                            id="room-items",
                            className="roomOptions"
                        )
                    ]),
                    dbc.Row([
                        dbc.RadioItems(
                            options=[
                                {'label': 'Lämpötila', 'value': 'Temperature'},
                                {'label': 'Kosteus', 'value': 'Humidity'},
                                {'label': 'Co2', 'value': 'CO2'},
                            ],
                            value="Temperature",
                            id="option-items",
                            className=""
                        )
                    ]),
                ],className='optionsBar'),

                dbc.Col(
                    dcc.Graph(
                        id='temp-graph',
                        config={
                            'scrollZoom': True,
                            'doubleClick': 'reset',
                            'watermark': False,
                            'displayModeBar': 'hover'},
                    ), md=10),
            ], className='graph'
        ),
    ], className='container-fluid',
)

@app.callback(
    Output('room-title', 'children'),
    [Input('room-items', 'value')]
)
def update_title(selected_room):
    return str(selected_room)

# Modify the existing callback to include room_title
@app.callback(
    Output('temp-graph', 'figure'),
    [
        Input('room-items', 'value'),
        Input('option-items', 'value'),
        Input('data', 'value'),
    ]
)
def update_graph(room, option, data):
    # Determine which file to load based on the selected data value
    if data == '24_hours':
        file_path = 'HistoryUI/HistoricData24Hours.json'
    elif data == '1_year':
        file_path = 'HistoryUI/HistoricData1year.json'
    elif data == '6_month':
        file_path = 'HistoryUI/HistoricData6Months.json'
    elif data == '1_month':
        file_path = 'HistoryUI/HistoricData1Month.json'
    elif data == '1_week':
        file_path = 'HistoryUI/HistoricData1Week.json'
    else:
        # Default to 24-hours data if none of the options are selected
        file_path = 'HistoryUI/HistoricData24Hours.json'

    with open(file_path, 'r') as json_file:
        room_data = json.load(json_file)

    timestamps = [item['Timestamp'] for item in room_data[room]]
    data = [item[option] for item in room_data[room]]

    if option == 'Temperature':
        layout = go.Layout(
            title='',
            xaxis={'title': '', 'gridcolor': 'gray'},
            yaxis={'title': 'Lämpötila(°C)', 'gridcolor': 'gray'},
            plot_bgcolor='whitesmoke',
            paper_bgcolor='whitesmoke',
            font={'color': 'black'},
        )

    elif option == 'Humidity':
        layout = go.Layout(
            title='',
            xaxis={'title': '', 'gridcolor': 'gray'},
            yaxis={'title': 'Kosteus(%)', 'gridcolor': 'gray'},
            plot_bgcolor='whitesmoke',
            paper_bgcolor='whitesmoke',
            font={'color': 'black'},
        )
    else:
        layout = go.Layout(
            title='',
            xaxis={'title': '', 'gridcolor': 'gray'},
            yaxis={'title': 'Co2 (ppm)', 'gridcolor': 'gray'},
            plot_bgcolor='whitesmoke',
            paper_bgcolor='whitesmoke',
            font={'color': 'black'},
        )

    chart = go.Scatter(x=timestamps, y=data, mode='lines+markers', marker={'color': 'blue'}, name=room),

    return {
        'data': chart,
        'layout': layout
    }

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)