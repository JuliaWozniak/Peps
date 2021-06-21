import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import json
import plotly.express as px


region = "м.+Київ"



def get_income(p):
    if 'step_11' in p['unified_source']:
        income = p['unified_source']['step_11']
    elif 'step_2' in p['unified_source']:
        income = p['unified_source']['step_2']
    else:
        return (0)
    kk = income.keys()
    total_income = 0
    for k in kk:
        try:
            item = income[k]
            if 'sizeIncome' in item:
                total_income += float(item['sizeIncome'])
        except KeyError:
            print('income') 
    return(total_income)

def get_estate(p):
    if 'step_3' in p['unified_source']:
        income = p['unified_source']['step_3']
    else:
        return ((0,0))
    kk = income.keys()
    total_area = 0
    total_cost = 0
    for k in kk:
        try:
            item = income[k]
            item_dict = {'area':0}
            if 'totalArea' in item:
                total_area += float(item['totalArea'])
            if 'costAssessment' in item:
                total_cost += float(item['costAssessment'])
        except KeyError as e:
            print(e)
    return((total_area, total_cost))

def get_cars(p):
    if 'step_6' in p['unified_source']:
        income = p['unified_source']['step_6']
    else:
        return (0)
    kk = income.keys()
    income_list = []
    total_cost = 0
    for k in kk:
        item = income[k]
        if 'costDate' in item:
            total_cost += int(item['costDate'])
    return(total_cost)


def download_data(reg):
	region = str(reg)
	print('here')
	data = []
	r = requests.get("https://declarations.com.ua/search?q=суддя&deepsearch=on&declaration_year%5B%5D=2019&region_value%5B%5D" + region + "&format=opendata").json()
	data += r["results"]["object_list"]
	for page in range(2, 5):
		subr = requests.get("https://declarations.com.ua/search?q=суддя&deepsearch=on&declaration_year%5B%5D=2019&region_value%5B%5D=" + region + "&format=opendata&page=%s" % page).json()
		data += subr["results"]["object_list"]
	new_df = []
	for p in data:
		new = {'guid':0}
		new['guid'] = p['guid']
		try:
			new['total_income'] = get_income(p)
		except KeyError:
			print('income' + p['guid'] + a)
		try:
			estate = get_estate(p)
			new['total_area'] = estate[0]
			new['estate_cost'] = estate[1]
		except KeyError :
			print('estate'+ p['guid'] + a)
		try:
			new['cost_cars'] = get_cars(p)
		except KeyError:
			print(p['guid'])
		new_df += [new]
	df = pd.DataFrame(new_df)
	
	return (df)


df = download_data(region)

app = dash.Dash("__main_PEP__")
regions = ["м.+Київ", "Львівська+область","Одеська+область"]
server = app.server
app.layout = html.Div([
    html.Div([
	dcc.Dropdown(id='group-select', options=[{'label': reg, 'value': reg} for  reg in regions],
                            value='м.+Київ', style={'width': '140px'})]),
     dcc.Graph('shot-dist-graph', config={'displayModeBar': False})])


@app.callback(
	dash.dependencies.Output('shot-dist-graph', 'figure'),
        [dash.dependencies.Input('group-select', 'value')])

def update_graph(reg):
	df = download_data(reg)
	return px.histogram(df, "total_income")
if __name__ == '__main__':
     app.run_server(debug=True, port=49091)

