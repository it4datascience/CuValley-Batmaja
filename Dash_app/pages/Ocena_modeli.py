import dash
from dash import html, dcc,callback, Input, Output
from joblib import load
import pandas as pd
import dalex as dx
from src.plots import DashExplainers
dash.register_page(__name__, order=2)


with open('../Dash_app/assets/fitted_model.pkl', 'rb') as file:
    model = load(file)
X_test = pd.read_csv('../Dash_app/assets/X_test.csv')
y_test = pd.read_csv('../Dash_app/assets/y_test.csv')

# de = DashExplainers(model, X_test, y_test)
# importance = de.plot_importance()




layout = html.Div(
html.Div([
html.Br(),
dcc.Tabs(
        id='tabs-2',
        children=[
            dcc.Tab(label='Baseline', value='tab-1',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
            dcc.Tab(label='Bayesian Ridge', value='tab-2',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
            dcc.Tab(label='Temporal Fusion Transformer', value='tab-3',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"})
        ],
        value='tab-1',
    colors={
        "border":"#b3b3b3", #obwodka
        "background":'white', #tlo
        'primary':'#035891' #jesli wybrane

    },
),
html.Div(id='div-2')
])
)

@callback(
    Output('div-2', 'children'),
    [Input('tabs-2', 'value')]
)
def render_content(tab):
    if tab=='tab-1':
        return html.Div([

        ])
    elif tab == 'tab-2':
        return html.Div([

        ])
    elif tab == 'tab-3':
        return html.Div([

        ])