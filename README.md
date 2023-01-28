# CuValley-Batmaja

![Batmaja](https://i0.wp.com/batmaja.com/wp-content/uploads/2021/04/cropped-BATMAJA-calosc.png?resize=1024%2C356&ssl=1 "Batmaja Logo")

Projekt uczenia maszynowego do predykcji poziomu wody w Odrze zrealizowany w ramach Hackathonu [**CuValley Hack**](https://cuvalley.com/).

Rezultaty zostały przedstawione w interaktywnej aplikacji dostępnej pod adresem https://cuvalley-2023-kw5yuowusq-lm.a.run.app/analiza-danych

Szeregi czasowe mają strukturę szeregów wielowymiarowych z zmiennych objaśniającymi (Multivariate TimeSeries with Covariates). Poziom rzeki w obu stacjach jest powiązany ze sobą, ponieważ pochodzą z tego samego procesu w rozumieniu szeregów czasowych. Opady wpływają na poziomy w obu stacjach pośrednio. Podczas eksploracyjnej analizy danych i korelacji krzyżowej udowodniliśmy zależności pomiędzy obiema stacjami oraz wpływem opadów na te stacje. Ponadto poziom wody w stacjach podlega sezonowości.

Korelacja krzyżowa pomiędzy stacjami:
![explanation](results/TLCC-GŁOGÓW-RACIBÓRZ-MIEDONIA.png)

Korelacja krzyżowa pomiędzy stacją w Głogowie a opadami (z uwzględnieniem zagregowanej średniej i mediany z wszystkich stacji):
![explanation](results/TLCC-GŁOGÓW-opady.png)



Materiały uzupełniające:
- [Szeregi wielowymiarowe a wiele szeregów czasowych](https://unit8co.github.io/darts/userguide/timeseries.html#multivariate-time-series-vs-multiple-time-series)
- [Zmienne objaśniające dla szeregów czasowych](https://unit8co.github.io/darts/userguide/covariates.html)