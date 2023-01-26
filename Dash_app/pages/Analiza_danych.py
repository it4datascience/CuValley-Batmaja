import dash
from dash import html, dcc,callback, Input, Output
from src.plots import CreateGraph
dash.register_page(__name__, order=1)

example = 'example'
cg = CreateGraph()
figures = cg.load_eda_plots(names=[example])

layout = html.Div([
# tytul

    html.Div([
    html.Br(),
    dcc.Tabs(
        id='tabs-1',
        children=[
            dcc.Tab(label='Historyczne dane w stacjach', value='tab-1',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
            dcc.Tab(label='Porównanie poziomów pomiędzy stacjami', value='tab-2',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
            dcc.Tab(label='Korelacja oddziaływania pomiędzy stacjami', value='tab-3',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"})
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
# statystyki opisowe
html.Div([
html.Div([
html.H6(children='Title 1',
style={'textAlign': 'center',
'color': '#616161'}),
html.H6(children='Value 1',
                            style={'textAlign': 'center',
                                   'color': 'white'}),
                ], className='card_container three columns'),

                html.Div([
                    html.H6(children='Title 2',
                            style={'textAlign': 'center',
                                   'color': '#616161'}),
                    html.H6(children='Value 2',
                            style={'textAlign': 'center',
                                   'color': 'white'}),
                ], className='card_container three columns'),

                html.Div([
                    html.H6(children='Title 3',
                            style={'textAlign': 'center',
                                   'color': '#616161'}),
                    html.H6(children='Value 3',
                            style={'textAlign': 'center',
                                   'color': 'white'}),
                ], className='card_container three columns'),

                html.Div([
                    html.H6(children='Title 4',
                            style={'textAlign': 'center',
                                   'color': '#616161'}),
                    html.H6(children="Value 4",
                            style={'textAlign': 'center',
                                   'color': 'white'}),

                ], className='card_container_last three columns'), ], className='row flex display'),
            # druga linia cards
            html.Div([
            # Wykres
            html.Div([
                html.Br(),
                dcc.Graph(id="graph-1", figure=figures[0])
            ], className='add_container twelve columns')
        ])

        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Div([
                html.Div([
                    html.H6(children='Title 1',
                            style={'textAlign': 'center',
                                   'color': '#616161'}),
                    html.H6(children='Value 1',
                            style={'textAlign': 'center',
                                   'color': 'white'}),
                ], className='card_container three columns'),

                html.Div([
                    html.H6(children='Title 2',
                            style={'textAlign': 'center',
                                   'color': '#616161'}),
                    html.H6(children='Value 2',
                            style={'textAlign': 'center',
                                   'color': 'white'}),
                ], className='card_container three columns'),

                html.Div([
                    html.H6(children='Title 3',
                            style={'textAlign': 'center',
                                   'color': '#616161'}),
                    html.H6(children='Value 3',
                            style={'textAlign': 'center',
                                   'color': 'white'}),
                ], className='card_container three columns'),

                html.Div([
                    html.H6(children='Title 4',
                            style={'textAlign': 'center',
                                   'color': '#616161'}),
                    html.H6(children="Value 4",
                            style={'textAlign': 'center',
                                   'color': 'white'}),

                ], className='card_container_last three columns'), ], className='row flex display'),
            # druga linia cards
            html.Div([
                # Wykres
                html.Div([
                    html.Br(),
                    dcc.Graph(id="graph-1", figure=figures[0],style={
                                "width": "100%",
                                "height": "100%"
                            })
                ], className='add_container twelve columns textAlign center',)
            ])

        ])
