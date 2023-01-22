import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import dalex as dx
from plotly.io import to_json, read_json

class CreateGraph:
    """
    Klasa CreateGraph została utworzona w celu integracji wykresów tworzonych w trakcie analizy danych oraz modelowania
    z aplikacją napisaną przy użyciu frameworka Dash.
    """

    def load_eda_plots(self, names=[]):
        """
        Dotyczy strony Analiza danych
        Wczytaj wykresy z plików w formacie json (zapisanych w folderze assets) i zwróć je zapisane w tabeli
        :return: list - tabela zawierająca zapisane wykresy typu figure
        """
        output = []
        for key in names:
            file = "../Dash_app/assets/eda_{0}.json".format(key)
            output.append(read_json(file, output_type='Figure', skip_invalid=False, engine=None))
        return output
    def save_eda_plots(self, plots = [], names=[]):
        """
        Zapisz wykresy w formacie json w folderze assets
        :param plots: lista zawierająca obiekty figures
        :return: None
        """
        for key, value in plots.items():
            with open("../Dash_app/assets/eda_{0}.json".format(key), 'w') as f:
                f.write(to_json(value))
        return None
class DashExplainers:
    def __init__(self, model, X_test, y_test):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.explainer = dx.Explainer(model, X_test, y_test)
    def plot_importance(self):
        """
        Funkcja, ktora tworzy i zwraca wykres istotności zmiennych
        :return: fig
        """
        explanation = self.explainer.model_parts()
        fig = explanation.plot(title='Istotność zmiennych', digits=1, show=False)
        fig.layout.height = 400
        fig.layout.width = 550
        fig.update_layout(yaxis=dict(showgrid=False),
                           xaxis=dict(showgrid=False),
                              paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='#616161',
                              title_font={"size": 20})
        return fig




