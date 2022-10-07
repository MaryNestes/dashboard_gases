from dash import Dash, Input, Output
from .elements import layout
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from dash import dcc
import os

from .config import PATH, TOKEN, STYLE

app = Dash(__name__)

app.layout = layout


@app.callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    prevent_initial_call=True, )
def func(n_clicks):
    return dcc.send_file(r"../Guide.pdf")


@app.callback(
    Output("dropdown", "options"), Input("dropdown", "search_value")
)
def material_options(search_value):
    return [{"label": i, "value": i} for i in ['CO2', 'SO2', 'N2O', 'CO', 'CH4', 'HNO3']]


@app.callback(
    [Output("date", "options"), Output("date", "value")],
    [Input("date", "search_value"), Input("dropdown", "value")])
def func(value, dropdown):
    if dropdown in ['CO2', None]:
        list = sorted(os.listdir(PATH + os.sep + 'CO2'))
    else:
        list = sorted(os.listdir(PATH + os.sep + '{}_MR'.format(dropdown)))
    list = [i.replace('.csv', '').replace('_', ' ') for i in list]

    date_options = [{'label': x, 'value': x} for x in list]
    return date_options, date_options[-1]['value']


@app.callback(
    Output(component_id='pressure', component_property='figure'),
    [Input(component_id='dropdown', component_property='value'),
     Input(component_id='date', component_property='value'),
     Input(component_id='slider', component_property='value')])
def update_pressure_map(dropdown, date, slider):
    if dropdown == 'CO2':
        pp = 'ppmv'
        gas = pd.read_csv(PATH + os.sep + '{}'.format(dropdown) + os.sep + date[:8] + '_' + date[9:] + '.csv')
    else:
        if dropdown == 'CH4':
            pp = 'ppmv'
        else:
            pp = 'ppbv'
        gas = pd.read_csv(PATH + os.sep + '{}_MR'.format(dropdown) + os.sep + date[:8] + '_' + date[9:] + '.csv')
    df = pd.DataFrame(gas)
    h = [0, 100, 250, 500, 700, 850, 1000]
    i = h.index(slider)

    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color='{}'.format(slider),
                            color_continuous_scale=px.colors.diverging.Portland,
                            title='Объемная концентрация в слоях {0}-{1}gPa атмосферы:'.format(h[i - 1], slider))

    fig.update_traces(marker={'size': 17, "opacity": 0.2}, mode='markers',
                      hovertemplate='Широта=%{lon}<br>Долгота=%{lat}<br>Значение=%{marker.color}')
    fig.update_layout(mapbox={'center_lat': 58, 'center_lon': 76, 'zoom': 3,
                              'accesstoken': TOKEN, 'style': STYLE},
                      title_font={'family': 'Times New Roman', 'color': 'black', 'size': 25}, title_x=0.5,
                      coloraxis_colorbar={'title': "Среднее,{}".format(pp)})

    return fig


@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='dropdown', component_property='value'),
     Input(component_id='date', component_property='value')])
def update_map(value, dt):
    if value in ['CO2', None]:
        pp = 'ppmv'
        gas = pd.read_csv(PATH + os.sep + '{}'.format(value) + os.sep + dt[:8] + '_' + dt[9:] + '.csv')

    else:
        if value == 'CH4':
            pp = 'ppmv'
        else:
            pp = 'ppbv'
        gas = pd.read_csv(PATH + os.sep + '{}_MR'.format(value) + os.sep + dt[:8] + '_' + dt[9:] + '.csv')
    df = pd.DataFrame(gas)

    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color='Mean',
                            hover_data=["100", "250", '500', '700', '850', '1000'],
                            color_continuous_scale=px.colors.diverging.Portland,
                            title='Среднее значение объемной концентрации в столбе атмосферы:')

    fig.update_traces(marker={'size': 17, "opacity": 0.2}, mode='markers',
                      hovertemplate='Широта=%{lon}<br>Долгота=%{lat}<br>Среднее=%{marker.color}')
    fig.update_layout(mapbox={'center_lat': 58, 'center_lon': 76, 'zoom': 3, 'accesstoken': TOKEN, 'style': STYLE},
                      title_font={'family': 'Times New Roman', 'color': 'black', 'size': 25}, title_x=0.5,
                      coloraxis_colorbar={'title': "Среднее,{}".format(pp)})

    return fig


@app.callback(
    Output(component_id='line', component_property='figure'),
    [Input(component_id='map', component_property='clickData'),
     Input(component_id='dropdown', component_property='value')])
def update_fig(input_value, dropdown):
    if not input_value is None:
        value = input_value['points'][0]['customdata']
        height = [100, 250, 500, 700, 850, 1000]
        z = (max(value) - min(value)) / 2
        fig = px.line(x=value, y=height)

        if (dropdown == 'CO2') or (dropdown == 'CH4'):
            fig.update_layout(yaxis={'autorange': "reversed", 'title': 'Высота,gPa'},
                              xaxis={'range': [min(value) - z, max(value) + z], 'title': {'text': 'ppmv'}},
                              plot_bgcolor='#dadde3', showlegend=False, margin=dict(t=20, l=0, b=0, r=0),
                              title={'text': 'Объемная кон-ция', 'x': 0.3, 'font': {'size': 12}})
        else:
            fig.update_layout(yaxis={'autorange': "reversed", 'title': 'Высота,gPa'},
                              xaxis={'range': [min(value) - z, max(value) + z], 'title': 'ppbv'},
                              plot_bgcolor='#dadde3', showlegend=False, margin=dict(t=20, l=0, b=0, r=0),
                              title={'text': 'Объемная кон-ция', 'x': 0.3, 'font': {'size': 12}})

        return fig
    else:
        fig = px.line(x=[0, 0, 0, 0, 0, 0], y=[0, 0, 0, 0, 0, 0])
        fig.update_layout(yaxis={'title': 'Высота,gPa'},
                          xaxis={'title': 'ppbv'}, plot_bgcolor='#dadde3', showlegend=False,
                          margin=dict(t=20, l=0, b=0, r=0),
                          title={'text': 'Объемная кон-ция', 'x': 0.3, 'font': {'size': 12}})
        return fig
