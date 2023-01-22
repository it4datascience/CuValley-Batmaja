import dash
from dash import dcc
from dash import html
app = dash.Dash(__name__, use_pages=True)
server = app.server
app.config.suppress_callback_exceptions=True


app.layout = html.Div([
html.Div([
    html.Div(
        html.Img(src='assets/logo_BATMAJA.png', className='center-image', style={
                'height': '20%',
                'width': '20%',
            }),
        className='center-div'
    ),
    html.A(
    html.Div(
        html.Img(src='assets/logo_CUVALLEY.jpg', className='right-top-image'),
        className='right-top-div'
    ), href='https://cuvalley.com/stworzenie-systemu-automatycznej-estymacji-poziomu-wody-w-rzece/')
], style={"display":"flex"}),
    html.H3('RIVER ESTIMATOR',
            style={'text-align': 'center', 'color': '#035891'}),


    html.Div(
        [
            html.Div([
                dcc.Link(
                    html.Button(f"{page['name']}", style={"margin-right":"1%", "margin-left":"1%"}), href=page["path"],
                )
                for page in dash.page_registry.values()]
            )
        ], style={'textAlign': 'center'}
    ),

	dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8080)