from dash import dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

total_lactating_cows = 20

# variables for lactating cow
cost_barley_straw = 0.1
cost_alfalfa_hay = 0.1
cost_corn_silage = 0.1
cost_roaring_corn = 0.1
cost_howling_barley = 0.1
cost_rapeseed_grit = 0.1
cost_wheat_bran = 0.1

weight_barley_straw = 1
weight_alfalfa_hay = 4
weight_corn_silage = 28
weight_roaring_corn = 4
weight_howling_barley = 4
weight_rapeseed_grit = 2
weight_wheat_bran = 0.3

# variables for milk
milk_per_day = 18
price_per_litter = 5
do_reset = False
milk_per_day_all = milk_per_day * total_lactating_cows
milk_per_year_all = milk_per_day_all * 365
price_per_year = milk_per_year_all * price_per_litter

# resuable css for button
btn_style = {
    "marginLeft": "5%",
    "width": "10%",
    "display": "inline-block",
    "padding": "5px 0px",
    "border": "none",
    "background": "#008CBA",
    "borderRadius": "5px",
    "color": "white"
}

# custom CSS styles for input
input_style = {
    # 'width': '100%',
    'padding': '0.375rem 0.75rem',
    'font-size': '1rem',
    'line-height': '1.5',
    'color': '#495057',
    'background-color': '#fff',
    'background-clip': 'padding-box',
    'border': '1px solid #ced4da',
    'border-radius': '0.25rem',
    'transition': 'border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out',
    'margin-left': '5px'
}

# Create input field and button
input_lactating = dcc.Input(id='total-lactating', type='number', value=20, style=input_style, debounce=True)    #style={'marginRight':'10px', 'marginLeft': '5px'}
button_formula = html.Button('Re-calculate', id='recalculate-formula', style=btn_style, n_clicks=0)

input_milk = dcc.Input(id='day-milk', type='number', value=18, min=1, style=input_style, debounce=True)
button_milk_day = html.Button('Re-calculate', id='recalculate-milk-day', style=btn_style, n_clicks=0)

input_month = dcc.Input(id='summer-month', type='number', value=3, min=2, style=input_style, debounce=True)
button_milk = html.Button('Re-calculate', id='recalculate-milk', style=btn_style, n_clicks=0)

# Initial values for pie chart
cost = 31609
production = 657000

# Create the pie chart
pie_chart = go.Figure(
    data=[go.Pie(labels=["Feeding Cost", "Production"], values=[cost, production])],
    layout=go.Layout(title="Feeding Cost vs Production"),
)

# Initial data for horizontal bar chart
categories = ['Feeding Cost', 'Regular Production', 'Production with Green Grass']
chart_values = [31609, 657000, 972000]

# Create horizontal bar chart
bar_chart = go.Figure(data=go.Bar(x=chart_values, y=categories, orientation='h'))

#The style arguments for the currentemissionstatus page contents
layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Label('Lactating Cows:'),
            input_lactating,
            button_formula
        ])
    ]),
    html.P(),
    html.H4("Food Formula and Cost for Lactating Cows"),
    dbc.Row([
        dbc.Col([
            html.P(),
            dash_table.DataTable(
                id='computed-table-3',
                columns=[
                    {"name": "Fooder", "id": "fooder", "editable": False},
                    {"name": "Cost", "id": "cost"},
                    {'name': 'Weight(kg)/Day/Cow', 'id': 'weight'},
                    {'name': 'Weight(kg)/Year/Cow', 'id': 'weight-per-year', "editable": False},
                    {'name': 'Cost/Year/Cow', 'id': 'cost-per-year', "editable": False},
                    {'name': 'Cost/Year/All Cow', 'id': 'cost-per-category', "editable": False}
                ],
                data=[
                    {
                        "fooder": "Barley straw", 
                        "cost": cost_barley_straw, 
                        "weight": weight_barley_straw, 
                        "weight-per-year": weight_barley_straw * 365, 
                        "cost-per-year": round(weight_barley_straw * 365 * cost_barley_straw, 2),
                        "cost-per-category": round(weight_barley_straw * 365 * cost_barley_straw * total_lactating_cows, 2)
                    },
                    {
                        "fooder": "Alfalfa hay", 
                        "cost": cost_alfalfa_hay, 
                        "weight": weight_alfalfa_hay, 
                        "weight-per-year": weight_alfalfa_hay * 365, 
                        "cost-per-year": round(weight_alfalfa_hay * 365 * cost_alfalfa_hay, 2),
                        "cost-per-category": round(weight_alfalfa_hay * 365 * cost_alfalfa_hay * total_lactating_cows, 2)
                    },
                    {
                        "fooder": "Corn silage", 
                        "cost": cost_corn_silage, 
                        "weight": weight_corn_silage, 
                        "weight-per-year": weight_corn_silage * 365, 
                        "cost-per-year": round(weight_corn_silage * 365 * cost_corn_silage, 2),
                        "cost-per-category": round(weight_corn_silage * 365 * cost_corn_silage * total_lactating_cows, 2)
                    },
                    {
                        "fooder": "Roaring corn", 
                        "cost": cost_roaring_corn, 
                        "weight": weight_roaring_corn, 
                        "weight-per-year": weight_roaring_corn * 365, 
                        "cost-per-year": round(weight_roaring_corn * 365 * cost_roaring_corn, 2),
                        "cost-per-category": round(weight_roaring_corn * 365 * cost_roaring_corn * total_lactating_cows, 2)
                    },
                    {
                        "fooder": "Howling barley", 
                        "cost": cost_howling_barley, 
                        "weight": weight_howling_barley, 
                        "weight-per-year": weight_howling_barley * 365, 
                        "cost-per-year": round(weight_howling_barley * 365 * cost_howling_barley, 2),
                        "cost-per-category": round(weight_howling_barley * 365 * cost_howling_barley * total_lactating_cows, 2)
                    },
                    {
                        "fooder": "Rapeseed grit", 
                        "cost": cost_rapeseed_grit, 
                        "weight": weight_rapeseed_grit, 
                        "weight-per-year": weight_rapeseed_grit * 365, 
                        "cost-per-year": round(weight_rapeseed_grit * 365 * cost_rapeseed_grit, 2),
                        "cost-per-category": round(weight_rapeseed_grit * 365 * cost_rapeseed_grit * total_lactating_cows, 2)
                    },
                    {
                        "fooder": "Wheat bran", 
                        "cost": cost_wheat_bran, 
                        "weight": weight_wheat_bran, 
                        "weight-per-year": weight_wheat_bran * 365, 
                        "cost-per-year": round(weight_wheat_bran * 365 * cost_wheat_bran, 2),
                        "cost-per-category": round(weight_wheat_bran * 365 * cost_wheat_bran * total_lactating_cows, 2)
                    },
                    {
                        "fooder": "", 
                        "cost": "", 
                        "weight": "", 
                        "weight-per-year": "", 
                        "cost-per-year": "",
                        "cost-per-category": ""
                    }
                ],
                editable=True,
                style_cell={'textAlign': 'center'},
                style_data_conditional=[
                    {
                        'if': {'row_index': 7},
                        'fontWeight': 'bold',
                        'fontSize': '18px'
                    }
                ]
            )
        ])
    ]),
    html.P(),
    html.H4("Milk Production"),
    html.P(),
    dbc.Row([
        dbc.Col([
            html.Label('Milk/Day:'),
            input_milk,
            button_milk_day
        ])
    ]),
    html.P(),
    dbc.Row([
        dbc.Col([
            dbc.Switch(
                id="switch-grass",
                label="Green Grass",
                value=False,
                style={'marginTop': '5px'}
            )
        ], width=2),
        dbc.Col([
            html.Div(id='milk-info', style={'display': 'block'}, children=[
                html.Label('Summer months:'),
                input_month,
                button_milk
            ])
        ], width=10)
    ]),
    html.P(),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='computed-table-milk-2',
                columns=[
                    {"name": "Total Cows", "id": "total-cows", "editable": False},
                    {"name": "Price", "id": "price"},
                    {'name': 'One Cow(litters)/Day', 'id': 'one-cow', "editable": False},
                    {'name': 'All Cows(litters)/Day', 'id': 'all-cow', "editable": False},
                    {'name': 'Total(litters)/Year', 'id': 'total-year', "editable": False},
                    {'name': 'Price/Year', 'id': 'price-year', "editable": False}
                ],
                data=[
                    {
                        "total-cows": total_lactating_cows, 
                        "price": price_per_litter,
                        "one-cow": milk_per_day, 
                        "all-cow": milk_per_day_all, 
                        "total-year": milk_per_year_all,
                        "price-year": price_per_year
                    }
                ],
                editable=True,
                style_cell={'textAlign': 'center'}
            )
        ])
    ]),
    html.Div(id='milk-condition', style={'display': 'none'}, children=[
        html.P(),
        # html.Label('* Considering Green Grass = 3 months (Default).')
        html.P(
            [
                html.Span("*", style={"color": "red"}),
                "Considering Green Grass = 3 months (Default).",
            ],
            style={"color": "green", "font-weight": "bold"},
        )
    ]),
    html.P(),
    html.H4("Visualization"),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id="pie-chart", figure=pie_chart, style={'border': '1px solid lightgrey', 'border-radius': '5px', 'padding': '10px'}),
                md=6
            ),
            dbc.Col(
                # html.Div(id='container-bar-chart', style={'display': 'none'}, children=[
                #     dcc.Graph(id="bar-chart", figure={}, style={'border': '1px solid lightgrey', 'border-radius': '5px', 'padding': '10px'}),
                # ]),
                dcc.Graph(
                    id='bar-chart',
                    figure=bar_chart,
                    style={'display': 'none'}  # Initially hide the bar chart
                ),
                md=6
            ),
        ],
        align='center',
        # style={'margin-top': '50px'}
    ),
    html.P(),
    html.H5("Note:"),
    html.P(),
    dbc.ListGroup(
        [
            dbc.ListGroupItem("• Tie-stall with traditional parlor"),
            dbc.ListGroupItem("• Pasteurization in high temperature (82 degrees)"),
            dbc.ListGroupItem("• However, the production could go upto 3 times after feeding green grass"),
            dbc.ListGroupItem("• Other production from milk: soft cheese, drinkable yogurt, ricotta, kefir")
        ]
    )
])

# callback for formula
@callback(
    Output('computed-table-3', 'data'),
    Input('computed-table-3', 'data_timestamp'),
    Input('recalculate-formula','n_clicks_timestamp'),
    State('computed-table-3', 'data'),
    State('recalculate-formula','n_clicks'),
    State('total-lactating', 'value')
)
def update_columns(timestamp, timestamp_clicks, rows, n_clicks, total_lactating):
    sum_values = 0.0
    for i, row in enumerate(rows):
        try:
            if i == 7:
                row['cost-per-category'] = sum_values
            else:
                row['weight-per-year'] = float(row['weight']) * 365
                row['cost-per-year'] = round(float(row['weight-per-year']) * float(row['cost']), 2)
                row['cost-per-category'] = round(float(row['cost-per-year']) * total_lactating, 2)
                sum_values += float(row['cost-per-category'])
        except:
            row['weight-per-year'] = ''
            row['cost-per-year'] = ''
            row['cost-per-category'] = ''
    return rows

# callback for milk production
@callback(
    Output('computed-table-milk-2', 'data'),
    Input('computed-table-milk-2', 'data_timestamp'),
    Input('recalculate-formula','n_clicks_timestamp'),
    Input('recalculate-milk','n_clicks_timestamp'),
    Input('recalculate-milk-day','n_clicks_timestamp'),
    Input('switch-grass', 'value'),
    State('computed-table-milk-2', 'data'),
    State('recalculate-formula','n_clicks'),
    State('recalculate-milk','n_clicks'),
    State('recalculate-milk-day','n_clicks'),
    State('total-lactating', 'value'),
    State('summer-month', 'value'),
    State('day-milk', 'value')
)
def update_milk_columns(timestamp, timestamp_clicks, timestamp_clicks_milk, timestamp_clicks_milk_day, switch_checked, rows, n_clicks, n_clicks_milk, n_clicks_milk_day,total_lactating, summer_month, day_milk):
    for i, row in enumerate(rows):
        try:
            row['total-cows'] = total_lactating
            if switch_checked:
                row['one-cow'] = day_milk * 3
                row['all-cow'] = day_milk * 3 * total_lactating
                row['total-year'] = ((day_milk * 3 * summer_month * 30) + ((12 - summer_month) * 30) * day_milk) * total_lactating
                row['price-year'] = float(row['price']) * row['total-year']
            else:
                row['one-cow'] = day_milk
                row['all-cow'] = day_milk * total_lactating
                row['total-year'] = float(row['all-cow']) * 365 
                row['price-year'] = float(row['price']) * row['total-year']                  
        except:
            row['total-cows'] = ''
            row['all-cow'] = ''
            row['total-year'] = ''

    return rows

# callback for toggle grass
@callback(
    Output('milk-info', 'style'),
    Output('milk-condition', 'style'),
    # Output('container-bar-chart', 'style'),
    Input('switch-grass', 'value')
)
def toggle_milk_info(switch_checked):
    if switch_checked:
        return {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}
    
# callback for updating pie chart
@callback(
    Output("pie-chart", "figure"),
    Input('computed-table-3', 'data'),
    Input('computed-table-milk-2', 'data')
)
def update_pie_chart(rows_formula, rows_milk):
    # Convert table data to a list of dictionaries
    table_rows = [row for row in rows_formula]
    
    # Get values from rows 0 to 6 and sum them
    sum_value = sum(row['cost-per-category'] for row in table_rows[:7])
    milk_cost = sum_value

    milk_production = rows_milk[0]['price-year']

    return go.Figure(
        data=[go.Pie(labels=["Feeding Cost", "Production"], values=[milk_cost, milk_production])],
        layout=go.Layout(title="Feeding Cost/Year vs Production/Year"),
    )

# callback for updating bar chart
@callback(
    [Output('bar-chart', 'style'), Output('bar-chart', 'figure')],
    Input('switch-grass', 'value'),
    Input('computed-table-3', 'data'),
    Input('computed-table-milk-2', 'data'),
    State('total-lactating', 'value'),
    State('day-milk', 'value')
)
def toggle_bar_chart(switch_checked, rows_formula, rows_milk, total_lactating, day_milk):
    # calculate cost from first table
    # Convert table data to a list of dictionaries
    table_rows = [row for row in rows_formula]
    # Get values from rows 0 to 6 and sum them
    sum_value = sum(row['cost-per-category'] for row in table_rows[:7])
    cost = sum_value

    # current green grass production from second table
    green_grass_production = rows_milk[0]['price-year']

    # calculate regular production from green grass production
    total_cows = total_lactating #rows_milk[0]['total-cows']
    price = float(rows_milk[0]['price'])
    one_cow_day = day_milk #float(rows_milk[0]['one-cow']) / 3 # need to be 3 times less than green grass production
    regular_production =  total_cows * price * one_cow_day * 365
    #regular_production = 12345

    if switch_checked:
        updated_colors = ['#EF553B', '#636EFA', '#50C878']  # Update the bar colors
        updated_chart_values = [cost, regular_production, green_grass_production]  # Update the chart values
        updated_bar_chart = go.Figure(data=go.Bar(x=updated_chart_values, y=categories, orientation='h', marker_color=updated_colors))
        updated_bar_chart.update_layout(
            title='Feeding Cost, Production, and Production with Green Grass',
            xaxis=dict(title='Values'),
            yaxis=dict(title='Categories'),
        )
        return {'display': 'block', 'border': '1px solid lightgrey', 'border-radius': '5px', 'padding': '10px'}, updated_bar_chart  # Show the bar chart with updated values
    else:
        return {'display': 'none'}, bar_chart  # Hide the bar chart and reset to initial values