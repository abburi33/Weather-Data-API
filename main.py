from flask import Flask, render_template
import pandas as pd

data = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = data[['STAID', 'STANAME                                 ']]

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", data=stations.to_html())


@app.route('/api/v1/<station>/<date>')
def station_date(station, date):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df["    DATE"] == date]['   TG'].squeeze() / 10

    details = {
        "temperature": temperature,
        "station": station,
        "date": date
    }

    return details


@app.route('/api/v1/<station>/y/<year>')
def station_yearly(station, year):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    yearly_data = df.loc[df['    DATE'].dt.year == int(year)]
    return yearly_data.to_dict(orient="records")


@app.route('/api/v1/<station>')
def station_all_data(station):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    station_data = df.to_dict(orient='records')
    return station_data


if __name__ == "__main__":
    app.run(debug=True, port=5000)
