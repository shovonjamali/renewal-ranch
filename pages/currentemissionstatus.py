import base64
import datetime
import io

from dash.dependencies import Input, Output
from dash import dcc, html, callback, dash_table, State
import plotly.express as px
import pandas as pd
import numpy as np
from pages import calculate_emission as ce


#The style arguments for the currentemissionstatus page contents
layout = html.Div([
    
    html.Div(id="current-emission", children=[]),
    html.Button("Download Image", id="btn_image", style={
        "display": "inline-block",
        "padding": "7px 10px",
        "border": "none",
        "background": "#8BC34A",
        "borderRadius": "5px",
        "color": "white"
        
    }),
    dcc.Download(id="download-image")
])


def calculate(feed_data,manure_data,feed_constants,animal_constants,other_constants):
    '''Accepts the farm information and constants as input and 
    return the total emission and cost'''
    if feed_data is None:
        return html.H2("Please upload the feed data in home page!")
    input_f = pd.DataFrame(feed_data)
    if manure_data is None:
        return html.H2("Please upload the manure related data in home page!")
    input_m = pd.DataFrame(manure_data)
    if feed_constants is None:
        return html.H2("Please upload the feed constants in home page!")
    constant_f = pd.DataFrame(feed_constants)
    if animal_constants is None:
        return html.H2("Please upload the constants related to animals in home page!")
    constant_a = pd.DataFrame(animal_constants)
    if other_constants is None:
        return html.H2("Please upload the constants related to animals in home page!")
    constant_o = pd.DataFrame(other_constants)
    
    return ce.emission_calc(input_f, input_m, constant_f, constant_a, constant_o)



@callback(
        Output("current-emission", "children"),
        Output("emission-cal", "data"),
        Output("cost-cal", "data"),
        Input("input-feed", "data"),
        Input("input-manure", "data"),   
        Input("feed-constants", "data"),  
        Input("animal-constants", "data"),                             
        Input("other-constants", "data"),                                                        
          )
def populate_checklist(feed_data,manure_data,feed_constants,animal_constants,other_constants):
    emission_cal, cost_cal = calculate(feed_data,manure_data,feed_constants,animal_constants,other_constants)
    
    ########## Preparing Calculated Emission For Visualizing ###########
    current_emission = (emission_cal.iloc[:,1:].sum(skipna = True)).to_frame()
    index_list = ['CH4-Enteric (t/An)', 'NH3', 'NO2', 'N2O', 'CH4-Manure' ]
    farm_emissions = current_emission.loc[index_list].reset_index(level=0)
    farm_emissions.columns = ['Emitted Gas','Quantity (t/An)' ]
    df = pd.DataFrame({'Emitted Gas':['Total Emission'], 'Quantity (t/An)':[farm_emissions['Quantity (t/An)'].sum()] })
    farm_emissions_pie = farm_emissions
    farm_emissions = pd.concat([farm_emissions, df])
    farm_emissions['Quantity (t/An)'] = farm_emissions['Quantity (t/An)'].astype(float).round(2)
    layout = html.Div([
    dash_table.DataTable(
          data=farm_emissions.to_dict('records'),
        ),
    dcc.Graph(
        id='pie',
        figure = px.pie(farm_emissions_pie, values= 'Quantity (t/An)', names='Emitted Gas', hole=.3),
    
    )
])
    ########## Returns the layout and values to dcc store ###########
    return  layout, emission_cal.to_dict('records'), cost_cal.to_dict('records')


@callback(
    Output("download-image", "data"),
    Input("btn_image", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "dash-community-components.png"
    )
