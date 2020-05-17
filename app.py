from flask import Flask, render_template, Markup, url_for, request, redirect, send_file
from werkzeug.exceptions import HTTPException
import requests
import json
import csv
import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import urllib, json
import datetime
import os
import unicodedata
import math

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
	df = pd.read_csv('https://docs.google.com/spreadsheets/d/1Ak0bZT-2KqIFLeIO8AqnlaTJeTblfopzMDGrRUtDUvg/export?format=csv')
	df.to_csv('covid-19_india_data.csv', index=False)
	if request.method == "GET":
		df = pd.read_json("https://pomber.github.io/covid19/timeseries.json")
		shape = df.shape
		df_india_json = df.loc[shape[0]-1, 'India']
		df_india_json_1 = df.loc[shape[0]-2, 'India']

		df_india = pd.DataFrame.from_dict(df_india_json, orient="index")
		df_india_1 = pd.DataFrame.from_dict(df_india_json_1, orient="index")

		lastUpdateIn = df_india.iloc[0,0]
		lastUpdateIn = datetime.datetime.strptime(lastUpdateIn, "%Y-%m-%d").strftime("%d/%m/%Y")
		lastUpdateGlo = lastUpdateIn

		confirmedIn = df_india.iloc[1,0]
		recoveredIn = df_india.iloc[3,0]
		deathsIn = df_india.iloc[2,0]
		activeIn = confirmedIn - recoveredIn - deathsIn

		incConfIn = confirmedIn - df_india_1.iloc[1,0]
		incRecovIn = recoveredIn - df_india_1.iloc[3,0]
		incDeaIn = deathsIn - df_india_1.iloc[2,0]

		filename = "covid-19_india_data.csv"
		data = pd.read_csv(filename)
		states = data['States']

		return render_template('home.html', lastUpdateIn=lastUpdateIn, lastUpdateGlo=lastUpdateGlo,
			confirmedIn=confirmedIn, activeIn=activeIn, recoveredIn=recoveredIn, deathsIn=deathsIn,
			incConfIn=incConfIn, incRecovIn=incRecovIn, incDeaIn=incDeaIn,
			column_names=states[1:len(states)])

	else:
		selectedState = request.form['stateName']

		df = pd.read_json("https://pomber.github.io/covid19/timeseries.json")
		shape = df.shape
		df_india_json = df.loc[shape[0]-1, 'India']
		df_india_json_1 = df.loc[shape[0]-2, 'India']

		df_india = pd.DataFrame.from_dict(df_india_json, orient="index")
		df_india_1 = pd.DataFrame.from_dict(df_india_json_1, orient="index")

		lastUpdateIn = df_india.iloc[0,0]
		lastUpdateIn = datetime.datetime.strptime(lastUpdateIn, "%Y-%m-%d").strftime("%d/%m/%Y")
		lastUpdateGlo = lastUpdateIn

		confirmedIn = df_india.iloc[1,0]
		recoveredIn = df_india.iloc[3,0]
		deathsIn = df_india.iloc[2,0]
		activeIn = confirmedIn - recoveredIn - deathsIn

		incConfIn = confirmedIn - df_india_1.iloc[1,0]
		incRecovIn = recoveredIn - df_india_1.iloc[3,0]
		incDeaIn = deathsIn - df_india_1.iloc[2,0]

		filename = "covid-19_india_data.csv"
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

		df_table = data
		df_table_state = df_table.iloc[index]
		# print(type(df_table_state))
		df_table_state = df_table_state.to_dict()
		# print(df_table_state)

		df = pd.DataFrame.from_dict(df_table_state, orient='index')
		df = df.transpose()
		df = df.rename(columns = {'States':'Dates'})
		df['Dates'] = ['Cases']
		# print(df.columns)

		col_names = ['Actual', 'Predicted', 'Error(%)']
		index_names = ['30th April', '1st May', '2nd May', '3rd May', '4th May', '5th May', 
						'6th May', '7th May', '8th May', '9th May', '10th May', '11th May',
						'12th May', '13th May', '14th May', '15th May', '16th May', '17th May', 
						'18th May', '19th May', '20th May', '21st May', '22nd May', '23rd May']
		startDate = 8
		endDate = 18
		df_styletable = pd.DataFrame({}, columns=col_names, index=index_names[startDate:endDate])

		for i in range(startDate, endDate):
			actualVal_string = str(index_names[i]) + '(Actual)'
			predictedVal_string = str(index_names[i]) + '(Predicted)'
			
			actualVal = float(df[actualVal_string].values)
			predictedVal = float(df[predictedVal_string].values)
			if math.isnan(actualVal)==False and math.isnan(predictedVal)==False:
				error = (predictedVal-actualVal)*100/predictedVal
			else:
				error = float("NaN")

			df_styletable.iloc[i-startDate,0] = actualVal if actualVal%1 else int(actualVal)
			df_styletable.iloc[i-startDate,1] = predictedVal if predictedVal%1 else int(predictedVal)
			df_styletable.iloc[i-startDate,2] = error
		
		df_styletable.fillna('Awaited', inplace=True)
		
		# def color_negative_red(value):
		#   if value < 0:
		#     color = 'red'
		#   elif value > 0:
		#     color = 'green'
		#   else:
		#     color = 'black'
		#   return 'color: %s' % color
		# style = df_styletable.style.applymap(color_negative_red, subset=['Error(%)'])

		# df_styletable.to_html('table.html')
		# with open('table.html', 'w') as html:
		# 	html.write(style.render())
		
		table = df_styletable.to_html(index=True, col_space='5', justify='center')
		df_styletable.to_html().replace('border="1"','border="0"')

	    # Available Font Families: "Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", 
	    # "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", 
	    # "PT Sans Narrow", "Raleway", "Times New Roman".
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=stateData_actual['States'], 
			y=stateData_actual[stateData_actual.columns[index+1]], 
			mode='lines+markers', name='Actual',
			line=dict(color='royalblue', width=2)))
		fig.add_trace(go.Scatter(x=stateData_predicted['States'], 
			y=stateData_predicted[stateData_predicted.columns[index+1]],
			mode='lines+markers', name='Predicted',
			line=dict(color='firebrick', width=2, dash='dashdot')))

		fig.update_xaxes(visible=True, title_text="Date", title_standoff = 5,
            title_font=dict(size=18, family='Sans-Serif', color='black'),
            ticks="outside", tickangle=0, tickfont=dict(family='Rockwell', color='black', size=14),
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
            legend=dict(x=0.6, y=1.2, traceorder="normal",
                font=dict(family="Courier New, monospace", size=12, color="black"),
                bgcolor="whitesmoke", bordercolor="Black", borderwidth=2),
            width=700,
	        height=450,
            plot_bgcolor='#C0C0C0',
	      	paper_bgcolor= '#C0C0C0',
            )
		config = {'responsive': True}
		div = fig.to_html(full_html=False, config=config)
		
		return render_template('chart.html', lastUpdateIn=lastUpdateIn, lastUpdateGlo=lastUpdateGlo,
			confirmedIn=confirmedIn, activeIn=activeIn, recoveredIn=recoveredIn, deathsIn=deathsIn,
			incConfIn=incConfIn, incRecovIn=incRecovIn, incDeaIn=incDeaIn,
			column_names=states[1:len(states)],
			div=Markup(div), table=Markup(table))
        
@app.route('/info')
def info():
	return render_template('info.html')

@app.route('/about')
def aboutus():
	return render_template('about.html')

@app.errorhandler(404)
def not_found(e):
	return render_template("error_page.html", errorCode='404')

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return render_template("error_page.html", e=e, errorCode='500'), 500

if __name__ == '__main__':
    app.run(debug=True)