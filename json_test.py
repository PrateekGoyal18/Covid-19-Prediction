import json 
import csv 
import pandas as pd
import os

data = pd.read_json("https://pomber.github.io/covid19/timeseries.json")
data.to_csv('output.csv', index=False)
with open("output.csv", "rb") as f:
    reader = csv.reader(f)
    countriesNames = reader.next()
    rest = [row for row in reader]

os.remove('output.csv')

for i in countriesNames:
	countryData = data[i]
	name = "/home/prateek/Documents/Covid Prediction Website/Test1/Files/" + str(i) + ".csv"
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