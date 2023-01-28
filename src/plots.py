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
        layout = go.Layout(title=title, xaxis=dict(title = 'Czas',showgrid=False,color='#035891',title_font={"size": 20}),
                           yaxis=dict(title = 'Poziom wody',showgrid=False,title_font={"size": 20},color='#035891'))
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
        data = px.line(df,y='rs',x='Offset')  #, line_color='#fcb040'
        layout = go.Layout()

        fig = go.Figure(data=data, layout=layout)
        fig.update_traces(line_color='#fcb040', line_width=3.5)
        fig.update_layout(title = 'Korelacja krzyżowa opóźnienia w czasie pomiędzy stacjami hydrologicznymi Głogów i Racibórz-Miedonia',
            xaxis_title='Offset', yaxis_title='Pearson r',xaxis_title_font={"size": 20},yaxis_title_font={"size": 20},
            xaxis_tickvals=[-9, -6, -3, 0, 3, 6, 9],
            xaxis_range=[-9, 9], yaxis_range=[df.rs.min() -0.1, df.rs.max() +0.1])
        fig.add_trace(go.Scatter(x=[0, 0], y=[df.rs.min() -0.1, df.rs.max() +0.1], mode='lines', name='Center',marker_color='black'))
        fig.add_trace(go.Scatter(x=[df._get_value(df['rs'].idxmax(), 'Offset'),df._get_value(df['rs'].idxmax(), 'Offset')]
                                 , y=[df.rs.min() -0.1, df.rs.max() +0.1], mode='lines', name='Peak synchrony',marker_color='#035891'))
        fig.layout.height = 600
        fig.layout.width = 1200
        fig.update_layout(title_font={'size': 20}, title_x=0.5, font_family="Lato, sans-serif",
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)')
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
        fig.update_traces(line_color='#fcb040', line_width=3.5)
        fig.update_layout(
            title='Korelacja krzyżowa opóźnienia w czasie pomiędzy stacją {0},a opadami mierzonymi w stacji {1}'.
            format(pierwsza_stacja,druga_stacja.split('(')[0]),
            xaxis_title='Offset', yaxis_title='Pearson r',xaxis_title_font={"size": 20},yaxis_title_font={"size": 20},
            xaxis_tickvals=[-9, -6, -3, 0, 3, 6, 9],
            xaxis_range=[-9, 9], yaxis_range=[df.rs.min() -0.1, df.rs.max() +0.1])
        fig.add_trace(go.Scatter(x=[0, 0], y=[df.rs.min() -0.1, df.rs.max() +0.1], mode='lines', name='Center',marker_color='black'))
        fig.add_trace(
            go.Scatter(x=[df._get_value(df['rs'].idxmax(), 'Offset'), df._get_value(df['rs'].idxmax(), 'Offset')],
                       y=[df.rs.min() -0.1, df.rs.max() +0.1], mode='lines', name='Peak synchrony',marker_color='#035891'))
        fig.layout.height = 600
        fig.layout.width = 1200
        fig.update_layout(title_font={'size': 20}, title_x=0.5, font_family="Lato, sans-serif",
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)')
        return fig



class SaveData():
    def __init__(self):
        self.df = pd.DataFrame(columns=['pierwsza_stacja','druga_stacja','corr'])
    def add_to_df(self,first_station,second_station, rs):
        self.df = self.df.append(pd.DataFrame([[first_station,second_station, rs]], columns=['pierwsza_stacja','druga_stacja','corr']))
        return  None
    def save_df(self):
        self.df.to_csv('../results/corr_stations.csv', index=False)

class MLModels():
    def __init__(self):
        self.df = pd.DataFrame
        self.dates_idx = pd.date_range(start='2012-01-01', end='2021-10-31', freq='1D')
    def load_data(self, path='../results/'):
        self.models_forecast = pd.read_csv(path+'models_forecast.csv')
        self.models_historical_forecasts = pd.read_csv(path+'historical_forecasts.csv')
        self.models_metrics = pd.read_csv(path+'models_metrics.csv')
        self.dataset = pd.read_csv(path+'prepared_data.csv')
        self.test_dataset = pd.read_json(path+'test_dataset.json',orient='split')
        self.dataset['Data'] = pd.to_datetime(self.dataset['Data'], format='%Y-%m-%d')
        self.models_forecast['Data'] = pd.to_datetime(self.models_forecast['Data'], format='%Y-%m-%d')
        self.models_historical_forecasts['Data'] = pd.to_datetime(self.models_historical_forecasts['Data'], format='%Y-%m-%d')
        return None
    def model_evaluation_plot(self, model='Baseline', target_to_viz = 'GŁOGÓW (151160060) Stan wody [cm]',
                              horizon_to_viz = 7,
                              title='Porównanie wartości prognozowanych przez model z wartościami rzeczywistymi'
                              ):
        df = self.models_historical_forecasts[(self.models_historical_forecasts['Model'] == model)]
        df=df[(df['Stacja']==target_to_viz)]
        df_2 = self.dataset
        if model=='Baseline':
            trace1 = go.Scatter(x=df.Data,
                                y=df[f'Forecast_-{horizon_to_viz}D'], marker_color='#fcb040', name='Prognoza modelu')
            trace2 = go.Scatter(x=df_2['Data'],
                                y=df_2[target_to_viz], marker_color='black', name='Dane historyczne')
        else:
            trace1 = go.Scatter(x=df.loc[df['Zmienne'] == 'Past+Future', 'Data'],
                                y=df.loc[df['Zmienne'] == 'Past+Future',f'Forecast_-{horizon_to_viz}D'], marker_color='#fcb040', name='Prognoza modelu')
            trace2 = go.Scatter(x=df_2['Data'],
                                y=df_2[target_to_viz], marker_color='black', name='Dane historyczne')
        traces = [trace1, trace2]
        layout = go.Layout(title=title+' dla stacji {0}'.format(target_to_viz.split('(')[0]), xaxis=dict(title='Czas', showgrid=False, color='black'),
                           yaxis=dict(title='Poziom wody', showgrid=False, title_font={"size": 20}, color='black')
                           ,xaxis_title_font={"size": 20})
        fig = go.Figure(data=traces, layout=layout)
        fig.layout.height = 600
        fig.layout.width = 1200
        fig.update_layout(title_font={'size': 20}, title_x=0.5, font_family="Lato, sans-serif",
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',xaxis_range=[df.Data.iloc[0],df.Data.iloc[-1]])
        return fig

    def model_forecast_plot(self, model='Baseline', target_to_viz = 'GŁOGÓW (151160060) Stan wody [cm]',
                            title='Predykcja modelu w przyszłość',
                            len_historic_data=60, zmienne=None):
        df = self.models_forecast[(self.models_forecast['Model'] == model)]
        df_2 = self.dataset
        df_2 = df_2[(df_2['Data'] >= '2012-01-01') & (df_2['Data'] <= '2021-10-31')]
        if model =='Baseline':
            trace1 = go.Scatter(x=df.Data,
                                y=df[target_to_viz], marker_color='black', name='Predykcja')
        else:
            trace1 = go.Scatter(x=df.loc[df['Zmienne'] == 'Past+Future', 'Data'],
                                y=df.loc[df['Zmienne'] == 'Past+Future',target_to_viz], marker_color='black', name='Predykcja')

        trace2 = go.Scatter(x=df_2.Data[-len_historic_data:],
                            y=df_2[target_to_viz][-len_historic_data:], marker_color='#fcb040', name='Dane historyczne')
        traces = [trace1, trace2]
        layout = go.Layout(title=title, xaxis=dict(title='Czas', showgrid=False, color='black'),
                           yaxis=dict(title='Poziom wody', showgrid=False, title_font={"size": 20}, color='black'),
                           xaxis_title_font={"size": 20})
        fig = go.Figure(data=traces, layout=layout)
        fig.layout.height = 600
        fig.layout.width = 1200
        fig.update_layout(title_font={'size': 30}, title_x=0.5, font_family="Lato, sans-serif",
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)')

        return fig










