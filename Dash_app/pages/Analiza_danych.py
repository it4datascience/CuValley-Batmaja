import dash
from dash import html, dcc,callback, Input, Output
from src.plots import DataAnalysis
dash.register_page(__name__, order=1)

da = DataAnalysis()
da.load_data(path = '../data/')
figure_2 = da.line_plot("Stan poziomu wody w stacjach Głogów i Racibórz-Miedonia")


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
        value='tab-2',
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
