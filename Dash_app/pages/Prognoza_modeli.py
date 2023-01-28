import dash
from dash import html, dcc,callback, Input, Output
from src.plots import MLModels
dash.register_page(__name__, order=3)

ml = MLModels()
ml.load_data()
figure_1 = ml.model_forecast_plot()
layout = html.Div(
html.Div([
html.Br(),
dcc.Tabs(
        id='tabs-3',
        children=[
            dcc.Tab(label='Baseline', value='tab-1',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
            dcc.Tab(label='Bayesian Ridge', value='tab-2',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
        ],
        value='tab-1',
    colors={
        "border":"#b3b3b3", #obwodka
        "background":'white', #tlo
        'primary':'#035891' #jesli wybrane

    },
),
html.Div(id='div-3')
])
)

@callback(
    Output('div-3', 'children'),
    [Input('tabs-3', 'value')]
)
def render_content(tab):
    if tab=='tab-1':
        return html.Div([
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

        ])
