import json 
import csv 
import pandas as pd
import os
import datetime

df = pd.read_json("https://pomber.github.io/covid19/timeseries.json")
# data.to_csv('output.csv', index=False)
# with open("output.csv", "rb") as f:
#     reader = csv.reader(f)
#     countriesNames = reader.next()
#     rest = [row for row in reader]

# os.remove('output.csv')

# for i in countriesNames:
# 	countryData = data[i]
# 	name = "/home/prateek/Documents/Covid Prediction Website/Test1/Files/" + str(i) + ".csv"
# 	print(name)
# 	data_file = open(name, 'w') 
	 
# 	csv_writer = csv.writer(data_file) 

# 	count = 0
# 	for datewiseData in countryData: 
# 		if count == 0: 
# 			header = datewiseData.keys() 
# 			csv_writer.writerow(header) 
# 			count += 1 
# 		csv_writer.writerow(datewiseData.values()) 

# 	data_file.close()

shape = df.shape
df_india_json = df.loc[shape[0]-1, 'India']
df_india_json_1 = df.loc[shape[0]-2, 'India']

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

print(confirmedIn)