#############################################################################
# Name: Capstone Enhancement - Dashboard
# Course: CS499 Computer Science Capstone
# Student: Buddy Marcey
# Date: 12-1-2024
#############################################################################

'''
The purpose of this program is to provide an end user with a dashboard
to access data stored in a MongoDB database. This MongoDB instance is running
in an EC2 instance on AWS. This script builds and updates the dashboard, which will
run on the local machine that starts the script.
'''

from dash import Dash, html, dash_table, dcc, callback, Output, Input
import base64
import plotly.express as px
import dash_leaflet as dl

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from CRUD import AnimalShelter

# initiate database connection and set up initial dataframe

username = "UserAdmin"
password = "HorseGirl1979!"

db = AnimalShelter(username, password)

df = pd.DataFrame.from_records(db.read({}))

df.drop(columns=['_id'], inplace=True)

###################################################################
# Dashboard HTML components
###################################################################

app = Dash()

# Brand logo image
image_filename = 'venv/Grazioso Salvare Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([

    html.Img(src='data:image/png;base64, {}'.format(encoded_image.decode()), height='100px'),

    html.Center(html.B(html.H3('Enhanced Database Dashboard Developed by Buddy Marcey for CS499'))),
    html.Hr(),
    html.Div(children='Animals'),
    html.Div(
        dcc.RadioItems(
            id='filter-type',
            options=[
                {'label' : 'Water Rescue', 'value' : 'waterRescue'},
                {'label' : 'Mountain/Wilderness Rescue', 'value' : 'wildRescue'},
                {'label' : 'Disaster Rescue/Scent Tracking', 'value' : 'scentRescue'},
                {'label' : 'Reset', 'value' : 'reset'},
            ],
            value='reset',
            inline=True
        )
    ),

    # 10 items in the initial table setup with sortable buttons
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
            hidden_columns=['animal_id', 'animal_type', 'datetime', 'monthyear', 'location_lat',
            'location_long', 'age_upon_outcome_in_weeks', '', 'outcome_subtype', 'outcome_type'],
            data=df.to_dict('records'), 
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable=False,
            row_selectable="multi",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[2],
            page_action="native",
            page_current=0,
            page_size=10,
            ),

    # displays the pie chart and map in a row below the table
    html.Div(
        className='row',
        style={'display' : 'flex'},
        children=[
            html.Div(
                id='graph-id',
                className='col s12 m6',
            ),
            html.Div(
                id='map-id',
                className='col s12 m6',
            )
        ])
    ])

@app.callback([Output('datatable-id', 'data'),
Output('datatable-id', 'columns')],
[Input('filter-type', 'value')])

def update_dashboard(filter_type):
    if filter_type == 'waterRescue':
        df = pd.DataFrame.from_records(db.read(
            {'$and' : [
                {'breed' : {'$in' : [
                    'Labrador Retriever Mix',
                    'Chesapeake Bay Retriever',
                    'Newfoundland',
                ]}},
                {'sex_upon_outcome' : 'Intact Female'},
                {'$and' : [
                    {'age_upon_outcome_in_weeks' : {'$gte' : 26}},
                    {'age_upon_outcome_in_weeks' : {'$lte' : 156}}
                ]}
            ]}
        ))

    elif filter_type == 'wildRescue':
        df = pd.DataFrame.from_records(db.read(
            {'$and' : [
                {'breed' : {'$in' : [
                    'German Shepherd',
                    'Alaskan Malamute',
                    'Old English Sheepdog',
                    'Siberian Husky',
                    'Rottweiler',
                ]}},
                {'sex_upon_outcome' : 'Intact Male'},
                {'$and' : [
                    {'age_upon_outcome_in_weeks' : {'$gte' : 26}},
                    {'age_upon_outcome_in_weeks' : {'$lte' : 156}}
                ]}
            ]}
        ))

    elif filter_type == 'scentRescue':
        df = pd.DataFrame.from_records(db.read(
            {'$and' : [
                {'breed' : {'$in' : [
                    'Doberman Pinscher',
                    'German Shepherd',
                    'Golden Retriever',
                    'Bloodhound',
                    'Rottweiler',
                ]}},
                {'sex_upon_outcome' : 'Intact Male'},
                {'$and' : [
                    {'age_upon_outcome_in_weeks' : {'$gte' : 20}},
                    {'age_upon_outcome_in_weeks' : {'$lte' : 300}}
                ]}
            ]}
        ))

    elif filter_type == 'reset':
        df = pd.DataFrame.from_records(db.read({}))

    # adjustments to retrieved data
    df.drop(columns=['_id'], inplace=True)
    columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')

    return (data, columns)

@app.callback(
    Output('graph-id', 'children'),
    [Input('datatable-id', 'derived_viewport_data')]
)

def update_graphs(viewData):
    graphData = pd.DataFrame.from_dict(viewData)

    return [dcc.Graph(
        figure = px.histogram(graphData, x='breed'),
        )
    ]
    
@app.callback(
    Output('map-id', 'children'),
    [Input('datatable-id', "derived_virtual_data"),
    Input('datatable-id', "derived_virtual_selected_rows")]
)

def update_map(viewData, index):
    dff = pd.DataFrame.from_dict(viewData)
    if index is None:
        row = 0
    else:
        row = index[0]

    # returns the map component on data parameter change
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'},
        center=[30.75, -97.48],
        zoom=10,
        children=[
            dl.TileLayer(id="base_layer_id"),
            dl.Marker(position=[
                dff.iloc[row, 12],
                dff.iloc[row, 13]],
                children=[
                    dl.Tooltip(dff.iloc[row, 4]),
                    dl.Popup([
                        html.H1("Animal Name"),
                        html.P(dff.iloc[row, 15])
                ])
            ])
        ])
    ]

    
# serve the app
if __name__ == '__main__':
    app.run(debug=True) 