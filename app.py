from flask import Flask, render_template, Markup, url_for, request, redirect, send_file
from werkzeug.exceptions import HTTPException
import requests
import json
import csv
import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pandas import DataFrame
import numpy as np
import urllib, json
from datetime import datetime
import pytz
import os
import unicodedata
import math

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
	dfs = pd.read_html('https://www.mohfw.gov.in/', header=0)
	for df in dfs:
	    print()
	df1 = df
	
	df1.drop(df1.tail(5).index,inplace=True)
	df1 = df1.drop(['Cured/Discharged/Migrated*','S. No.','Deaths**','Active Cases*'], axis=1)
	df1.rename(columns={'Name of State / UT': 'State', 'Total Confirmed cases*': 'Cases'}, inplace=True)
	df1 = df1[~df1.State.str.contains("Cases being reassigned to states", na=False)]
	df1['State'] = df1['State'].replace({'Dadar Nagar Haveli': 'Dadra and Nagar Haveli'})

	states_svg = {'State': ['Jammu and Kashmir','West Bengal','Uttarakhand','Uttar Pradesh','Tripura','Tamil Nadu','Telengana','Sikkim','Rajasthan','Puducherry','Punjab','Odisha','Nagaland','Mizoram','Madhya Pradesh','Manipur','Meghalaya','Maharashtra','Lakshadweep','Kerala','Karnataka','Ladakh','Jharkhand','Haryana','Himachal Pradesh','Gujarat','Goa','Dadra and Nagar Haveli','Delhi','Daman and Diu','Chhattisgarh','Chandigarh','Bihar','Assam','Arunachal Pradesh','Andhra Pradesh','Andaman and Nicobar Islands']}
	df2 = DataFrame(states_svg, columns= ['State'])
	df3=pd.merge(df2, df1, on="State")
	df4 = {'State': "Lakshadweep", 'Cases': 0}
	df5 = df3.append(df4, ignore_index=True)
	df4 = {'State': "Daman and Diu", 'Cases': 0}
	df5 = df5.append(df4, ignore_index=True)
	df6 = df5.reindex([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,35,18,19,20,21,22,23,24,25,26,27,36,28,29,30,31,32,33,34])
	df6.reset_index(drop=True)
	df6.to_csv('cases_svgformat.csv',index=False)
	cases_list = list(df6['Cases'])

	df = pd.read_excel("https://docs.google.com/spreadsheets/d/1Ak0bZT-2KqIFLeIO8AqnlaTJeTblfopzMDGrRUtDUvg/export?format=xlsx", sheet_name='Daily Data')
	df_weekahead = pd.read_excel("https://docs.google.com/spreadsheets/d/1Ak0bZT-2KqIFLeIO8AqnlaTJeTblfopzMDGrRUtDUvg/export?format=xlsx", sheet_name='Week Ahead')
	df.to_csv('covid-19_india_data.csv', index=False)
	df_weekahead.to_csv('week ahead data.csv', index=False)
	
	if request.method == "GET":
		url = 'https://www.mohfw.gov.in/'
		html = requests.get(url).content
		df_list = pd.read_html(html)
		df = df_list[-1]
		df_total = df.iloc[[37]]
		confirmedIn = df_total.iloc[0]['Total Confirmed cases*']
		activeIn = df_total.iloc[0]['Active Cases*']
		recoveredIn = df_total.iloc[0]['Cured/Discharged/Migrated*']
		deathsIn = df_total.iloc[0]['Deaths**']

		filename = "covid-19_india_data.csv"
		data = pd.read_csv(filename)
		states = data['States']

		return render_template('index.html',
			# , lastUpdateIn=lastUpdateIn, 
			confirmedIn=confirmedIn, activeIn=activeIn, recoveredIn=recoveredIn, deathsIn=deathsIn,
			# incConfIn=incConfIn, incRecovIn=incRecovIn, incDeaIn=incDeaIn, 
			column_names=states[1:len(states)], 
			cases_list=cases_list)

	else:
		selectedState = request.form['stateName']

		url = 'https://www.mohfw.gov.in/'
		html = requests.get(url).content
		df_list = pd.read_html(html)
		df = df_list[-1]
		df_total = df.iloc[[37]]
		confirmedIn = df_total.iloc[0]['Total Confirmed cases*']
		activeIn = df_total.iloc[0]['Active Cases*']
		recoveredIn = df_total.iloc[0]['Cured/Discharged/Migrated*']
		deathsIn = df_total.iloc[0]['Deaths**']

		filename = "covid-19_india_data.csv"
		weekahead_filename = "week ahead data.csv"
		data = pd.read_csv(filename)
		data_weekahead = pd.read_csv(weekahead_filename)
		states_weekahead = list(data_weekahead['States'])
		
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
		df_table_state = df_table_state.to_dict()

		df = pd.DataFrame.from_dict(df_table_state, orient='index')
		df = df.transpose()
		df = df.rename(columns = {'States':'Dates'})
		df['Dates'] = ['Cases']

		col_names = ['Actual', 'Predicted', 'Error(%)']
		index_names = ['30th April', '1st May', '2nd May', '3rd May', '4th May', '5th May', 
						'6th May', '7th May', '8th May', '9th May', '10th May', '11th May',
						'12th May', '13th May', '14th May', '15th May', '16th May', '17th May', 
						'18th May', '19th May', '20th May', '21st May', '22nd May', '23rd May',
						'24th May', '25th May', '26th May', '27th May', '28th May', '29th May',
						'30th May', '31st May', '1st June', '2nd June', '3rd June', '4th June',
						'5th June', '6th June', '7th June', '8th June', '9th June', '10th June',
						'11th June', '12th June']
						# '13th June', '14th June', '15th June',
						# '16th June', '17th June', '18th June', '19th June', '20th June', 
						# '21st June', '22nd June', '23rd June', '24th June', '25th June',
						# '26th June', '27th June', '28th June', '29th June', '30th June']
		startDate = 37
		endDate = 44
		df_errortable = pd.DataFrame({}, columns=col_names, index=index_names[startDate:endDate])

		for i in range(startDate, endDate):
			actualVal_string = str(index_names[i]) + '(Actual)'
			predictedVal_string = str(index_names[i]) + '(Predicted)'
			
			actualVal = float(df[actualVal_string].values)
			predictedVal = float(df[predictedVal_string].values)
			if math.isnan(actualVal)==False and math.isnan(predictedVal)==False:
				error = (predictedVal-actualVal)*100/predictedVal
			else:
				error = float("NaN")

			df_errortable.iloc[i-startDate,0] = actualVal if actualVal%1 else int(actualVal)
			df_errortable.iloc[i-startDate,1] = predictedVal if predictedVal%1 else int(predictedVal)
			df_errortable.iloc[i-startDate,2] = error
		df_errortable.fillna('Awaited', inplace=True)

		for state in states_weekahead:
			if state == selectedState:
				data_weekahead.set_index("States", inplace=True)
				list_weekahead = list(data_weekahead.loc[selectedState])
				df_errortable.insert(2, "Week Ahead Predictions", list_weekahead[startDate:endDate])
				df_errortable.rename(columns={"Predicted":"Daily Predictions", "Error(%)":"Daily Predictions Error(%)"}, inplace=True)
				df_errortable.insert(4, "Week Ahead Predictions Error(%)", list_weekahead[startDate:endDate])

				for i in range(7):
					actualVal = df_errortable.iloc[i,0]
					if actualVal != 'Awaited':
						actualVal = float(actualVal)
					predictedVal = df_errortable.iloc[i,2]
					if predictedVal != 'Awaited':
						predictedVal = float(predictedVal)
					if type(actualVal)==float and type(predictedVal)==float:
						error = (predictedVal-actualVal)*100/predictedVal
					else:
						error = 'Awaited'
					df_errortable.iloc[i,4] = error

				fig = go.Figure()
				fig.add_trace(go.Scatter(x=stateData_actual['States'], 
				y=stateData_actual[stateData_actual.columns[index+1]], 
				mode='lines+markers', name='Actual',
				line=dict(color='royalblue', width=2)))
				fig.add_trace(go.Scatter(x=stateData_predicted['States'], 
				y=stateData_predicted[stateData_predicted.columns[index+1]],
				mode='lines+markers', name='Daily Predictions',
				line=dict(color='firebrick', width=2, dash='dashdot')))
				fig.add_trace(go.Scatter(x=stateData_predicted['States'], 
					y=list(data_weekahead.loc[selectedState]),
					mode='lines+markers', name='Week Ahead Predictions',
					line=dict(color='green', width=2, dash='dot')))

				fig.update_xaxes(visible=True, title_text="Date", title_standoff = 5,
		            title_font=dict(size=18, family='Sans-Serif', color='black'),
		            ticks="outside", tickangle=-35, tickfont=dict(family='Rockwell', color='black'),
		            tickwidth=2, tickcolor='black', ticklen=8, nticks = 5,
		            showgrid=True, gridwidth=1, gridcolor='White',
		            showline=True, linewidth=2, linecolor='black', mirror=False)

				fig.update_yaxes(visible=True, title_text="Confirmed Cases", title_standoff = 5,
		            title_font=dict(size=18, family='Sans-Serif', color='black'),
		            ticks="outside", tickangle=0, tickfont=dict(family='Rockwell', color='black'),
		            tickwidth=2, tickcolor='black', ticklen=8, nticks = 8,
		            showgrid=True, gridwidth=1, gridcolor='White',
		            showline=True, linewidth=2, linecolor='black', mirror=False)

				graphTitle = str(selectedState) + " Graph"
				fig.update_layout(
					title=dict(text=graphTitle, 
			            	font=dict(family='Times New Roman', size=30, color='#ff0000')),
					showlegend=True,
		            legend_orientation="v",
		            font=dict(size=14, family='Courier New, monospace', color='black'),
		            legend=dict(x=0.4, y=1.25, traceorder="normal",
		                # font=dict(family="Courier New, monospace", size=12, color="black"),
		                # bgcolor="whitesmoke", bordercolor="Black", borderwidth=2
		                ),
		            plot_bgcolor='#C0C0C0',
			      	paper_bgcolor= '#C0C0C0',
		            )
				config = {'responsive': True}
				div = fig.to_html(full_html=False, config=config)
				table_type = 'Main state'
				break

			else:
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
		            ticks="outside", tickangle=-35, tickfont=dict(family='Rockwell', color='black'),
		            tickwidth=2, tickcolor='black', ticklen=8, nticks = 5,
		            showgrid=True, gridwidth=1, gridcolor='White',
		            showline=True, linewidth=2, linecolor='black', mirror=False)

				fig.update_yaxes(visible=True, title_text="Confirmed Cases", title_standoff = 5,
		            title_font=dict(size=18, family='Sans-Serif', color='black'),
		            ticks="outside", tickangle=0, tickfont=dict(family='Rockwell', color='black'),
		            tickwidth=2, tickcolor='black', ticklen=8, nticks = 8,
		            showgrid=True, gridwidth=1, gridcolor='White',
		            showline=True, linewidth=2, linecolor='black', mirror=False)

				graphTitle = str(selectedState) + " Graph"
				fig.update_layout(
					title=dict(text=graphTitle, 
			            	font=dict(family='Times New Roman', size=30, color='#ff0000')),
					showlegend=True,
		            legend_orientation="v",
		            font=dict(size=14, family='Courier New, monospace', color='black'),
		            legend=dict(x=0.5, y=1.17, traceorder="normal",
		                # font=dict(family="Courier New, monospace", size=12, color="black"),
		                # bgcolor="whitesmoke", bordercolor="Black", borderwidth=2
		                ),
		            plot_bgcolor='#C0C0C0',
			      	paper_bgcolor= '#C0C0C0',
		            )
				config = {'responsive': True}
				div = fig.to_html(full_html=False, config=config)
				table_type = 'Other state'
		
		df_errortable.fillna('Awaited', inplace=True)
		df_errortable.reset_index(inplace=True)
		df_errortable.rename(columns = {'index':'Dates'}, inplace=True)
		table = df_errortable.to_html(index=False, justify='center')
		
		return render_template('index.html', 
			# lastUpdateIn=lastUpdateIn, 
			confirmedIn=confirmedIn, activeIn=activeIn, recoveredIn=recoveredIn, deathsIn=deathsIn,
			 # incConfIn=incConfIn, incRecovIn=incRecovIn, incDeaIn=incDeaIn,
			  column_names=states[1:len(states)], div=Markup(div), table=Markup(table), table_type=table_type, cases_list=cases_list)
        
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
    app.run(host='192.168.0.15', debug=True)