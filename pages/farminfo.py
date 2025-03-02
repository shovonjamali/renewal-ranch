import base64
import io

from dash import dcc, html, dash_table
import pandas as pd

def parse_contents(contents, filename, date):
    '''This function accepts page contents and returns data table as html div'''
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    # Read the data file contents
    try:       
        if 'xls' in filename:
            # Assume that the user uploaded an excel file
            input_feed = pd.read_excel(io.BytesIO(decoded),'feed')
            input_manure = pd.read_excel(io.BytesIO(decoded),'manure')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    # Return the data file as data table to display in home page
    return html.Div([
        html.H5(filename),
        dash_table.DataTable(
            data=input_feed.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in input_feed.columns],
            page_size=15,
            persistence=True,
            persistence_type = 'memory'
        ),
        dcc.Store(id='feed-data', data=input_feed.to_dict('records')),
        dcc.Store(id='manure-data', data=input_manure.to_dict('records')),

        html.Hr(),  # horizontal line

        # For debugging (can be removed), display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


