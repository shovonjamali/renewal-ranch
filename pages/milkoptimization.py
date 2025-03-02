from dash import dcc, html, Input, Output, callback, dash_table, State
import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc

from pages import calculate_emission as ce
from pages import optimization as op

from pages import calculate_emission as ce
from pages import optimization as op

total_lactating_cows = 20
total_pregnant_cows = 13
total_young_cows = 7


# variables for concentrate
con_cost = 0.5

lactating_cow_con = 6
pregnant_cow_con = 4
young_cow_con = 2

lactating_cow_con_per_year = lactating_cow_con * 365
pregnant_cow_con_per_year = pregnant_cow_con * 365
young_cow_con_per_year = young_cow_con * 365

lactating_cow_con_per_year_cost = lactating_cow_con_per_year * con_cost
pregnant_cow_con_per_year_cost = pregnant_cow_con_per_year * con_cost
young_cow_con_per_year_cost = young_cow_con_per_year * con_cost

lactating_cow_con_per_year_cost_total = lactating_cow_con_per_year_cost * total_lactating_cows
pregnant_cow_con_per_year_cost_total = pregnant_cow_con_per_year_cost * total_pregnant_cows
young_cow_con_per_year_cost_total = young_cow_con_per_year_cost * total_young_cows


# variables for hay
hay_cost = 0.1

lactating_cow_hay = 20
pregnant_cow_hay = 20
young_cow_hay = 15

lactating_cow_hay_per_year = lactating_cow_hay * 365
pregnant_cow_hay_per_year = pregnant_cow_hay * 365
young_cow_hay_per_year = young_cow_hay * 365

lactating_cow_hay_per_year_cost = lactating_cow_hay_per_year * hay_cost
pregnant_cow_hay_per_year_cost = pregnant_cow_hay_per_year * hay_cost
young_cow_hay_per_year_cost = young_cow_hay_per_year * hay_cost

lactating_cow_hay_per_year_cost_total = lactating_cow_hay_per_year_cost * total_lactating_cows
pregnant_cow_hay_per_year_cost_total = pregnant_cow_hay_per_year_cost * total_pregnant_cows
young_cow_hay_per_year_cost_total = young_cow_hay_per_year_cost * total_young_cows

# variable for milk
milk_per_day = 18
milk_per_day_all = milk_per_day * total_lactating_cows
milk_per_year_all = milk_per_day_all * 365

# resuable css for button
btn_style = {
                "marginLeft": "5%",
                "width": "10%",
                "display": "inline-block",
                "padding": "5px 0px",
                "border": "none",
                "background": "#8BC34A",
                "borderRadius": "5px",
                "color": "white"
            }

# Create input field and button
input_field = dcc.Input(id='con-cost-input', type='number', value=0.5, style={'marginRight':'10px', 'marginLeft': '5px'}, debounce=True)
button = html.Button('Re-calculate', id='recalculate-button', style=btn_style)

input_field_hay = dcc.Input(id='hay-cost-input', type='number', value=0.1, style={'marginRight':'10px', 'marginLeft': '5px'}, debounce=True)
button_hay = html.Button('Re-calculate', id='recalculate-hay', style=btn_style)

#The style arguments for the currentemissionstatus page contents
layout = html.Div([
    html.H4("Food Formula and Cost for Concentrate"),
    html.P(),
    dbc.Row([
        dbc.Col([
            html.Label('Concentrate Cost:'),
            input_field,
            button
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.P(),
            dash_table.DataTable(
                id='computed-table',
                columns=[
                    {"name": "Cow", "id": "cow", "editable": False},
                    {"name": "Total Cows", "id": "total-cows"},
                    {'name': 'Weight(kg)/Day', 'id': 'weight'},
                    {'name': 'Weight(kg)/Year', 'id': 'weight-per-year', "editable": False},
                    {'name': 'Cost/year', 'id': 'cost-per-year', "editable": False},
                    {'name': 'Cost Category/year', 'id': 'cost-per-category', "editable": False}
                ],
                data=[
                    {
                        "cow": "Lactating Cows", 
                        "total-cows": total_lactating_cows, 
                        "weight": lactating_cow_con, 
                        "weight-per-year": lactating_cow_con_per_year, 
                        "cost-per-year": lactating_cow_con_per_year_cost,
                        "cost-per-category": lactating_cow_con_per_year_cost_total
                    },
                    {
                        "cow": "Pregnant Cows", 
                        "total-cows": total_pregnant_cows, 
                        "weight": pregnant_cow_con, 
                        "weight-per-year": pregnant_cow_con_per_year, 
                        "cost-per-year": pregnant_cow_con_per_year_cost,
                        "cost-per-category": pregnant_cow_con_per_year_cost_total
                    },
                    {
                        "cow": "Young (3-6 months) Cows", 
                        "total-cows": total_young_cows, 
                        "weight": young_cow_con, 
                        "weight-per-year": young_cow_con_per_year, 
                        "cost-per-year": young_cow_con_per_year_cost,
                        "cost-per-category": young_cow_con_per_year_cost_total
                    },
                    {
                        "cow": "", 
                        "total-cows": "", 
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
                        'if': {'row_index': 3},
                        'fontWeight': 'bold',
                        'fontSize': '18px'
                    }
                ]
            )
        ])
    ]),
    html.P(),
    html.H4("Food Formula and Cost for Hay"),
    html.P(),
    dbc.Row([
        dbc.Col([
            html.Label('Hay Cost:'),
            input_field_hay,
            button_hay
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.P(),
            dash_table.DataTable(
                id='computed-table-hay',
                columns=[
                    {"name": "Cow", "id": "cow", "editable": False},
                    {"name": "Total Cows", "id": "total-cows"},
                    {'name': 'Weight(kg)/Day', 'id': 'weight'},
                    {'name': 'Weight(kg)/Year', 'id': 'weight-per-year', "editable": False},
                    {'name': 'Cost/year', 'id': 'cost-per-year', "editable": False},
                    {'name': 'Cost Category/year', 'id': 'cost-per-category', "editable": False}
                ],
                data=[
                    {
                        "cow": "Lactating Cows", 
                        "total-cows": total_lactating_cows, 
                        "weight": lactating_cow_hay, 
                        "weight-per-year": lactating_cow_hay_per_year, 
                        "cost-per-year": lactating_cow_hay_per_year_cost,
                        "cost-per-category": lactating_cow_hay_per_year_cost_total
                    },
                    {
                        "cow": "Pregnant Cows", 
                        "total-cows": total_pregnant_cows, 
                        "weight": pregnant_cow_hay, 
                        "weight-per-year": pregnant_cow_hay_per_year, 
                        "cost-per-year": pregnant_cow_hay_per_year_cost,
                        "cost-per-category": pregnant_cow_hay_per_year_cost_total
                    },
                    {
                        "cow": "Young (3-6 months) Cows", 
                        "total-cows": total_young_cows, 
                        "weight": young_cow_hay, 
                        "weight-per-year": young_cow_hay_per_year, 
                        "cost-per-year": young_cow_hay_per_year_cost,
                        "cost-per-category": young_cow_hay_per_year_cost_total
                    },
                    {
                        "cow": "", 
                        "total-cows": "", 
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
                        'if': {'row_index': 3},
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
            dash_table.DataTable(
                id='computed-table-milk',
                columns=[
                    {"name": "Total Cows", "id": "total-cows"},
                    {'name': 'One Cow(litters)/Day', 'id': 'one-cow'},
                    {'name': 'All Cows(litters)/Day', 'id': 'all-cow', "editable": False},
                    {'name': 'Total(litters)/year', 'id': 'total-year', "editable": False}
                ],
                data=[
                    {
                        "total-cows": total_lactating_cows, 
                        "one-cow": milk_per_day, 
                        "all-cow": milk_per_day_all, 
                        "total-year": milk_per_year_all
                    }
                ],
                editable=True,
                style_cell={'textAlign': 'center'}
            )
        ])
    ]),
    html.P(),
    html.H5("Note:"),
    html.P(),
    dbc.ListGroup(
        [
            dbc.ListGroupItem("Tie-stall with traditional parlor"),
            dbc.ListGroupItem("Pasteurization in high temperature (82 degrees)"),
            dbc.ListGroupItem("However, the production could go upto 3 times after feeding green grass"),
            dbc.ListGroupItem("Other production from milk: soft cheese, drinkable yogurt, ricotta, kefir")
        ]
    )
])

# callback for concentrate
@callback(
    Output('computed-table', 'data'),
    Input('computed-table', 'data_timestamp'),
    Input('recalculate-button','n_clicks_timestamp'),
    State('computed-table', 'data'),
    State('recalculate-button','n_clicks'),
    State('con-cost-input', 'value')
)
def update_columns(timestamp, timestamp_clicks, rows, n_clicks, con_cost_user):
    sum_values = 0.0
    for i, row in enumerate(rows):
        try:
            if i == 3:
                row['cost-per-category'] = sum_values
            else:
                row['weight-per-year'] = float(row['weight']) * 365
                row['cost-per-year'] = float(row['weight-per-year']) * float(con_cost_user)
                row['cost-per-category'] = float(row['cost-per-year']) * float(row['total-cows'])
                sum_values += float(row['cost-per-category'])
        except:
            row['weight-per-year'] = ''
            row['cost-per-year'] = ''
            row['cost-per-category'] = '' #'NA'
    return rows

# callback for hay
@callback(
    Output('computed-table-hay', 'data'),
    Input('computed-table-hay', 'data_timestamp'),
    Input('recalculate-hay','n_clicks_timestamp'),
    State('computed-table-hay', 'data'),
    State('recalculate-hay','n_clicks'),
    State('hay-cost-input', 'value')
)
def update_hay_columns(timestamp, timestamp_clicks, rows, n_clicks, con_cost_user):
    sum_values = 0.0
    for i, row in enumerate(rows):
        try:
            if i == 3:
                row['cost-per-category'] = sum_values
            else:
                row['weight-per-year'] = float(row['weight']) * 365
                row['cost-per-year'] = float(row['weight-per-year']) * float(con_cost_user)
                row['cost-per-category'] = float(row['cost-per-year']) * float(row['total-cows'])
                sum_values += float(row['cost-per-category'])
        except:
            row['weight-per-year'] = ''
            row['cost-per-year'] = ''
            row['cost-per-category'] = ''
    return rows

# callback for milk production
@callback(
    Output('computed-table-milk', 'data'),
    Input('computed-table-milk', 'data_timestamp'),
    State('computed-table-milk', 'data')
)
def update_milk_columns(timestamp, rows):
    for i, row in enumerate(rows):
        try:
            row['all-cow'] = float(row['one-cow']) * float(row['total-cows'])
            row['total-year'] = float(row['all-cow']) * 365 
        except:
            row['all-cow'] = ''
            row['total-year'] = ''
    return rows