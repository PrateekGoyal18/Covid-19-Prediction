## Setup
~~~
git clone https://github.com/PrateekGoyal18/Covid-19-Prediction.git
cd Covid-19-Prediction
source env_test/bin/activate
pip install -r requirements.txt
python app.py
~~~
The server will start at [192.168.0.14:5000](http://192.168.0.14:5000)

## About

Shows a forecasting of India's coronvirus cases - cumulative and statewise.
- Data from [Johns Hopkins](https://github.com/CSSEGISandData/COVID-19) via https://github.com/pomber/covid19
- Data is updated once a day around 00:15 UTC (https://github.com/pomber/covid19/blob/master/.github/workflows/main.yml#L3)

## Built with

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Plotly](https://plotly.com/)
