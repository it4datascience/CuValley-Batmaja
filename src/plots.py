import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import dalex as dx
from plotly.io import to_json, read_json
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from ast import literal_eval

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

class DataAnalysis:
    def __init__(self):
        self.dates_idx = pd.date_range(start='2011-01-01', end='2021-10-31', freq='1D')
    def load_hydro_data(self,path):
        #Load hydro
        self.hydro = pd.read_excel(path+'hydro.xlsx', sheet_name='hydro', header=[1, 2])
        # taking only Date and level of water
        self.hydro.columns = ['Data'] + [f'{col_name} Stan wody [cm]' for col_name in self.hydro.columns.get_level_values(0)][1:]
        # set the column type for column with date
        self.hydro['Data'] = pd.to_datetime(self.hydro['Data'], format='%Y-%m-%d')
        ################# Add new dates for modeling purposes | To change when will be new datasets
        self.hydro = self.hydro.set_index('Data').reindex(self.dates_idx).reset_index().rename({'index': 'Data'}, axis=1)
        self.hydro = self.hydro.bfill().ffill()
        ###############################################################################################

        # Change col type with level of water to int
        for col_name in self.hydro.columns[1:]:
            self.hydro[col_name] = self.hydro[col_name].astype(int)
        return self.hydro

    def load_prepared_dataset(self, path='../results/'):
        self.dataset = pd.read_csv(path+'prepared_data.csv')
        self.dataset['Data'] = pd.to_datetime(self.dataset['Data'], format='%Y-%m-%d')
        self.hierarchy = pd.read_csv(path+'prepared_hierarchy.csv')
        return self.dataset, self.hierarchy

    def create_col_name(station_id, station_name, suffix):
        name = f'{station_name} ({station_id}) {suffix}'
        return name




    def line_plot(self,title):
        trace1 = go.Scatter(x=self.hydro['Data'], y=self.hydro['GŁOGÓW (151160060) Stan wody [cm]'], name='Stacja Głogów',marker_color='#fcb040')
        trace2 = go.Scatter(x=self.hydro['Data'], y=self.hydro['RACIBÓRZ-MIEDONIA (150180060) Stan wody [cm]'], name='Stacja Racibórz-Miedonia',marker_color='#035891',)
        traces = [trace1, trace2]
        layout = go.Layout(title=title, xaxis=dict(title = 'Czas',showgrid=False,color='black'),
                           yaxis=dict(title = 'Poziom wody',showgrid=False,title_font={"size": 20},color='black'))
        fig = go.Figure(data=traces, layout=layout)
        fig.layout.height = 600
        fig.layout.width = 1200
        fig.update_layout(title_font={'size': 30}, title_x=0.5,font_family="Lato, sans-serif",
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)')
        return fig

    def corr_stations(self):
        rs=literal_eval(self.rs)
        df = {'rs': rs, 'Offset': list(range(-9,10))}
        df = pd.DataFrame(data=df)
        data = px.line(df,y='rs',x='Offset')
        layout = go.Layout()

        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(
            xaxis_title='Offset', yaxis_title='Pearson r',
            xaxis_tickvals=[-9, -6, -3, 0, 3, 6, 9],
            xaxis_range=[-9, -9], yaxis_range=[0, 1])
        fig.add_trace(go.Scatter(x=[0, 0], y=[0, 1], mode='lines', name='Center'))
        fig.add_trace(go.Scatter(x=[df._get_value(df['rs'].idxmax(), 'Offset'),df._get_value(df['rs'].idxmax(), 'Offset')]
                                 , y=[0, 1], mode='lines', name='Peak synchrony'))
        return fig
    def load_corr_stations(self, path='../results/'):
        self.df_corr = pd.read_csv(path+'corr_stations.csv')
        self.rs = self.df_corr['corr'][0]
        self.df_corr = self.df_corr.drop(self.df_corr.index[0])
        return None
    def corr_stations_2(self, pierwsza_stacja='GŁOGÓW', druga_stacja='RACIBÓRZ (350180540) Suma opadów [mm]'):
        #dodac tytul pierwsza i druga stacja
        index = self.df_corr[(self.df_corr['pierwsza_stacja'] == pierwsza_stacja) & (self.df_corr['druga_stacja'] == druga_stacja)].index[0]
        corr = self.df_corr._get_value(index, 'corr')
        rs = literal_eval(corr)
        df = {'rs': rs, 'Offset': list(range(-9, 10))}
        df = pd.DataFrame(data=df)
        data = px.line(df, y='rs', x='Offset')
        layout = go.Layout()
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(
            xaxis_title='Offset', yaxis_title='Pearson r',
            xaxis_tickvals=[-9, -6, -3, 0, 3, 6, 9],
            xaxis_range=[-9, -9], yaxis_range=[0, 1])
        fig.add_trace(go.Scatter(x=[0, 0], y=[0, 1], mode='lines', name='Center'))
        fig.add_trace(
            go.Scatter(x=[df._get_value(df['rs'].idxmax(), 'Offset'), df._get_value(df['rs'].idxmax(), 'Offset')],
                       y=[0, 1], mode='lines', name='Peak synchrony'))
        return fig



class SaveData():
    def __init__(self):
        self.df = pd.DataFrame(columns=['pierwsza_stacja','druga_stacja','corr'])
    def add_to_df(self,first_station,second_station, rs):
        self.df = self.df.append(pd.DataFrame([[first_station,second_station, rs]], columns=['pierwsza_stacja','druga_stacja','corr']))
        return  None
    def save_df(self):
        self.df.to_csv('../results/corr_stations.csv', index=False)










