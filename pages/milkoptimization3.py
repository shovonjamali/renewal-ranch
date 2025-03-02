import dash
from dash import dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import math
import plotly.graph_objs as go
import joblib
import os

# Style for button
button_style = {
    "marginLeft": "2%",
    "marginRight": "1%",
    "width": "15%",
    "display": "inline-block",
    "padding": "5px 0px",
    "border": "none",
    "background": "#008CBA",
    "borderRadius": "5px",
    "color": "white"
}

# Create list for lactating cow's information (for each column)
cow_info = ['Number of cows', 'Average weight']
cow_info_early = [30, 650]
cow_info_mid = [30, 500]
cow_info_late = [30, 700]

# Create the initial data for cow information table
info_data = [{'info': info, 'info-early': info_early, 'info-mid': info_mid, 'info-late': info_late}
                for info, info_early, info_mid, info_late in zip(cow_info, cow_info_early, cow_info_mid, cow_info_late)]

# Create lists for fodders (for each column)
fodders = ['Barley straw', 'Alfalfa hay', 'Corn silage', 'Roaring corn', 'Howling barley', 'Rapeseed grit', 'Wheat bran']
fodder_weight_early = [1, 4, 28, 4, 4, 3, 0.3]
fodder_weight_mid =   [1, 4, 28, 5, 5, 3, 0.3]    #[0, 0, 0, 0, 0, 0, 0]
fodder_weight_late =  [1, 4, 28, 3, 3, 3, 0.3]    #[0, 0, 0, 0, 0, 0, 0]

# Create the initial data for fodder table
fodder_data = [{'fodder': fodder, 'lactation-early': weight_early, 'lactation-mid': weight_mid, 'lactation-late': weight_late}
                for fodder, weight_early, weight_mid, weight_late in zip(fodders, fodder_weight_early, fodder_weight_mid, fodder_weight_late)]

# Coefficients for multiple linear regression model
b1 = 1.0080825063596421e-13
b2 = -3.059739490979892
b3 = -1.687538997430238e-14
b4 = 7.150762650301039
b5 = -2.701771080045919
b6 = -0.026249029984624195
b7 = 0.41181306054371103
b8 = 1.6075500875402453
b9 = 2.565693189949013
b0 = 21.538677147437568
coefficients = [b1, b2, b3, b4, b5, b6, b7, b8, b9]

early_lactation_days = 100 #math.floor((14 + 100) / 2)
mid_lactation_days = 200 #math.floor((100 + 200) / 2)
late_lactation_days = 305 #math.floor((200 + 305) / 2)

# Process button
button_process = html.Button('Re-calculate', id='btn-process', style=button_style, n_clicks=0)
# Copy buttons
button_copy_to_mid = html.Button('Copy Mid Lactation', style=button_style, id='btn-copy-to-mid', n_clicks=0)
button_copy_to_late = html.Button('Copy Late Lactation', style=button_style, id='btn-copy-to-late', n_clicks=0)
# Reset buttons
button_reset_mid = html.Button('Reset Mid Lactation', style=button_style, id='btn-reset-mid', n_clicks=0)
button_reset_late = html.Button('Reset Late Lactation', style=button_style, id='btn-reset-late', n_clicks=0)
                
layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Label('Information of Lactating Cows', style={'font-size': '1.25rem', 'font-weight': 'bold'}),
            button_process,
            html.P(),
            # Dash table to display the information data
            dash_table.DataTable(
                id='tbl-info',
                columns=[
                    {'name': '', 'id': 'info', 'editable': False},
                    {'name': 'Early Lactation', 'id': 'info-early', 'editable': True},
                    {'name': 'Mid Lactation', 'id': 'info-mid', 'editable': True},
                    {'name': 'Late Lactation', 'id': 'info-late', 'editable': True}
                ],
                data=info_data,
                style_cell={'textAlign': 'center'},
            ),
        ])
    ]),
    html.P(),
    dbc.Row([
        dbc.Col([
            html.Label('Food Formula (kg) of Lactating Cows', style={'font-size': '1.25rem', 'font-weight': 'bold'}),
            button_reset_mid,
            button_reset_late,
            html.P(),
            # Dash table to display the fodder data
            dash_table.DataTable(
                id='tbl-fodder',
                columns=[
                    {'name': 'Fodder', 'id': 'fodder', 'editable': False},
                    {'name': 'Early Lactation', 'id': 'lactation-early', 'editable': True},
                    {'name': 'Mid Lactation', 'id': 'lactation-mid', 'editable': True},
                    {'name': 'Late Lactation', 'id': 'lactation-late', 'editable': True}
                ],
                data=fodder_data,
                style_cell={'textAlign': 'center'},
            ),
        ])
    ]),
    dbc.Row([
        # dbc.Col([
        #     html.Div(id='output')
        # ], width=3),
        dbc.Col([
            dcc.Graph(id='milk-chart', style={'display': 'blick'})
        ], width=12),
    ]),
])

def generate_bar_chart(early_lactation_total_food_weight, early_quantity,
                    mid_lactation_total_food_weight, mid_quantity,
                    late_lactation_total_food_weight, late_quantity,
                    early_cows, mid_cows, late_cows):
    
    categories = ['Early Lactation', 'Mid Lactation', 'Late Lactation']
    
    value_set1 = [round(early_lactation_total_food_weight * early_cows, 2), round(mid_lactation_total_food_weight * mid_cows, 2), round(late_lactation_total_food_weight * late_cows, 2)]
    value_set2 = [round(early_quantity * early_cows, 2), round(mid_quantity * mid_cows, 2), round(late_quantity * late_cows, 2)]
    
    # Create the grouped bar chart figure
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=value_set1,
        name='Fodder (kg)',
        marker_color='rgb(85, 123, 255)',
        text=value_set1,
        textposition='inside'
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=value_set2,
        name='Milk (litters)',
        marker_color='rgb(239, 85, 59)', #'rgb(85, 65, 54)',
        text=value_set2,
        textposition='inside'
    ))

    # Customize the layout
    fig.update_layout(
        title='',
        xaxis_title='Categories',
        yaxis_title='Values',
        barmode='group'
    )

    return fig

@callback(
    #Output('output', 'children'),
    Output('milk-chart', 'style'),
    Output('milk-chart', 'figure'),
    Input('btn-process', 'n_clicks'),
    State('tbl-info', 'data'),
    State('tbl-fodder', 'data'),
    #prevent_initial_call=True
)
def process_table_data(n_clicks, table_data_info, table_data_fodder):
    early_lactation_infos = []
    mid_lactation_infos = []
    late_lactation_infos = []

    early_lactation_values = []    
    mid_lactation_values = []
    late_lactation_values = []

    early_quantity = 0
    mid_quantity = 0
    late_quantity = 0
    
    #if n_clicks > 0:
    for row in table_data_info:
        early_lactation_infos.append(float(row['info-early']))
        mid_lactation_infos.append(float(row['info-mid']))
        late_lactation_infos.append(float(row['info-late']))

    early_cows = early_lactation_infos[0]
    early_avg_weight = early_lactation_infos[1]

    mid_cows = mid_lactation_infos[0]
    mid_avg_weight = mid_lactation_infos[1]

    late_cows = late_lactation_infos[0]
    late_avg_weight = late_lactation_infos[1]

    for row in table_data_fodder:
        early_lactation_values.append(float(row['lactation-early']))
        mid_lactation_values.append(float(row['lactation-mid']))
        late_lactation_values.append(float(row['lactation-late']))

    early_lactation_total_food_weight = sum(early_lactation_values)
    early_lactation_values.append(early_lactation_days) 
    early_lactation_values.append(float(early_avg_weight))

    mid_lactation_total_food_weight = sum(mid_lactation_values)
    mid_lactation_values.append(mid_lactation_days) 
    mid_lactation_values.append(float(mid_avg_weight))

    late_lactation_total_food_weight = sum(late_lactation_values)
    late_lactation_values.append(late_lactation_days) 
    late_lactation_values.append(float(late_avg_weight))

    # Get the absolute path of the current script
    current_path = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the scaler file
    scaler_file_path = os.path.join(current_path, 'scaler_milk.joblib')
    # Load the fitted scaler
    scaler = joblib.load(scaler_file_path)

    # Calculate the predicted value (y) for early lactation using the coefficients and the given data
    if(early_lactation_total_food_weight != 0 and early_avg_weight != 0):
        early_lactation_normalized = scaler.transform([early_lactation_values])
        predicted_y_early = b0 + sum(coef * val for coef, val in zip(coefficients, early_lactation_normalized[0]))
        early_quantity = math.ceil(predicted_y_early)

    # Calculate the predicted value (y) for mid lactation using the coefficients and the given data
    if(mid_lactation_total_food_weight != 0 and mid_avg_weight != 0):
        mid_lactation_normalized = scaler.transform([mid_lactation_values])
        predicted_y_mid = b0 + sum(coef * val for coef, val in zip(coefficients, mid_lactation_normalized[0]))
        mid_quantity = math.ceil(predicted_y_mid)

    # Calculate the predicted value (y) for late lactation using the coefficients and the given data
    if(late_lactation_total_food_weight != 0 and late_avg_weight != 0):
        late_lactation_normalized = scaler.transform([late_lactation_values])
        predicted_y_late = b0 + sum(coef * val for coef, val in zip(coefficients, late_lactation_normalized[0]))
        late_quantity = math.ceil(predicted_y_late)

    fig = generate_bar_chart(early_lactation_total_food_weight, early_quantity, mid_lactation_total_food_weight, mid_quantity, late_lactation_total_food_weight, late_quantity, early_cows, mid_cows, late_cows)

    return {'display': 'block'}, fig

    # If the button is not clicked yet, return an empty Div
    #return html.Div(), {'display': 'none'}, go.Figure()

@callback(
    Output('tbl-fodder', 'data'),
    Output('tbl-info', 'data'),
    # Input('btn-copy-to-mid', 'n_clicks'),
    # Input('btn-copy-to-late', 'n_clicks'),
    Input('btn-reset-mid', 'n_clicks'),
    Input('btn-reset-late', 'n_clicks'),
    State('tbl-fodder', 'data'),
    State('tbl-info', 'data'),
    prevent_initial_call=True
)
#def copy_to_columns(clicks_to_mid, clicks_to_late, clicks_to_mid_reset, clicks_to_late_reset, fodder_table_data):
def copy_to_columns(clicks_to_mid_reset, clicks_to_late_reset, fodder_table_data, info_table_data):    
    # To check which button was clicked
    ctx = dash.callback_context
    prop_id = ctx.triggered[0]['prop_id']
    
    if 'btn-copy-to-mid' in prop_id:
        for row in fodder_table_data:
            row['lactation-mid'] = row['lactation-early']
    elif 'btn-copy-to-late' in prop_id:
        for row in fodder_table_data:
            row['lactation-late'] = row['lactation-early']
    elif 'btn-reset-mid' in prop_id:
        for row in fodder_table_data:
            row['lactation-mid'] = 0
        for row in info_table_data:
            row['info-mid'] = 0
    elif 'btn-reset-late' in prop_id:
        for row in fodder_table_data:
            row['lactation-late'] = 0
        for row in info_table_data:
            row['info-late'] = 0

    return fodder_table_data, info_table_data

