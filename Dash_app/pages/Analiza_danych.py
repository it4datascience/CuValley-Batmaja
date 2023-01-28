import dash
from dash import html, dcc,callback, Input, Output
from src.plots import DataAnalysis
dash.register_page(__name__, order=1)

da = DataAnalysis()
da.load_hydro_data(path = '../data/')
da.load_corr_stations()
figure_1 = da.line_plot("Stan poziomu wody w stacjach Głogów i Racibórz-Miedonia")
figure_2 = da.corr_stations()
figure_3 = da.corr_stations_2()
drop_style = {'background-color': '#cfa527', 'textAlign': 'center', 'margin': 'auto', 'color':'black'}
water_level_cols = {'GŁOGÓW (151160060) Stan wody [cm]','RACIBÓRZ-MIEDONIA (150180060) Stan wody [cm]'}
hydro_cols = []
meteo_cols=[]
drop_station = dcc.Dropdown(id='drop-1',
                            options=[{"label":i.split(")")[0]+')', "value":i} for i in water_level_cols],
                            placeholder='Wybierz stację do analizy', className='dropdown',multi=True,
                            style=drop_style
                            )
drop_hydro = dcc.Dropdown(id='drop-2',
                            options=[{"label":i.split(")")[0]+')', "value":i} for i in hydro_cols],
                            placeholder='Wybierz stację hydrologiczną do analizy', className='dropdown',multi=True,
                            style=drop_style
                            )
drop_meteo = dcc.Dropdown(id='drop-3',
                            options=[{"label":i.split(")")[0]+')', "value":i} for i in meteo_cols],
                            placeholder='Wybierz stację meteorologiczną do analizy', className='dropdown',multi=True,
                            style=drop_style
                            )


layout = html.Div([
# tytul

    html.Div([
    html.Br(),
    dcc.Tabs(
        id='tabs-1',
        children=[
            dcc.Tab(label='Porównanie poziomów pomiędzy stacjami', value='tab-1',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
            dcc.Tab(label='Korelacja oddziaływania pomiędzy stacjami', value='tab-2',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
            dcc.Tab(label='Korelacja oddziaływania pomiędzy stacjami,a opadami', value='tab-3',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"})
        ],
        value='tab-1',
    colors={
        "border":"#b3b3b3", #obwodka
        "background":'white', #tlo
        'primary':'#035891' #jesli wybrane

    },
),
    html.Div(id='div-1')
])])

@callback(
    Output('div-1', 'children'),
    [Input('tabs-1', 'value')]
)
def render_content(tab):
    if tab=='tab-1':
        return html.Div([
            html.Br(),
            drop_station,
            html.Br(),
            html.Div([
                html.Br(),
                dcc.Graph(figure=figure_1),

            ],
                className='add_container twelve columns'
            )

        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Br(),
            html.Div([
                html.Br(),
                dcc.Graph(figure=figure_2),

            ],
                className='add_container twelve columns'
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.Br(),
            drop_hydro,
            html.Br(),
            drop_meteo,
            html.Br(),
            html.Div([
                html.Br(),
                dcc.Graph(figure=figure_3),

            ],
                className='add_container twelve columns'
            )
        ])
