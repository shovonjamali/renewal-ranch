from dash import dcc, html, Input, Output, callback, dash_table, State
import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
import math
import plotly.graph_objs as go

from pages import calculate_emission as ce
from pages import optimization as op

#The style arguments for the currentemissionstatus page contents
layout = html.Div([
    dbc.Row([
        html.B("Adjust the weights(%) here"),
        html.P(),
        dbc.Col([
            html.B("Emission"),
            dcc.Input(id="weight-em", type="number", value=70, min=0, max=100, step=1, style={'marginRight':'10px', 'marginLeft': '5px'},debounce=True),
            html.B("Cost"),
            dcc.Input(id="weight-cost", type="number", value=30, min=0, max=100, step=1, style={'marginRight':'10px', 'marginLeft': '5px'},debounce=True),
            html.B("Milk"),
            dcc.Input(id="weight-new", type="number", value=0, min=0, max=100, step=1, style={'marginRight':'10px', 'marginLeft': '5px',},debounce=True),
            html.Button('Optimize', id='opt-button', n_clicks=0,
                    style={
                        "marginLeft": "5%",
                        "width": "10%",
                        "display": "inline-block",
                        "padding": "5px 0px",
                        "border": "none",
                        "background": "#8BC34A",
                        "borderRadius": "5px",
                        "color": "white"
            })
        ]),
        ]),
    html.P(),
    html.P(),
     html.Div([
        dbc.Row([
        dbc.Col([
        html.B("Optimal Feed Mixture (Update feed information here)"),
        html.Button('Recalculate', id='re-button', n_clicks=0,
                    style={
                        "marginLeft": "10%",
                        "width": "10%",
                        "display": "inline-block",
                        "padding": "5px 0px",
                        "border": "none",
                        "background": "#8BC34A",
                        "borderRadius": "5px",
                        "color": "white"
                    },
        ),
        ]),
        ]),
        html.P(),
        dash_table.DataTable(id = 'feed-edit-table',
            columns=[{"name": i, "id": i} for i in ['Animal Category', 'Animal Numbers', 'Barley Straw', 'Alfalfa Hay',
       'Corn Silage', 'Roaring Corn', 'Howling Barley', 'Rapeseed Grit', 'Wheat Bran']], editable=True
        ),
        html.P(),
        html.P(),
        html.B("Predicted Output Based on Suggested Values"),
        dash_table.DataTable(id = 'recommended-output-table'
         
        ),
        html.Div(id='output-info', style={'display': 'none'}),
        # dcc.Graph(id='pie-chart2'),
        html.Div(children=
            [
                dcc.Graph(id='bar-emission', style={'display': 'inline-block'}),
                dcc.Graph(id='bar-cost',style={'display': 'inline-block'}),
                dcc.Graph(id='pie-chart2')
            ])   
        ])
])

def output_cal(feed,constant_feed,emission_cal,cost_cal):
    '''Accepts input feed, constants, optimized emission and cost
    and returns the adjusted feed, new emission and new cost'''

    #Energy and emission factor calculation according to ipcc
    GE = (feed.iloc[:,2:]*list(constant_feed.loc['GE'])).sum(axis=1)/239
    DE = (feed.iloc[:,2:]*list(constant_feed.loc['DE'])).sum(axis=1)/239
    DE_perc = DE/GE*100
    Ym = -0.0038 *DE_perc*DE_perc + 0.3501 *DE_perc - 0.811
    opt_ef = ((GE* (Ym/100)*365)/55.65)

    ########### Feed, cost and emission output result preperation
    feed_output = pd.DataFrame(columns=['Animal Category'])
    feed_output['Animal Category']=feed['Animal Category']
    feed_output['CH4-Enteric (t/An)'] = feed['Animal Numbers']* opt_ef/1000
    feed_output['CH4-Reduction %'] =  round(((feed_output['CH4-Enteric (t/An)']- emission_cal['CH4-Enteric (t/An)'])/emission_cal['CH4-Enteric (t/An)']*-100),2)
    feed_output['Estimated Cost'] =  (feed.iloc[:,2:]*list(constant_feed.loc['Feed Cost'])).sum(axis=1)
    feed_output['Estimated Net Energy (Kg)'] =  0.84*DE - .77
    feed_output = round(feed_output,2)

    org_cost = cost_cal.copy()
    org_cost.columns = ['Animal Category','Estimated Cost']
    org_cost['Calculated'] = ['Current Cost','Current Cost','Current Cost']
    new_cost = feed_output.loc[:,['Animal Category','Estimated Cost']]
    new_cost['Calculated'] = ['New Cost','New Cost','New Cost']
    cost = org_cost.append(new_cost)


    org_emission = emission_cal.loc[:,['Animal Category','CH4-Enteric (t/An)']].copy()
    org_emission['Calculated'] = ['Current CH4-Enteric','Current CH4-Enteric','Current CH4-Enteric']
    new_emission = feed_output.loc[:,['Animal Category','CH4-Enteric (t/An)']]
    new_emission['Calculated'] = ['New CH4-Enteric','New CH4-Enteric','New CH4-Enteric']
    ch4_enteric = org_emission.append(new_emission)

    return feed_output, ch4_enteric, cost

def opt_calc(weight_em, weight_cost, weight_new, input_feed, input_manure, constant_feed, constant_animal, constant_other, constraints, boundary, emission_cal, cost_cal, lactating_cow_weight, milk_fat):
    opt_feed, opt_feed_output, lact_success = op.optimize(weight_em, weight_cost, weight_new, input_feed, input_manure, constant_feed, constant_animal, constant_other,constraints,boundary, emission_cal, cost_cal, lactating_cow_weight, milk_fat)
    return opt_feed, lact_success

@callback(
    Output('weight-em', 'value'),    
    Output('weight-cost', 'value'),
    Output('weight-new', 'value'),
    Output('re-button', 'n_clicks'),
    Input('weight-em', 'value'),
    Input('weight-cost', 'value'),
    Input('weight-new', 'value'),
    Input('re-button','n_clicks_timestamp'),
    State('re-button','n_clicks'),
    prevent_initial_call=True 
)
def update_inputs(emission, cost, milk, time_st, n_clicks):
    ctx = dash.callback_context
    changed_input = ctx.triggered[0]['prop_id'].split('.')[0]
    var_emiision = 10
    var_cost = 10
    var_milk = 10

    if changed_input == 'weight-em':
        var_emiision = emission
        total = emission + cost + milk
        remaining_value = 100 - total
        
        if remaining_value >= 0:
            if milk != 0:
                var_cost = remaining_value + cost
                var_milk = milk
            else:
                var_milk = remaining_value + milk
                var_cost = cost
        else:
            var_cost = remaining_value + cost
            var_milk = milk
            
        
    elif changed_input == 'weight-cost':
        var_cost = cost
        total = emission + cost + milk
        remaining_value = 100 - total

        if remaining_value >= 0:
            if milk != 0:
                var_emiision = remaining_value + emission
                var_milk = milk
            else:
                var_milk = remaining_value + milk
                var_emiision = emission
        else:
            var_emiision = remaining_value + emission
            var_milk = milk
        
    elif changed_input == 'weight-new':
        var_milk = milk
        total = emission + cost + milk
        remaining_value = 100 - total

        if remaining_value >= 0:
            if emission != 0:
                var_emiision = remaining_value + emission
                var_cost = cost
            else:
                var_cost = remaining_value + cost
                var_emiision = emission
        else:
            var_emiision = remaining_value + emission
            var_cost = cost
    
    if n_clicks:
        var_emiision = 65
        var_cost = 20
        var_milk = 15
          
    return var_emiision, var_cost, var_milk, 0

########################### Callback for interactions

@callback(Output("feed-edit-table", "data"),
          Output("output-info", "children"),
        Input('weight-em', 'value'),
        Input('weight-cost', 'value'),
        Input('weight-new', 'value'),
        Input("input-feed", "data"),
        Input("input-manure", "data"),   
        Input("feed-constants", "data"),  
        Input("animal-constants", "data"),                             
        Input("other-constants", "data"),
        Input("feed-constraints", "data"),   
        Input("boundary-condition", "data"), 
        Input("emission-cal", "data"),
        Input("cost-cal", "data"),
        Input('opt-button','n_clicks_timestamp'),
        State('opt-button','n_clicks'),
        )

def populate_checklist(weight_em, weight_cost, weight_new, feed_data, manure_data, feed_constants, animal_constants,
                    other_constants, feed_constraints, boundary_condition, emission, cost, opt_time, opt_clicks):
    ############# Check the input and convert into dataframes
    if feed_data is None:
        return html.H2("Please upload the feed data in home page!")
    feed_data = pd.DataFrame(feed_data)
    if manure_data is None:
        return html.H2("Please upload the manure related data in home page!")
    manure_data = pd.DataFrame(manure_data)
    if feed_constants is None:
        return html.H2("Please upload the feed constants in home page!")
    feed_constants = pd.DataFrame(feed_constants)
    if animal_constants is None:
        return html.H2("Please upload the constants related to animals in home page!")
    animal_constants = pd.DataFrame(animal_constants)
    if other_constants is None:
        return html.H2("Please upload the constants related to animals in home page!")
    other_constants =  pd.DataFrame(other_constants)
    if feed_constraints is None:
        return html.H2("Please upload the constraints related to feed in home page!")
    constraints = pd.DataFrame(feed_constraints)
    if boundary_condition is None:
        return html.H2("Please upload the boundary conditions in home page!")
    boundary = pd.DataFrame(boundary_condition)
    if emission is None:
        return html.H2("Please calculate current emission status first!")
    emission_cal = pd.DataFrame(emission)
    if cost is None:
        return html.H2("Please calculate current emission status first!")
    cost_cal = pd.DataFrame(cost)    
  
    ################### Prepare the data in correct format
    input_feed, input_manure, constant_feed, constant_animal, constant_other = ce.data_prep(feed_data,manure_data,feed_constants,animal_constants,other_constants) 
    ######################## Calculate the optimized feed combinations according to weights of cost and emission

    # new for milk
    lactating_cows_actual_fooder = feed_data['Lactating Cows'][3:].tolist()
    lactating_cow_weight  = feed_data.iloc[1, 1]
    milk_yield_actual  = feed_data.iloc[2, 1]
    dmi_list = feed_constants['DMI'].tolist()

    total_DMI_actual = sum(value * dmi_value for value, dmi_value in zip(lactating_cows_actual_fooder, dmi_list))
    FCM4_actual = float((total_DMI_actual - (4.048 - (0.00387 * lactating_cow_weight))) / 0.0584)
    milk_fat = float((FCM4_actual - (0.4 * milk_yield_actual)) / 15)
    milk_fat = round(milk_fat, 2)
    #milk_fat = 42.38

    opt_feed, lact_success = opt_calc(weight_em, weight_cost, weight_new, input_feed, input_manure, constant_feed, constant_animal, constant_other, constraints, boundary, emission_cal, cost_cal, lactating_cow_weight, milk_fat)
    
    return opt_feed.to_dict('records'), lact_success


####################### Callback to render output emission and bar graphs 
@callback(Output("recommended-output-table", "data"),
        Output("bar-emission", "figure"),
        Output("bar-cost", "figure"),   
        Output("pie-chart2", "figure"),
        Input("input-feed", "data"),
        Input("feed-constants", "data"),                                 
        Input("emission-cal", "data"),
        Input("cost-cal", "data"),
        Input("feed-edit-table", "data"),
        )

def populate_checklist(feed_data, feed_constants, emission, cost,rows):  
    ################### Check the input from callback and prepare for calculations
    if feed_data is None:
        return html.H2("Please upload the feed data in home page!")
    feed_data = pd.DataFrame(feed_data)

    if feed_constants is None:
        return html.H2("Please upload the feed constants in home page!")
    constant_feed = pd.DataFrame(feed_constants)
    constant_feed =constant_feed.T
    constant_feed.columns = constant_feed.iloc[0,:]
    constant_feed= constant_feed[1:]

    if emission is None:
        return html.H2("Please calculate current emission status first!")
    emission_cal = pd.DataFrame(emission)

    if cost is None:
        return html.H2("Please calculate current emission status first!")
    cost_cal = pd.DataFrame(cost) 

    ##################### Calculate emission output from the new feed combination
    updated_feed = pd.DataFrame(rows)
    cols=[i for i in updated_feed.columns if i not in ["Animal Category"]]
    for col in cols:
        updated_feed[col]=pd.to_numeric(updated_feed[col])
    opt_feed_output, ch4_enteric, cost=output_cal(updated_feed,constant_feed, emission_cal, cost_cal)
    ######################## Prepare the barchart
    ch4_figure = px.bar(ch4_enteric, x='Animal Category', y='CH4-Enteric (t/An)',color='Calculated', barmode="group")
    cost_figure = px.bar(cost, x='Animal Category', y='Estimated Cost', color='Calculated', barmode="group")

    ######################## Prepare the pie chart for milk production
    lactating_cow_weight  = feed_data.iloc[1, 1]
    milk_yield_actual  = feed_data.iloc[2, 1]
    lactating_cows_actual_fooder = feed_data['Lactating Cows'][3:].tolist()

    feed_constants = pd.DataFrame(feed_constants)

    # Extract DMI values and store them in a list
    dmi_list = feed_constants['DMI'].tolist()

    first_row = rows[0]  
    #lactating_cows_recommended_fooder = list(first_row.values())[2:]

    value1 = float(dmi_list[0]) * float(rows[0]["Barley Straw"])
    value2 = float(dmi_list[1]) * float(rows[0]["Alfalfa Hay"])
    value3 = float(dmi_list[2]) * float(rows[0]["Corn Silage"])
    value4 = float(dmi_list[3]) * float(rows[0]["Roaring Corn"])
    value5 = float(dmi_list[4]) * float(rows[0]["Howling Barley"])
    value6 = float(dmi_list[5]) * float(rows[0]["Rapeseed Grit"])
    value7 = float(dmi_list[6]) * float(rows[0]["Wheat Bran"])
    
    total_DMI_recommended = value1 + value2 + value3 + value4 + value5 + value6 + value7

    # total_DMI_recommended = sum(value * dmi_value for value, dmi_value in zip(lactating_cows_recommended_fooder, dmi_list))
    total_DMI_actual = sum(value * dmi_value for value, dmi_value in zip(lactating_cows_actual_fooder, dmi_list))

    FCM4_actual = float((total_DMI_actual - (4.048 - (0.00387 * lactating_cow_weight))) / 0.0584)
    milk_fat = float((FCM4_actual - (0.4 * milk_yield_actual)) / 15)
    milk_fat = round(milk_fat, 2)

    FCM4_recommended = float((total_DMI_recommended - (4.048 - (0.00387 * lactating_cow_weight))) / 0.0584)
    milk_yield_recommended = math.ceil(float((FCM4_recommended - (15 * milk_fat)) / 0.4))
    
    points = ['Current Milk', 'New Milk']
    values = [milk_yield_actual, milk_yield_recommended]

    trace = [
        go.Bar(x=points, y=values, marker=dict(color=['rgb(85, 123, 255)', 'rgb(239, 85, 59)']), showlegend=False),  # Custom legend label
        go.Scatter(x=points, y=[0, 0], mode='lines', line=dict(color='black'), showlegend=False)  # Custom legend label
    ]

    layout = go.Layout(
        title='',
        xaxis=dict(title='Milk Types'),
        yaxis=dict(title='Milk Production'),
    )

    return opt_feed_output.to_dict('records'), ch4_figure, cost_figure, {'data': trace, 'layout': layout}