#JOEY ASHCROFT
#code to create APIs for data quieries related to precipitation, stations, and temperature

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return a list of all precipation scores for the last 12 months"""
    #get the date
    last_date=session.query(func.max(Measurement.date)).scalar()
    #parse the date
    from dateutil.parser import parse
    last_date=parse(last_date)
    #date from a year ago
    year_ago=dt.date(last_date.year-1, last_date.month, last_date.day)

    # Perform a query to retrieve the data and precipitation scores
    prcp_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    # Convert list of tuples into normal list
    precip = list(np.ravel(prcp_scores))

    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations and how many of each"""
    station_list = session.query(Measurement.station, func.count(Measurement.station)).\
                group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    
    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_list))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():

    #get the date
    last_date=session.query(func.max(Measurement.date)).scalar()
    #parse the date
    from dateutil.parser import parse
    last_date=parse(last_date)
    #date from a year ago
    year_ago=dt.date(last_date.year-1, last_date.month, last_date.day)

    """Return a list of stations and how many of each"""
    temp_data=session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= year_ago).all()
    
    # Convert list of tuples into normal list
    temp_data = list(np.ravel(temp_data))

    return jsonify(temp_data)


@app.route("/api/v1.0/<start>")
def start_date(start):
    data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    data = list(np.ravel(data))
    return jsonify(data)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    data = list(np.ravel(data))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
