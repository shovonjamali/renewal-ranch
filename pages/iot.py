import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html, Input, Output, callback, dash_table, State



###################### IoT Data Preparation
iot_data = pd.read_csv("grafana1.csv", parse_dates=['Time']) 
iot_data.columns=['Time','Battery','CH4','CO','Humidity','NH3','PM1','PM10','PM2.5','Pressure','Temperature in Celsius'] 
iot_data = iot_data.drop_duplicates(['Time'])
iot_data['Time'] = pd.to_datetime(iot_data['Time'], utc=True)
iot_data=iot_data.sort_values(by='Time')
iot_data['Date'] = iot_data['Time']
iot_data.set_index(['Date'], inplace=True)
dates = list(iot_data.sort_values('Time')['Time'])
iot_data_mean = iot_data.resample('H').mean()


#The style arguments for the iot page contents
layout = dbc.Spinner(children=[
    html.Div([
        dcc.DatePickerRange( # To select data range
            id='date-picker-range',  
            calendar_orientation='horizontal',  
            day_size=39,  
            start_date_placeholder_text="Start Date",
            end_date_placeholder_text="End Date",  
            with_portal=False,  
            first_day_of_week=0,  
            reopen_calendar_on_clear=True,
            is_RTL=False,  
            clearable=True,  
            number_of_months_shown=1,  
            min_date_allowed=iot_data['Time'].min(),  
            max_date_allowed=iot_data['Time'].max(),  
            initial_visible_month=dates[len(dates)//2],  
            start_date=iot_data['Time'].min(),
            end_date=iot_data['Time'].max(),
            display_format='MMM Do, YY', 
            month_format='MMMM, YYYY',  
            minimum_nights=1, 

            persistence=True,
            persisted_props=['start_date', 'end_date'],
            persistence_type='session',  

            updatemode='singledate'  
        ),
        ##################### Draw line chart for the time series
        html.Div(id='time-series', children=[
            # dbc.Row([            
            #     dbc.Col([
            #         dcc.Graph(id='battery',
            #         figure = px.line(iot_data, x=iot_data.index, y='Battery'),
            #         style={'display': 'inline-block'})
            #     ]), 
            # ]),
            dbc.Row([
                # dbc.Col([
                #     dcc.Graph(id='temperature',
                #     figure = px.line(iot_data, x=iot_data.index, y='Temperature in Celsius'),
                #     style={'display': 'inline-block'})
                # ]), 

                dbc.Col([
                    dcc.Graph(id='pressure',
                    figure = px.line(iot_data, x=iot_data.index, y='Pressure'),
                    style={'display': 'inline-block'}),
                ]),
                dbc.Col([
                    dcc.Graph(id='humidity',
                    figure = px.line(iot_data, x=iot_data.index, y='Humidity'),
                    style={'display': 'inline-block'}),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='pm1',
                    figure = px.line(iot_data, x=iot_data.index, y='PM1'),
                    style={'display': 'inline-block'})
                ]), 

                dbc.Col([
                    dcc.Graph(id='pm2.5',
                    figure = px.line(iot_data, x=iot_data.index, y='PM2.5'),
                    style={'display': 'inline-block'}),
                ]),
                dbc.Col([
                    dcc.Graph(id='pm10',
                    figure = px.line(iot_data, x=iot_data.index, y='PM10'),
                    style={'display': 'inline-block'}),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='ch4',
                    figure = px.line(iot_data, x=iot_data.index, y='CH4'),
                    style={'display': 'inline-block'})
                ]), 

                dbc.Col([
                    dcc.Graph(id='co',
                    figure = px.line(iot_data, x=iot_data.index, y='CO'),
                    style={'display': 'inline-block'}),
                ]),
                dbc.Col([
                    dcc.Graph(id='nh3',
                    figure = px.line(iot_data, x=iot_data.index, y='NH3'),
                    style={'display': 'inline-block'}),
                ])
            ]),
        ])             
    ])
], size="lg", color="primary", type="border", fullscreen=True)

################################### Callback if the date range changes
@callback(
    Output('time-series', 'children'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
)
def time_series(start_date, end_date):
    subset_iot_data = iot_data.loc[start_date:end_date]
    children = [dbc.Row([
            # dbc.Col([
            #     dcc.Graph(id='battery',
            #     figure = px.line(subset_iot_data, x=subset_iot_data.index, y='Battery'),
            #     style={'display': 'inline-block'})
            # ]), 
        ]),
        dbc.Row([
            # dbc.Col([
            #     dcc.Graph(id='temperature',
            #     figure = px.line(subset_iot_data, x=subset_iot_data.index, y='Temperature in Celsius'),
            #     style={'display': 'inline-block'})
            # ]), 

            dbc.Col([
                dcc.Graph(id='pressure',
                figure = px.line(subset_iot_data, x=subset_iot_data.index, y='Pressure'),
                style={'display': 'inline-block'}),
            ]),
            dbc.Col([
                dcc.Graph(id='humidity',
                figure = px.line(subset_iot_data, x=subset_iot_data.index, y='Humidity'),
                style={'display': 'inline-block'}),
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='pm1',
                figure = px.line(subset_iot_data, x=subset_iot_data.index, y='PM1'),
                style={'display': 'inline-block'})
            ]), 

            dbc.Col([
                dcc.Graph(id='pm2.5',
                figure = px.line(subset_iot_data, x=subset_iot_data.index, y='PM2.5'),
                style={'display': 'inline-block'}),
            ]),
            dbc.Col([
                dcc.Graph(id='pm10',
                figure = px.line(subset_iot_data, x=subset_iot_data.index, y='PM10'),
                style={'display': 'inline-block'}),
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='ch4',
                figure = px.line(subset_iot_data, x=subset_iot_data.index, y='CH4'),
                style={'display': 'inline-block'})
            ]), 

            dbc.Col([
                dcc.Graph(id='co',
                figure = px.line(subset_iot_data, x=subset_iot_data.index, y='CO'),
                style={'display': 'inline-block'}),
            ]),
            dbc.Col([
                dcc.Graph(id='nh3',
                figure = px.line(subset_iot_data, x=subset_iot_data.index, y='NH3'),
                style={'display': 'inline-block'}),
            ])
        ])
    ]
    return children

