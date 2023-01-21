import dash
from dash import html, dcc,callback, Input, Output
dash.register_page(__name__, order=1)

layout = html.Div(
    children=[
        html.H6('Stworzenie modelu/algorytmu, który na bazie danych historycznych oraz prognozy pogody, pochodzących z IMGW, pozwoli prognozować poziom wody i możliwości chłonności rzeki.')
    ]
)