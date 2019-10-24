import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)
@app.route("/")
def hawaii():
   """List all available api routes."""
   return (
       f"Available Routes:<br/>"
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs<br/>"
       )
@app.route("/api/v1.0/precipitation")
def precipitation():
   # Create our session (link) from Python to the DB
   session = Session(engine)
   """Return a list of all passenger names"""
   # Query all
   results = session.query(Measurement.date, Measurement.prcp).all()
   session.close()
   all_prcps = []
   for date, prcp in results:
       measurement_dict = {}
       measurement_dict["date"] = date
       measurement_dict["prcp"] = prcp
       all_prcps.append(measurement_dict)
   return jsonify(all_prcps)
@app.route("/api/v1.0/stations")
def stations():
   # Create our session (link) from Python to the DB
   session = Session(engine)
   """Return a list of passenger data including the name, age, and sex of each passenger"""
   # Query all passengers
   results = session.query(Station.name, Station.latitude, Station.longitude, Station.elevation).all()
   session.close()
   # Create a dictionary from the row data and append to a list of all_passengers
   all_stations = []
   for name, latitude, longitude, elevation in results:
       station_dict = {}
       station_dict["name"] = name
       station_dict["latitude"] = latitude
       station_dict["longitude"] = longitude
       station_dict["elevation"] = elevation
       all_stations.append(station_dict)
   return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query all tobs
    tobs_results = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date.between('2016-08-01', '2017-08-01')).all()
    
    tobs_list=[]
    for tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["station"] = tobs[0]
        tobs_dict["tobs"] = float(tobs[1])
       
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)


if __name__ == '__main__':
   app.run(debug=True)