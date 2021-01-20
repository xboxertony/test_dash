from dash import Dash
import dash_html_components as html

def create_dashboard(server):

    dash_app = Dash(
        server = server
        # routes_pathname_prefix = "/dashapp/",
        # external_stylesheets=[
        #     '/static/dist/css/styles.css',
        # ]
    )

    dash_app.layout = html.Div(id='dash-container')

    return dash_app.server