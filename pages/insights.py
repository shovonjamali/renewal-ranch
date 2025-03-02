from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
import seaborn as sns
from pages import iot_analysis as ia
import plotly.graph_objs as go


##############Data Preparation for insights
iotdata_new = ia.iotdata.copy()
iotdata_stat = iotdata_new.describe()
iotdata_stat = iotdata_stat.round(2)
iotdata_stat = iotdata_stat.rename_axis('Statistics').reset_index()

########## generate heatmap figure
# Create a custom color scale from red to white to green
custom_color_scale = [[0, 'rgb(255, 0, 0)'], [0.5, 'rgb(255, 255, 255)'], [1, 'rgb(0, 255, 0)']]

fig = px.imshow(iotdata_new.corr(), text_auto=True, aspect="auto", color_continuous_scale=custom_color_scale) 

#The style arguments for the insights page contents
layout = html.Div([
    html.B("IoT Activity Report"),
    dash_table.DataTable(
            data=iotdata_stat.to_dict('records'),
            ),
    html.B("IoT Interaction Map"),
    dcc.Graph(
        id='heatmap',
        # figure = heatmap_fig
        figure=fig
    )
])


