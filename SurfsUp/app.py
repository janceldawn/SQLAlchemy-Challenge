import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# Create an app
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    """Returns json with the date as the key and the value as the precipitation"""
    # Query date and prcp
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary with date as the key and precipitation as the value
    all_prcp = []
    for date, prcp in results:
        date_prcp = {}
        date_prcp["date"] = date
        date_prcp["prcp"] = prcp
        all_prcp.append(date_prcp)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():

    """Return a JSON list of stations from the dataset"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
   
    # Query the dates and temperature observations of the most-active station for the previous year of data
    # Find previous year data
    
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the temperature for the most active station over the previous year
    year_tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year).all()
    
    # Create a dictionary
    stations_tobs = []
    for date, tobs in year_tobs:
         date_tobs = {}
         date_tobs["date"] = date
         date_tobs["tobs"] = tobs
         stations_tobs.append(date_tobs)
    
    return jsonify(stations_tobs)


@app.route("/api/v1.0/<start_date>")
def start(start_date):

     # Convert the query parameters to datetime objects
    start_date_q = dt.datetime.strptime(start_date, '%Y-%m-%d')

    # Query the temperature data for the specified date range
    temp_date = (
        session.query(
            func.min(Measurement.tobs).label('TMIN'),
            func.avg(Measurement.tobs).label('TAVG'),
            func.max(Measurement.tobs).label('TMAX')
            )
            .filter(Measurement.date >= start_date)
        )
    result = temp_date.one()
    
    # Create a dictionary with the temperature summary
    summary_dict = {'start_date_q': start_date,
            'TMIN': result.TMIN,
            'TAVG': result.TAVG,
            'TMAX': result.TMAX,
        }

        # Use Flask's jsonify to create a JSON response
    return jsonify(summary_dict)


@app.route("/api/v1.0/<start_date>/<end_date>")
def startend(start_date, end_date):
        

    # Convert the query parameters to datetime objects
    start_date_q = dt.datetime.strptime(start_date, '%Y-%m-%d')

    if end_date:
        end_date_q = dt.datetime.strptime(end_date, '%Y-%m-%d')
    else:
        # If end_date is not provided, use the start_date as the end_date
        end_date_q = start_date_q

    # Query the temperature data for the specified date range
    temp_date = (
        session.query(
            func.min(Measurement.tobs).label('TMIN'),
            func.avg(Measurement.tobs).label('TAVG'),
            func.max(Measurement.tobs).label('TMAX')
            )
            .filter(Measurement.date >= start_date)
            .filter(Measurement.date <= end_date)
        )
    result = temp_date.one()

    # Create a dictionary with the temperature summary
    summary_dict = {'start_date_q': start_date,
            'TMIN': result.TMIN,
            'TAVG': result.TAVG,
            'TMAX': result.TMAX,
            'end_date_q': end_date
        }

    # Use Flask's jsonify to create a JSON response
    return jsonify(summary_dict)



if __name__ == '__main__':
    app.run(debug=True)