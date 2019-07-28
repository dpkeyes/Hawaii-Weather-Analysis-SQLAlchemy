import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, text, and_

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"<h1>Welcome to David's Super Duper Weather API!</h1>"
        f"<h2>Available Routes:</h2>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/startdate</br>"
        f"/api/v1.0/startdate/enddate</br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation dictionary as json"""
    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.prcp).\
                    order_by(Measurement.date).all()

    precipitation = {}
    for i in range(len(results)):
        precipitation.update({results[i][0]: results[i][1]})

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """Return the stations list as json"""
    session = Session(engine)

    stations = session.query(Station.station, Station.name).order_by(Station.station).all()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return list of temperature observations as json"""
    session = Session(engine)

    # Pull the last date as the end date from the measurement table and convert it to a datetime object
    end_date = session.query(Measurement.date).\
            order_by(Measurement.date.desc()).first()[0]
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')

    # Define the date one year prior as the start date
    start_date = dt.datetime(end_date.year - 1, end_date.month, end_date.day)

    # Query for the last 12 months of temperature data
    tobs = session.query(Measurement.date, Measurement.tobs).\
                    filter(and_(Measurement.date >= start_date, Measurement.date <= end_date)).\
                    order_by(Measurement.date).all()

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return list tmin, tavg, tmax for given start or start-end range as json"""
    session = Session(engine)

    canonicalized = start.replace(" ", "")

    available_dates = session.query(Measurement.date).\
                        distinct().all()
    available_dates = np.ravel(available_dates)

    summary_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= canonicalized).all()[0]

    if canonicalized in available_dates:
        return jsonify(summary_results)
    else:
        return jsonify({"error": f"We don't have data for the date: {start}"}), 404

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return list tmin, tavg, tmax for given start or start-end range as json"""
    session = Session(engine)

    canonicalized_start = start.replace(" ", "")
    canonicalized_end = end.replace(" ", "")

    available_dates = session.query(Measurement.date).\
                        distinct().all()
    available_dates = np.ravel(available_dates)

    summary_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= canonicalized_start).\
                        filter(Measurement.date <= canonicalized_end).all()[0]

    if (canonicalized_start in available_dates and canonicalized_end in available_dates) and canonicalized_start <= canonicalized_end:
        return jsonify(summary_results)
    elif (canonicalized_start in available_dates and canonicalized_end in available_dates) and canonicalized_start > canonicalized_end:
        return jsonify({"error": f"Your start date {start} must be earlier than your end date {end}"}), 404
    else:
        return jsonify({"error": f"Your date range extends outside the dates in our dataset, which goes from 2010-01-01 to 2017-08-24"}), 404

if __name__ == "__main__":
    app.run(debug=True)
