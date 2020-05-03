from flask import Flask, render_template, Markup, url_for, request, redirect, send_file
import requests
import json
import csv
import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import urllib, json
import pandas as pd
import datetime
import os
import unicodedata

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "GET":
		df = pd.read_json("https://pomber.github.io/covid19/timeseries.json")

		df.to_csv('output.csv', index=False)
		with open("output.csv", "rb") as f:
			reader = csv.reader(f)
			countriesNames = reader.next()
			rest = [row for row in reader]
		os.remove('output.csv')

		for i in countriesNames:
			countryData = df[i]
			name = "Files/" + str(i) + ".csv"
			data_file = open(name, 'w') 
			 
			csv_writer = csv.writer(data_file) 

			count = 0
			for datewiseData in countryData: 
				if count == 0: 
					header = datewiseData.keys() 
					csv_writer.writerow(header) 
					count += 1 
				csv_writer.writerow(datewiseData.values())
			data_file.close()

		shape = df.shape
		df_india_json = df.ix[shape[0]-1, 'India']
		df_india_json_1 = df.ix[shape[0]-2, 'India']

		df_india = pd.DataFrame.from_dict(df_india_json, orient="index")
		df_india_1 = pd.DataFrame.from_dict(df_india_json_1, orient="index")

		lastUpdateIn = df_india.iloc[0,0]
		lastUpdateIn = datetime.datetime.strptime(lastUpdateIn, "%Y-%m-%d").strftime("%d/%m/%Y")
		lastUpdateGlo = lastUpdateIn

		confirmedIn = df_india.iloc[1,0]
		recoveredIn = df_india.iloc[2,0]
		deathsIn = df_india.iloc[3,0]
		activeIn = confirmedIn - recoveredIn - deathsIn

		incConfIn = confirmedIn - df_india_1.iloc[1,0]
		incRecovIn = recoveredIn - df_india_1.iloc[2,0]
		incDeaIn = deathsIn - df_india_1.iloc[3,0]

		filename = "covid_30 - covid_30.csv"
		data = pd.read_csv(filename)
		states = data['States']

		return render_template('home.html', lastUpdateIn=lastUpdateIn, lastUpdateGlo=lastUpdateGlo,
			confirmedIn=confirmedIn, activeIn=activeIn, recoveredIn=recoveredIn, deathsIn=deathsIn,
			incConfIn=incConfIn, incRecovIn=incRecovIn, incDeaIn=incDeaIn,
			column_names=states)
			# confirmedGlo=confirmedGlo, recoveredGlo=recoveredGlo, deathsGlo=deathsGlo, 

	else:
		text = request.form['stateName']
		selectedState = unicodedata.normalize('NFKD', text).encode('ascii','ignore')

		df = pd.read_json("https://pomber.github.io/covid19/timeseries.json")
		shape = df.shape
		df_india_json = df.ix[shape[0]-1, 'India']
		df_india_json_1 = df.ix[shape[0]-2, 'India']

		df_india = pd.DataFrame.from_dict(df_india_json, orient="index")
		df_india_1 = pd.DataFrame.from_dict(df_india_json_1, orient="index")

		lastUpdateIn = df_india.iloc[0,0]
		lastUpdateIn = datetime.datetime.strptime(lastUpdateIn, "%Y-%m-%d").strftime("%d/%m/%Y")
		lastUpdateGlo = lastUpdateIn

		confirmedIn = df_india.iloc[1,0]
		recoveredIn = df_india.iloc[2,0]
		deathsIn = df_india.iloc[3,0]
		activeIn = confirmedIn - recoveredIn - deathsIn

		incConfIn = confirmedIn - df_india_1.iloc[1,0]
		incRecovIn = recoveredIn - df_india_1.iloc[2,0]
		incDeaIn = deathsIn - df_india_1.iloc[3,0]

		filename = "covid_30 - covid_30.csv"
		data = pd.read_csv(filename)
		data.set_index("States")
		index = data[data["States"]==selectedState].index.values
		index = int(index)
		stateNames = data['States'].tolist()
		items = dict()
		actual = pd.DataFrame(items)
		predicted = pd.DataFrame(items)

		actual['States'] = stateNames
		predicted['States'] = stateNames
		for col_name in data.columns:
			if(col_name.find("Actual")>=0):
				actual[col_name[:-8]] = data[col_name]
			elif(col_name.find("Predicted")>=0):
				predicted[col_name[:-11]] = data[col_name]
		actual = actual.transpose()
		predicted = predicted.transpose()
		actual.to_csv('actual.csv', header=False)
		stateData_actual = pd.read_csv('actual.csv')
		predicted.to_csv('predicted.csv', header=False)
		stateData_predicted = pd.read_csv('predicted.csv')
		
		data = pd.read_csv(filename)
		states = data['States']

	    # Available Font Families: "Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", 
	    # "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", 
	    # "PT Sans Narrow", "Raleway", "Times New Roman".
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=stateData_actual['States'], 
			y=stateData_actual[stateData_actual.columns[index+1]], 
			mode='lines+markers', name='Actual'))
		fig.add_trace(go.Scatter(x=stateData_predicted['States'], 
			y=stateData_predicted[stateData_predicted.columns[index+1]],
			mode='lines+markers', name='Predicted'))

		fig.update_xaxes(visible=True, title_text="Date", title_standoff = 5,
            title_font=dict(size=18, family='Sans-Serif', color='black'),
            ticks="outside", tickangle=45, tickfont=dict(family='Rockwell', color='black', size=14),
            tickwidth=2, tickcolor='black', ticklen=8, nticks = 8,
            showgrid=True, gridwidth=1, gridcolor='White',
            showline=True, linewidth=2, linecolor='black', mirror=False)

		fig.update_yaxes(visible=True, title_text="Confirmed Cases", title_standoff = 5,
            title_font=dict(size=18, family='Sans-Serif', color='black'),
            ticks="outside", tickangle=0, tickfont=dict(family='Rockwell', color='black', size=14),
            tickwidth=2, tickcolor='black', ticklen=8, nticks = 8,
            showgrid=True, gridwidth=1, gridcolor='White',
            showline=True, linewidth=2, linecolor='black', mirror=False)

		graphTitle = str(selectedState) + " Graph"
		fig.update_layout(
			title=dict(text=graphTitle, 
	            	font=dict(family='Times New Roman', size=25, color='#ff0000')),
			showlegend=True,
            legend_orientation="h",
            font=dict(size=14, family='Courier New, monospace', color='black'),
            legend=dict(title="<b> Parameters </b>", x=0.6, y=1.2, traceorder="normal",
                font=dict(family="Courier New, monospace", size=12, color="black"),
                bgcolor="whitesmoke", bordercolor="Black", borderwidth=2),
            width=800,
	        height=450,
            plot_bgcolor='#C0C0C0',
	      	paper_bgcolor= '#C0C0C0',
            )

		div = fig.to_html(full_html=False)
		
		return render_template('chart.html', lastUpdateIn=lastUpdateIn, lastUpdateGlo=lastUpdateGlo,
			confirmedIn=confirmedIn, activeIn=activeIn, recoveredIn=recoveredIn, deathsIn=deathsIn,
			incConfIn=incConfIn, incRecovIn=incRecovIn, incDeaIn=incDeaIn,
			column_names=states,
			div=Markup(div))
        

if __name__ == '__main__':
    app.run(host='192.168.0.14', debug=True)