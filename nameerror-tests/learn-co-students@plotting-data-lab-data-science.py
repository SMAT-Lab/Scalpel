import pandas
file_name = './cities.xlsx'
travel_df = pandas.read_excel(file_name)
cities = travel_df.to_dict('records')
cities
import plotly
plotly.offline.init_notebook_mode(connected=True)
# use offline mode to avoid initial registration
x_values = [cities[0]['City'], cities[1]['City'], cities[2]['City']]
y_values = [cities[0]['Population'], cities[1]['Population'], cities[2]['Population']]
trace_first_three_pops = {'x': x_values, 'y': y_values}
plotly.offline.iplot([trace_first_three_pops])
text_values = []
bar_trace_first_three_pops = {'type': 'bar', 'x': x_values, 'y': y_values, 'text': text_values}
bar_trace_first_three_pops['type'] # 'bar'
plotly.offline.iplot([bar_trace_first_three_pops])
area_values = None
bar_trace_first_three_areas = {'type': 'bar', 'x': [], 'y': [], 'text': []}
bar_trace_first_three_pops = {'type': 'bar', 'x': [], 'y': [], 'text': []}
plotly.offline.iplot([bar_trace_first_three_pops, bar_trace_first_three_areas])