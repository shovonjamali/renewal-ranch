import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
from pages import home, currentemissionstatus, milkoptimization, milkoptimization2, milkoptimization3, recommendations, iot, insights


# Initializing dash app
app = dash.Dash(external_stylesheets=[
        dbc.themes.BOOTSTRAP, 
        'https://use.fontawesome.com/releases/v5.8.1/css/all.css'
    ],
    suppress_callback_exceptions=True)

server = app.server

image_path = 'assets/logo.png'
image_path_bottom_logo = 'assets/logo_bottom.png'

# The style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#4E342E"  # "#0A2558"
}

# The styles for the main content position it to the right of the sidebar and add some padding.
CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem"
}

# The sidebar contents are specified here
sidebar = html.Div(
    [
        html.H2("Renewal Ranch", className="text-white"),
        html.Img(src=image_path, style={"width": "100%"}),
        html.Hr(className="text-white"),
        html.P(
            "Optimizing livestock farming for a sustainable tomorrow", className="text-white"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Main Hub", href="/", active="exact", className="text-white"),
                dbc.NavLink("Active Emission Metrics", href="/currentstatus", active="exact", className="text-white"),
                dbc.NavLink("Strategic Suggestions", id="recommendations", href="/recommendations", className="text-white", active="exact"),
                #dbc.NavLink("Milk Optimization", id="milkoptimization3", href="/milkoptimization3", className="text-white", active="exact"),
                dbc.NavLink("IoT Metrics", href="/iot", active="exact", className="text-white"),
                dbc.NavLink("IoT-Driven Insights", href="/insights", active="exact", className="text-white")
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(className="text-white"),
        html.Img(src=image_path_bottom_logo, style={"width": "100%", "margin-top": "15%"}),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

# The front page layout combined and the dcc store values to share across the pages
app.layout = html.Div(
                [
                    dcc.Location(id='url'), sidebar, content,
                    dcc.Store(id='input-feed', data=None, storage_type='memory'),
                    dcc.Store(id='input-manure', data=None, storage_type='memory'),
                    # dcc.Store(id='input-concentrate', data=None, storage_type='memory'),
                    dcc.Store(id='feed-constants', data=None, storage_type='memory'),
                    dcc.Store(id='animal-constants', data=None, storage_type='memory'),
                    dcc.Store(id='other-constants', data=None, storage_type='memory'),
                    dcc.Store(id='feed-constraints', data=None, storage_type='memory'),
                    dcc.Store(id='boundary-condition', data=None, storage_type='memory'),
                    dcc.Store(id='emission-cal', data=None, storage_type='memory'),    
                    dcc.Store(id='cost-cal', data=None, storage_type='memory'),        
                    dcc.Store(id='feed-scenario', data=None, storage_type='memory'),   
                    dcc.Store(id='opt-feed', data=None, storage_type='memory'),                           
                    dcc.Store(id='output-table', data=None, storage_type='memory'),
                ]
            )

# Navigating through the sidebar links
@app.callback(
        Output("page-content", "children"), 
        [Input("url", "pathname")]
    )
def render_page_content(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/currentstatus":
        return currentemissionstatus.layout
    elif pathname == "/recommendations":
        return recommendations.layout
    elif pathname == "/milkoptimization":
        return milkoptimization.layout
    elif pathname == "/milkoptimization2":
        return milkoptimization2.layout
    elif pathname == "/milkoptimization3":
        return milkoptimization3.layout
    elif pathname == "/iot":
        return iot.layout
    elif pathname == "/insights":
        return insights.layout
    else:
        return "404 Page Error! Please choose a link."


@app.callback(
    Output("recommendations-collapse", "is_open"),
    Input("recommendations-navlink", "n_clicks"),
    State("recommendations-collapse", "is_open"),
    
)
def toggle_recommendations_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    else:
        return is_open
    
if __name__ == "__main__":
    # app.run_server(debug=True, port=8888)
    app.run_server(debug=False, port=8888)      # to turn off the errors that's being displayed when the page loads


