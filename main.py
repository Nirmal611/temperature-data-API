from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

stations = pd.read_csv('data_small/stations.txt', skiprows=17)
stations = stations[['STAID', 'STANAME                                 ']]
@app.route('/')
def home():
    return render_template('home.html', data = stations.to_html())


@app.route('/<station_id>/<date>/')
def weather_data(station_id,date):
    filename = "data_small/TG_STAID"+str(station_id).zfill(6)+".txt"
    df = pd.read_csv(filename , skiprows=20 , parse_dates=['    DATE'])

    df['TG'] = df['   TG'].mask(df['   TG'] == -9999 , np.nan)/10
    df['year'] = df['    DATE'].dt.year
    df['month'] = df['    DATE'].dt.month

    temperature = df.loc[df['    DATE'] == date]['TG'].squeeze()
    year = date.split('-')[0]
    month = date.split('-')[1]

    year_mean = df.loc[df['year'] == int(year)]['TG'].mean()
    month_mean = df.loc[(df['year'] == int(year)) & (df['month'] == int(month))]['TG'].mean()

    df2= pd.read_csv('data_small/stations.txt', skiprows=17)
    station = df2.loc[df2['STAID'] == int(station_id)]['STANAME                                 '].squeeze()

    return {'station_id':station_id, 'station': station, 'date': date, 'temperature': temperature ,
            'year_mean': year_mean, 'month_mean': month_mean}

if __name__ == '__main__':
    app.run(debug=True)