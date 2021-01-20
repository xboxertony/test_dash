import dash
import dash_core_components as dcc
import dash_html_components as html
import math
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

df = pd.read_csv(
    "https://storage.googleapis.com/learn_pd_like_tidyverse/gapminder.csv")
bubble_size = [math.sqrt(p / math.pi) for p in df["pop"].values]
df['size'] = bubble_size
sizeref = 2*max(df['size'])/(100**2)

app.layout = html.Div([
    html.H2(children='A Gapminder Replica with Dash'),
    dcc.Graph(
        id='gapminder',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['continent'] == i]['gdpPercap'],
                    y=df[df['continent'] == i]['lifeExp'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': df[df['continent'] == i]['size'],
                        'line': {'width': 1, 'color': 'white'},
                        'sizeref': sizeref,
                        'symbol': 'circle',
                        'sizemode': "area"
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)