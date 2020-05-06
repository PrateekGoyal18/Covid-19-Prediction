import csv
import pandas as pd
import plotly.express as px

# filename = "covid_30 - covid_30.csv"
# data = pd.read_csv(filename)
# data.set_index("States")

# index = data[data["States"]=="Delhi"].index.values
# index = int(index)

# stateNames = data['States'].tolist()

# items = dict()
# actual = pd.DataFrame(items)
# predicted = pd.DataFrame(items)

# actual['States'] = stateNames
# predicted['States'] = stateNames

# for col_name in data.columns:
# 	if(col_name.find("Actual")>=0):
# 		actual[col_name] = data[col_name]
# 	elif(col_name.find("Predicted")>=0):
# 		predicted[col_name] = data[col_name]

# actual = actual.transpose()
# predicted = predicted.transpose()

# actual.to_csv('actual.csv', header=False)
# stateData_actual = pd.read_csv('actual.csv')
# fig = px.line(stateData_actual, x='States', y=stateData_actual.columns[index+1])
# fig.show()

# data = pd.read_csv('state_wise.csv')
# data.set_index('State')
# data_total = data.head(1)
# print(data_total['Confirmed'])

filename = "covid_30 - covid_30.csv"
data = pd.read_csv(filename)
print(data)
data.set_index("States")
print(data)
index = data[data["States"]=='Delhi'].index.values
print(index)
index = int(index)
print(index)
stateNames = data['States'].tolist()
items = dict()
actual = pd.DataFrame(items)
predicted = pd.DataFrame(items)