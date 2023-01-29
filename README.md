# CuValley-Batmaja

![Batmaja](https://i0.wp.com/batmaja.com/wp-content/uploads/2021/04/cropped-BATMAJA-calosc.png?resize=1024%2C356&ssl=1 "Batmaja Logo")

Projekt uczenia maszynowego do predykcji poziomu wody w Odrze zrealizowany w ramach Hackathonu [**CuValley Hack**](https://cuvalley.com/).

Rezultaty zostały przedstawione w interaktywnej aplikacji dostępnej pod adresem https://cuvalley-batmaja-kw5yuowusq-lm.a.run.app

## Spis Treści
* [O Projekcie](#o-projekcie)
* [Użyte Technologie](#użyte-technologie)
* [Aplikacja](#Aplikacja)
* [Materiały uzupełniające](#materiały-uzupełniające)

## O projekcie

Szeregi czasowe mają strukturę szeregów wielowymiarowych z zmiennych objaśniającymi (Multivariate TimeSeries with Covariates). Poziom rzeki w obu stacjach jest powiązany ze sobą, ponieważ pochodzą z tego samego procesu w rozumieniu szeregów czasowych. Opady wpływają na poziomy w obu stacjach pośrednio. Podczas eksploracyjnej analizy danych i korelacji krzyżowej udowodniliśmy zależności pomiędzy obiema stacjami oraz wpływem opadów na te stacje. Ponadto poziom wody w stacjach podlega sezonowości.

Korelacja krzyżowa pomiędzy stacjami:
![korelacja-stacja-stacja](results/TLCC-GŁOGÓW-RACIBÓRZ-MIEDONIA.png)

Korelacja krzyżowa pomiędzy stacją w Głogowie a opadami (z uwzględnieniem zagregowanej średniej i mediany z wszystkich stacji):
![korelacja-stacja-opady](results/TLCC-GŁOGÓW-opady.png)

Jako model wybrano **Bayesian Ridge**, który uwzględnia szeregi wielowymariowe (podobnie jak VARIMA). Wdrożono również model Bazowy (prognozuje ostatnią wartość ze zbioru treningowego) do celów porównawczych.

Dokonane walidacje czy backtesty nie niosły ze sobą wycieku danych (brak losowości), dlatego rezultaty są wiarygodne. Poniżej zaprezentowano backtesty dla zbioru testowego.
![backtests](results/Backtests_-7D.png)

## Użyte Technologie

* Python 3.10

* Docker

* Hosting - Google Cloud Run

## Aplikacja

* Analiza Danych

![analiza_danych](https://user-images.githubusercontent.com/101253790/215296857-ef094177-3d89-4f7a-89dc-f5ec5bf5d5ca.gif)

* Ocena Modeli

![ocena_modeli](https://user-images.githubusercontent.com/101253790/215296957-eef8756a-0f65-4327-9d3d-dcc4852a20ac.gif)

* Prognoza Modeli


![prognoza_modeli](https://user-images.githubusercontent.com/101253790/215296948-1ad3c19f-2de9-405e-b675-c5bbae5a4e20.gif)


## Uruchomienie Projektu

* Instalacja zależności

pip install -r requirements.txt

* Uruchomienie aplikacji

cd Dash_app

python app.py


## Materiały uzupełniające:
- [Szeregi wielowymiarowe a wiele szeregów czasowych](https://unit8co.github.io/darts/userguide/timeseries.html#multivariate-time-series-vs-multiple-time-series)
- [Zmienne objaśniające dla szeregów czasowych](https://unit8co.github.io/darts/userguide/covariates.html)
