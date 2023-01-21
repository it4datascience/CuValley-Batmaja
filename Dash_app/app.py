import dash
from dash import dcc
from dash import html

app = dash.Dash(__name__, use_pages=True)
server = app.server
app.config.suppress_callback_exceptions=True


app.layout = html.Div([
    html.Div(
        [
            html.Div([
                dcc.Link(
                    html.Button(f"{page['name']}"), href=page["path"]
                )
                for page in dash.page_registry.values()]
            )
        ]
    ),
    html.H3('STWORZENIE SYSTEMU AUTOMATYCZNEJ ESTYMACJI POZIOMU WODY W RZECE',
            style={'text-align':'center', 'color':'#035891'}),

	dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8080)