from operator import index
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, dash_table, State
import pandas as pd
from pages import farminfo

import base64
import io

# The style arguments for the home page contents
btnRegularStyle = {
    'width': '100%',
    'lineHeight': '60px',
    'textAlign': 'center',
    'cursor': 'pointer',
    'display': 'block',
    'height': '60px',
    'lineHeight': '60px',
    'background': '#8BC34A',
    'borderRadius': '5px',
    'color': 'white',
    'fontWeight': 'bold',
    'margin': '10px'
}

btnUploadedStyle = {
    'width': '100%',
    'lineHeight': '60px',
    'textAlign': 'center',
    'cursor': 'pointer',
    'display': 'block',
    'height': '60px',
    'lineHeight': '60px',
    'background': '#5cb85c',
    'borderRadius': '5px',
    'color': 'white',
    'fontWeight': 'bold',
    'margin': '10px'
}

toastStyle = {
    "position": "fixed",
    "top": 66,
    "right": 10,
    "width": 350,
    "zIndex": 9,
    "background-color": "#056608",
    "color": "white"
}

toastStyleError = {
    "position": "fixed",
    "top": 66,
    "right": 10,
    "width": 350,
    "zIndex": 9,
    "background-color": "#dc3545",
    "color": "white"
}

layout = html.Div([
    html.Div(
        html.P("A data-driven dashboard for estimating and optimizing greenhouse gas emissions from livestock farms. It enables emissions monitoring, feed scenario analysis, milk optimization, and sustainable farm management through interactive visualizations and optimization techniques."),
    style={
        "background-color": "#3E2723 ",
        "color": "white",
        "text-align": "justify",
        'margin': '10px',
        'width': '100%',
        'padding': '20px',
        'margin-bottom': '50px'
    }),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Upload your input data file ',
            html.A('by dragging or selecting')
        ]),
        style=btnRegularStyle,
        # Allow multiple files upload
        multiple=True
    ),
    dbc.Toast(
        "",
        id="upload-toast",
        header="",
        is_open=False,
        dismissable=True,
        duration=3000,
        style=toastStyle,
    ),
    dcc.Upload(
        id='upload-constants',
        children=html.Div([
            'Upload your feed constants data file ',
            html.A('by dragging or selecting')
        ]),
        style=btnRegularStyle,
        # Allow multiple files upload
        multiple=True
    ),
    dbc.Toast(
        "",
        id="upload-toast-2",
        header="",
        is_open=False,
        dismissable=True,
        duration=3000,
        style=toastStyle,
    ),
    dcc.Upload(
        id='upload-constraints',
        children=html.Div([
            'Upload your constraint data file ',
            html.A('by dragging or selecting')
        ]),
        style=btnRegularStyle,
        # Allow multiple files upload
        multiple=True
    ),
    dbc.Toast(
        "",
        id="upload-toast-3",
        header="",
        is_open=False,
        dismissable=True,
        duration=3000,
        style=toastStyle,
    ),
    html.Div(id='output-datatable'),
    html.A(
        html.Button(
            [
                html.I(className="fas fa-undo", style=dict(display='inline-block')),
                html.Div("", style=dict(display='inline-block'))
            ],
            id="btn_reset", 
            style={
                "position": "fixed",
                "left": "20rem",
                "bottom": "1rem",
                "display": "inline-block",
                "padding": "7px 10px",
                "border": "none",
                "background": "#D7CCC8",
                "borderRadius": "5px",
                "color": "white"
            },
            title='Reset'
        ),
        href='/'
    )
])

########################### Callback for visualization ######################
@callback(
    [
        Output('output-datatable', 'children'),
        Output('output-table', 'data')
    ],
    [
        Input('upload-data', 'contents')
    ],
    [
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified'),
        State('output-table', 'data')
    ]
)

########################## Callbacks for dcc store ##########################
@callback(
    [
        Output('input-feed', 'data'), 
        Output('upload-data', 'style'), 
        Output('upload-toast', 'is_open'),
        Output('upload-toast', 'style'), 
        Output('upload-toast', 'header'), 
        Output('upload-toast', 'children')
    ],
    [
        Input('upload-data', 'contents')
    ],
    [
        State('upload-data', 'filename'), 
        State('upload-toast', 'is_open'),
        State('input-feed', 'data')
    ]
)             
def feed_data(contents, filename, is_open, data):
    if contents is not None:
        if 'input.xlsx' in filename[0]:
            input_feed = pd.read_excel(filename[0],'feed')
            return input_feed.to_dict('records'), btnUploadedStyle, not is_open, toastStyle, "Success!", "Input data file uploaded."
        else:
            return None, btnRegularStyle, not is_open, toastStyleError, "Error!", "Please upload the correct input data file."
    elif data is not None:
        return data, btnUploadedStyle, is_open, toastStyle, "", ""
    else:
        return None, btnRegularStyle, is_open, toastStyle, "", ""

@callback(
    Output('input-manure', 'data'),
    Input('upload-data', 'contents'),
    [
        State('upload-data', 'filename'),
        State('input-manure', 'data')
    ]
)             
def manure_data(contents, filename, data):
    if contents is not None:
        if 'xls' in filename[0]:
            input_manure= pd.read_excel(filename[0],'manure')
            return input_manure.to_dict('records')
    elif data is not None:
        return data
            
@callback(
    [
        Output('feed-constants', 'data'),
        Output('upload-constants', 'style'), 
        Output('upload-toast-2', 'is_open'),
        Output('upload-toast-2', 'style'), 
        Output('upload-toast-2', 'header'), 
        Output('upload-toast-2', 'children')
    ],
    [
        Input('upload-constants', 'contents')
    ],
    [
        State('upload-constants', 'filename'),
        State('upload-toast-2', 'is_open'),
        State('feed-constants', 'data')
    ]
)             
def feed_const(contents, filename, is_open, data):
    if contents is not None:
        if 'constants.xlsx' in filename[0]:
            feed_constants = pd.read_excel(filename[0],'feed_related')
            return feed_constants.to_dict('records'), btnUploadedStyle, not is_open, toastStyle, "Success!", "Feed constants data file uploaded."
        else:
            return None, btnRegularStyle, not is_open, toastStyleError, "Error!", "Please upload the correct feed constants data file."
    elif data is not None:
        return data, btnUploadedStyle, is_open, toastStyle, "", ""
    else:
        return None, btnRegularStyle, is_open, toastStyle, "", ""

@callback(
    Output('animal-constants', 'data'),
    Input('upload-constants', 'contents'),
    [
        State('upload-constants', 'filename'),
        State('animal-constants', 'data')
    ]
)             
def animal_const(contents, filename, data):
    if contents is not None:
        if 'xls' in filename[0]:
            animal_constants = pd.read_excel(filename[0],'animal_related')
            return animal_constants.to_dict('records')
    elif data is not None:
        return data

@callback(
    Output('other-constants', 'data'),
    Input('upload-constants', 'contents'),
    [
        State('upload-constants', 'filename'),
        State('other-constants', 'data')
    ]
)             
def other_const(contents, filename, data):
    if contents is not None:
        if 'xls' in filename[0]:
            other_constants = pd.read_excel(filename[0],'other_constants')  
            return other_constants.to_dict('records')
    elif data is not None:
        return data

@callback(
    [
        Output('feed-constraints', 'data'),
        Output('upload-constraints', 'style'), 
        Output('upload-toast-3', 'is_open'),
        Output('upload-toast-3', 'style'), 
        Output('upload-toast-3', 'header'), 
        Output('upload-toast-3', 'children')
    ],
    [
        Input('upload-constraints', 'contents')
    ],
    [
        State('upload-constraints', 'filename'),
        State('upload-toast-3', 'is_open'),
        State('feed-constraints', 'data')
    ]
)             
def feed_constra(contents, filename, is_open, data):
    if contents is not None:
        if 'constraints.xlsx' in filename[0]:
            feed_constraints = pd.read_excel(filename[0],'feed_related')      
            return feed_constraints.to_dict('records'), btnUploadedStyle, not is_open, toastStyle, "Success!", "Constraints data file uploaded."
        else:
            return None, btnRegularStyle, not is_open, toastStyleError, "Error!", "Please upload the correct constraints data file."
    elif data is not None:
        return data, btnUploadedStyle, is_open, toastStyle, "", ""
    else:
        return None, btnRegularStyle, is_open, toastStyle, "", ""

@callback(
    Output('boundary-condition', 'data'),
    Input('upload-constraints', 'contents'),
    [
        State('upload-constraints', 'filename'),
        State('boundary-condition', 'data')
    ]
)             
def boundary_cond(contents, filename, data):
    if contents is not None:
        if 'xls' in filename[0]:
            boundary_condition = pd.read_excel(filename[0],'boundary')  
            return boundary_condition.to_dict('records')
    elif data is not None:
        return data
    