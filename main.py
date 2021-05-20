import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_csv('twenty.csv')

app = dash.Dash("__main_PEP__")
risks = df.risk.unique()
server = app.server
app.layout = html.Div([
    html.Div([dcc.Dropdown(id='group-select', options=[{'label': i, 'value': i} for  i in risks],
                           value='TOR', style={'width': '140px'})]),
    dcc.Graph('shot-dist-graph', config={'displayModeBar': False})])


@app.callback(
    Output('shot-dist-graph', 'figure'),
    [Input('group-select', 'value')]
)
def update_graph(grpname):
    import plotly.express as px
    return px.scatter(df[df['risk']==grpname], x='score', y='total_property_assets', size='total_property_assets_divide_income', color='1')

if __name__ == '__main__':

    app.run_server(debug=False)