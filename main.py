import dash
import dash_html_components as html
import datetime
import plotly.graph_objs as go
import dash_core_components as dcc
import flask
from dash.dependencies import Output,Input,State
import pandas as pd

server = flask.Flask(__name__)

app = dash.Dash(__name__,server=server)

L = {1:[[1,2,3],[4,5,6]],2:[[4,5,6,7,8],[80,90,100,200,300]]}

def update_news():
    df = pd.DataFrame({"col1":[1,2,3,4,5],"col2":[3,4,7,8,9]})
    return df

def generate_html_table():
    df = update_news()
    return html.Div([
        html.Table(
            [
                html.Tr([
                    html.Td(
                        html.A(
                            df.iloc[i,[0,1]].to_json(),
                        )
                    )
                ])
                for i in range(len(df))
            ],
            style={"height":"150px","overflowY":"scroll"}
        )
    ],style={"height":"100%"})


app.layout = html.Div([

    html.Div([
        dcc.Input(id="Random",value="1",type="text"),
        html.Button(id="submit-button",n_clicks=0,children="Submit")
    ]),

    html.Div([
            html.H1(children="Hello World"),
            html.Label("DASH GRAPH"),
            dcc.Input(
                id = "stock-input",
                placeholder = "Please Enter a stock to be charted",
                type="text",
                value = ""
            ),
            html.Div(
                dcc.Graph(id="Stock_Chart")
            ),
            html.Div(
                generate_html_table()
            )
        ],className="main")

])

#css的檔案名字是assets

@app.callback(dash.dependencies.Output("Stock_Chart","figure"),[Input("submit-button","n_clicks")]
,[State("Random","value")])
def update_chart(n_clicks,value):
    trace_close = go.Scatter(
        x=L[int(value)][0],
        y=L[int(value)][1],
        name = "close",
        line = dict(color="#f44242"))

    data = [trace_close]

    layout = {
        "title":"Callback Graph"+f"   value is {value}"
    }

    return {
        "data":data,
        "layout":layout
    }


@server.route("/")
def home():
    return app.index()

if __name__ == "__main__":
    server.run(debug=True)