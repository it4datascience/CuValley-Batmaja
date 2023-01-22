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

de = DashExplainers(model, X_test, y_test)
importance = de.plot_importance()




layout = html.Div(
        dcc.Graph(id="graph-3", figure=importance)
)