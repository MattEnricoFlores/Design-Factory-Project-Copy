import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import json

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the fullscreen modal
modal_plt_1 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.Row(html.Button("Close", id="close-button-plt-1"))),
        dbc.ModalBody(
            dbc.CardGroup([
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(
                            id="indicator-graphic-1",
                            config={'scrollZoom': True},
                            style={"width": "100%", "height": "100%"}
                        )
                    ]),
                    style={"max-width": "90vw", "max-height": "90vh", "margin": "auto"}
                )
            ])
        ),
    ],
    id="modal-plt-1",
    is_open=False,
    style={"width": "100%", "height": "100%", "margin": 0, "padding": 0, "position": "absolute", "top": "0", "left": "0"}
)

app.layout = dbc.Container(
    [
        html.H1('Absoplotly'),

        dbc.Row(
            [
                dbc.Col(dbc.Button("Viikko", color="secondary", className="me-1", value="1_week", id="week-data",
                                  n_clicks=0), md=4),
                dbc.Col(dbc.Button("Kuukausi", color="secondary", className="me-1", value="1_month",
                                  id="1_month-data", n_clicks=0), md=4),
                dbc.Col(dbc.Button("6 Kuukautta", color="secondary", className="me-1", value="6_month",
                                  id="6_month-data", n_clicks=0), md=4),
            ], className="py-5 text-center"),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='room-dropdown',
                        options=[
                            {'label': 'Ala-aula', 'value': 'Lower lobby'},
                            {'label': 'Huone 209', 'value': 'Room 209'},
                            {'label': 'Ravintolasali', 'value': 'Restaurant hall'},
                            {'label': 'Huone 109', 'value': 'Room 109'},
                            {'label': 'Huone 307', 'value': 'Room 307'},
                            {'label': 'Alaravintola', 'value': 'Lower restaurant'},
                            {'label': 'Vuolle 1 neuvottelutila', 'value': 'Vuolle 1'},
                            {'label': 'Ala-aulan narikka', 'value': 'Lower lobby cloakroom'},
                            {'label': '2. kerroksen aulatila', 'value': '2nd level lobby'},
                            {'label': 'Ylaravintola lavan oikea puoli', 'value': 'Upper restaurant right side of stage'},
                            {'label': 'Linno 1 ja 2 neuvottelutila', 'value': '2nd floor Linno 1 and 2'},
                            {'label': 'Huone 129', 'value': 'Room 129'},
                            {'label': 'Huone 126', 'value': 'Room 126'},
                            {'label': 'Huone 229', 'value': 'Room 229'},
                            {'label': 'Huone 226', 'value': 'Room 226'},
                            {'label': 'Huone 326', 'value': 'Room 326'},
                            {'label': 'Huone 327', 'value': 'Room 327'},
                        ],
                        value='Lower lobby',
                        style={'width': '100%'}
                    ),
                    md=2),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.RadioItems(
                        options=[
                            {'label': 'Lämpötila', 'value': 'Temperature'},
                            {'label': 'Kosteus', 'value': 'Humidity'},
                            {'label': 'Co2', 'value': 'CO2'},
                        ],
                        value="Temperature",
                        id="option-items",
                        className=""
                    ), md=2),

                dbc.Col(
                    dcc.Graph(
                        id='temp-graph-container',
                        config={
                            'scrollZoom': True,
                            'doubleClick':'reset',
                            'watermark':False,
                            'displayModeBar':'hover'}, 
                        style={'margin': 'auto'}
                    ),
                    md=8
                ),
            ]
        ),
        # Fullscreen button
        html.Button("Fullscreen", id="fullscreen-btn", n_clicks=0),

        # Include the fullscreen modal
        modal_plt_1
    ]
)

# Add a global variable to store the state of the fullscreen modal
fullscreen_modal_open = False

@app.callback(
    [
        Output('temp-graph-container', 'figure'),
        Output("indicator-graphic-1", "figure"),
        Output("modal-plt-1", "is_open"),
        Output('week-data', 'n_clicks'),
        Output('1_month-data', 'n_clicks'),
        Output('6_month-data', 'n_clicks'),
        Output('fullscreen-btn', 'n_clicks')
    ],
    [
        Input('room-dropdown', 'value'),
        Input('option-items', 'value'),
        Input('week-data', 'n_clicks'),
        Input('1_month-data', 'n_clicks'),
        Input('6_month-data', 'n_clicks'),
        Input("close-button-plt-1", "n_clicks"),
        Input('fullscreen-btn', 'n_clicks')
    ],
    [
        State('week-data', 'n_clicks'),
        State('1_month-data', 'n_clicks'),
        State('6_month-data', 'n_clicks'),
        State('fullscreen-btn', 'n_clicks')
    ]
)
def update_graph(room, option, week_data, month_data, half_year, close_modal_clicks, fullscreen_clicks,
                 week_data_state, month_data_state, half_year_state, fullscreen_clicks_state):
    global fullscreen_modal_open  # Declare the variable as global

    # Determine which file to load based on the button clicks
    if week_data or week_data_state:
        file_path = 'HistoricData1Week.json'
    elif month_data or month_data_state:
        file_path = 'HistoryData.json'
    elif half_year or half_year_state:
        file_path = 'HistoricData6Months.json'
    else:
        # Default to 1-week data if none of the buttons are clicked
        file_path = 'HistoricData1Week.json'

    with open(file_path, 'r') as json_file:
        room_data = json.load(json_file)

    timestamps = [item['Timestamp'] for item in room_data[room]]
    data = [item[option] for item in room_data[room]]

    # Create layout based on the selected option
    if option == 'Temperature':
        layout = go.Layout(
            title='',
            xaxis={'title': '', 'gridcolor': 'gray'},
            yaxis={'title': 'Lämpötila(°C)', 'gridcolor': 'gray'},
            plot_bgcolor='#161D2F',
            paper_bgcolor='#161D2F',
            font={'color': 'white'},
        )

    elif option == 'Humidity':
        layout = go.Layout(
            title='',
            xaxis={'title': '', 'gridcolor': 'gray'},
            yaxis={'title': 'Kosteus(%)', 'gridcolor': 'gray'},
            plot_bgcolor='#161D2F',
            paper_bgcolor='#161D2F',
            font={'color': 'white'},
        )
    else:
        layout = go.Layout(
            title='',
            xaxis={'title': '', 'gridcolor': 'gray'},
            yaxis={'title': 'Co2 (ppm)', 'gridcolor': 'gray'},
            plot_bgcolor='#161D2F',
            paper_bgcolor='#161D2F',
            font={'color': 'white'},
        )

    chart = {
        'data': [go.Scatter(x=timestamps, y=data, mode='lines+markers', marker={'color': '#51A3A3'}, name=room)],
        'layout': layout
    }

    # Additional logic to determine whether to open or close the fullscreen modal
    if fullscreen_clicks is not None and fullscreen_clicks % 2 == 1:
        fullscreen_modal_open = not fullscreen_modal_open

    if close_modal_clicks is not None and close_modal_clicks > 0:
        fullscreen_modal_open = False

    # Reset the n_clicks properties
    week_data = 0
    month_data = 0
    half_year = 0

    return chart, chart, fullscreen_modal_open, week_data, month_data, half_year, 0

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
