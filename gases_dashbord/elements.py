import os
from dash import dcc, html

from .config import PATH

files = [i.replace('.csv', '').replace('_', ' ') for i in sorted(os.listdir(PATH + os.sep + 'CO2'))]

dropdown = dcc.Dropdown(
    id="dropdown",
    options=[
        {'label': x, 'value': x}
        for x in ['CO2', 'SO2', 'N2O', 'CO', 'CH4', 'HNO3']
    ],
    value='CO2',
    clearable=False
)
date = dcc.Dropdown(
    id='date',
    options=[{'label': x, 'value': x} for x in files],
    value=files[-1],
    clearable=False,
    searchable=False
)

slider = dcc.Slider(min=100, max=1000,
                    step=None,
                    marks={
                        100: '0-100',
                        250: '100-250',
                        500: '250-500',
                        700: '500-700',
                        850: '700-850',
                        1000: '850-1000'
                    },
                    value=500,
                    id='slider')

layout = html.Div([
    html.Div([
        html.Label('Выберите газ:', style={'left': '150px', 'position': 'absolute', 'width': '150px', 'top': '10px'}),
        html.Div(dropdown, style={'width': '100px', 'left': '150px', 'top': '50px', 'position': 'absolute'}),
        html.Label('Выберите дату: (ГГГГММДД ччмм)', style={'left': '300px', 'position': 'absolute', 'width': '150px'}),
        html.Div(date, style={'width': '200px', 'position': 'absolute', 'left': '300px', 'top': '50px'}),
        html.Div(slider,
                 style={'width': '800px', 'margin-left': '1300px', 'display': 'inline-block ', 'position': 'absolute'})
    ], style={'margin-left': '100px', 'position': 'absolute'}),
    html.Button("Руководство по использованию", id="btn-download-txt"),
    dcc.Download(id="download-text"),
    html.Div([dcc.Graph(id='map', config={'displayModeBar': False},
                        style={'width': '1200px', 'display': 'inline-block ', 'height': '800px', 'position': 'absolute',
                               'top': '200px', 'left': '20px'}),
              dcc.Graph(id='line', config={'displayModeBar': False},
                        style={'width': '200px', 'height': '300px', 'position': 'absolute',
                               'top': '300px', 'left': '50px'}),
              dcc.Graph(id='pressure', config={'displayModeBar': False},
                        style={'width': '1200px', 'height': '800px', 'position': 'absolute',
                               'top': '200px', 'left': '1200px', 'display': 'inline-block '})
              ], style={'width': '100%'})
])
