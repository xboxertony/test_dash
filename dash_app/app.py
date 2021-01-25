
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import pdb
import statsmodels.api as sm
from dash.exceptions import PreventUpdate

lowess = sm.nonparametric.lowess
#### Configuration =================================================
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

##### Functions =============================
def make_lowess(series):
    series = pd.Series(series)
    endog = series.values
    exog = series.index.values

    smooth = lowess(endog, exog)
    index, data = np.transpose(smooth)

    return pd.Series(data, index=pd.to_datetime(index)) 


#### Data preparation ==============================================
df_group = pd.read_pickle("./data.pkl")

df_group = df_group.replace({'建物型態_': '套房(1房1廳1衛)'}, {'建物型態_': '套房<br>(1房1廳1衛)'}, regex=False)
df_group = df_group.replace({'建物型態_': '住宅大樓(11層含以上有電梯)'}, {'建物型態_': '住宅大樓<br>(11層含以上<br>有電梯)'}, regex=False)
df_group = df_group.replace({'建物型態_': '公寓(5樓含以下無電梯)'}, {'建物型態_': '公寓<br>(5樓含以下<br>無電梯)'}, regex=False)
df_group = df_group.replace({'建物型態_': '店面(店鋪)'}, {'建物型態_': '店面<br>(店鋪)'}, regex=False)
df_group = df_group.replace({'建物型態_': '華廈(10層含以下有電梯)'}, {'建物型態_': '華廈<br>(10層含以下有電梯)'}, regex=False)

##### Lines =================================
all_area = list(np.unique(np.array(df_group['鄉鎮市區_'])))
all_type = list(np.unique(np.array(df_group['建物型態_'])))
all_y = ['單價元平方公尺_count', '單價元平方公尺_median', 'date_diff_median']
app.layout = html.Div(children=[
        html.Div([
            html.Div([
                html.Label('Y'),
                dcc.Dropdown(
                    id='my_y',
                    options=[{'label' : p, 'value' : p} for p in all_y],
                    multi=False,
                    value='單價元平方公尺_median'
                ),
            ]),
            html.Div([
                html.Label('鄉鎮市區'),
                dcc.Dropdown(
                    id='my_area',
                    options=[{'label' : p, 'value' : p} for p in all_area],
                    multi=True,
                    value=all_area[0:4]
                ),
            ]),
            html.Div([
                html.Label('建物型態'),
                dcc.Dropdown(
                    id='my_type',
                    options=[{'label': v, 'value': v} for v in all_type],
                    multi=True,
                    value=all_type[0:6]
                ),
                html.Button(id='submit-button-state', n_clicks=0, children='Submit', 
                    style={'float':'right', 'margin': '10px 0px 10px 0px'}),
            ])], className="three columns", style={'margin': '10px'}),
        html.Div([
                dcc.Loading(
                    id="loading-2",
                    children=[dcc.Graph(id='graph')],
                    type="default",
                )
            ],  className="nine columns", style={'margin': '10px'})
])
                      
@app.callback(
    Output('graph', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('my_y', 'value'),
    State('my_area', 'value'),
    State('my_type', 'value'))
def set_cities_options(n_clicks, my_y, my_area, my_type):
    # pdb.set_trace()
    if type(my_area) == type(''):
        my_area = [my_area]
    if type(my_type) == type(''):
        my_type = [my_type]
    
    # pdb.set_trace()
    df_plot = df_group[df_group['鄉鎮市區_'].isin(my_area) & df_group['建物型態_'].isin(my_type)] 
    df_plot['k'] = df_plot.groupby(['建物型態_', '鄉鎮市區_'])[my_y].transform(make_lowess)

    fig = px.line(df_plot, x="date_", y=[my_y, 'k'], 
                    height=600, width=1000,
                    facet_col="鄉鎮市區_",
                    facet_row="建物型態_", 
                    template = 'plotly', # "plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
                    # color_discrete_map={
                    #     my_y: "#456987",
                    #     "k": "#147852"
                    # }
                    )
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    # pdb.set_trace()
    # fig.data[0].mode='markers+lines'
    # for i in fig.data[0:3]: 
    #     i.mode = 'markers+lines'
    fig.update_xaxes(matches='x', tickangle=-45, title=None)
    fig.update_yaxes(matches=None, title=None, showticklabels=True, visible=True)
    fig.update_layout(showlegend=False)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)