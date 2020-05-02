from flask import Flask, render_template, Markup, url_for, request, redirect, send_file
import requests
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import urllib, json
import pandas as pd
import datetime

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
			countryData = data[i]
			name = "Files/" + str(i) + ".csv"
			print(name)
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
		# date_split = lastUpdateIn.split("-")
		# lastUpdateIn = date_split[2] + "/" + date_split[1] + "/" + date_split[0]
		lastUpdateIn = datetime.datetime.strptime(lastUpdateIn, "%Y-%m-%d").strftime("%d/%m/%Y")
		lastUpdateGlo = lastUpdateIn

		confirmedIn = df_india.iloc[1,0]
		recoveredIn = df_india.iloc[2,0]
		deathsIn = df_india.iloc[3,0]
		activeIn = confirmedIn - recoveredIn - deathsIn

		incConfIn = confirmedIn - df_india_1.iloc[1,0]
		incRecovIn = recoveredIn - df_india_1.iloc[2,0]
		incDeaIn = deathsIn - df_india_1.iloc[3,0]

	    # Available Font Families: "Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", 
	    # "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", 
	    # "PT Sans Narrow", "Raleway", "Times New Roman".

		fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
		div = fig.to_html(full_html=False)

		states = ["Cumulative", "Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh",
					"Goa", "Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand",
					"Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya",
					"Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu",
					"Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
					"Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli",
					"Daman and Diu","Lakshadweep","NCT Delhi","Puducherry"]

		return render_template('home.html', lastUpdateIn=lastUpdateIn, lastUpdateGlo=lastUpdateGlo,
			confirmedIn=confirmedIn, activeIn=activeIn, recoveredIn=recoveredIn, deathsIn=deathsIn,
			incConfIn=incConfIn, incRecovIn=incRecovIn, incDeaIn=incDeaIn,
			column_names=states,
			div=Markup(div))
			# confirmedGlo=confirmedGlo, recoveredGlo=recoveredGlo, deathsGlo=deathsGlo, 

	else:
		selectedState = request.form['stateName']

		df = pd.read_json("https://pomber.github.io/covid19/timeseries.json")
		shape = df.shape
		df_india_json = df.ix[shape[0]-1, 'India']
		df_india_json_1 = df.ix[shape[0]-2, 'India']

		df_india = pd.DataFrame.from_dict(df_india_json, orient="index")
		df_india_1 = pd.DataFrame.from_dict(df_india_json_1, orient="index")

		lastUpdateIn = df_india.iloc[0,0]
		# date_split = lastUpdateIn.split("-")
		# lastUpdateIn = date_split[2] + "/" + date_split[1] + "/" + date_split[0]
		lastUpdateIn = datetime.datetime.strptime(lastUpdateIn, "%Y-%m-%d").strftime("%d/%m/%Y")
		lastUpdateGlo = lastUpdateIn

		confirmedIn = df_india.iloc[1,0]
		recoveredIn = df_india.iloc[2,0]
		deathsIn = df_india.iloc[3,0]
		activeIn = confirmedIn - recoveredIn - deathsIn

		incConfIn = confirmedIn - df_india_1.iloc[1,0]
		incRecovIn = recoveredIn - df_india_1.iloc[2,0]
		incDeaIn = deathsIn - df_india_1.iloc[3,0]

	    # Available Font Families: "Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", 
	    # "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", 
	    # "PT Sans Narrow", "Raleway", "Times New Roman".

		fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
		div = fig.to_html(full_html=False)

		states = ["Cumulative", "Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh",
					"Goa", "Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand",
					"Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya",
					"Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu",
					"Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
					"Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli",
					"Daman and Diu","Lakshadweep","NCT Delhi","Puducherry"]
		
		return render_template('home.html', lastUpdateIn=lastUpdateIn, lastUpdateGlo=lastUpdateGlo,
			confirmedIn=confirmedIn, activeIn=activeIn, recoveredIn=recoveredIn, deathsIn=deathsIn,
			incConfIn=incConfIn, incRecovIn=incRecovIn, incDeaIn=incDeaIn,
			column_names=states,
			div=Markup(div))
        

if __name__ == '__main__':
    app.run(host='192.168.0.14', debug=True)