import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
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
       f"/api/v1.0/start<br/>"
       f"/api/v1.0/start/end")

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
       measurement_dict[date] = prcp
    
       all_prcps.append(measurement_dict)
   return jsonify(all_prcps)
   
@app.route("/api/v1.0/stations")
def stations():
   # Create our session (link) from Python to the DB
   session = Session(engine)

   # Query all passengers
   results = session.query(Station.station).all()

   return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query all tobs
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between('2016-08-01', '2017-08-01')).all()

    tobs_list=[]
    for tobs in tobs_results:
        tobs_dict = {}
        tobs_dict[tobs[0]] = float(tobs[1])
       
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def start(start):
    session = Session(engine)
 # Min/Avg/Max temp
    start_date=dt.date(2017,7,20)
    temp_range = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    session.close()
    temp = list(np.ravel(temp_range))
    
    return jsonify(temp)

@app.route("/api/v1.0/<start>/<end>")
def range(start,end):
    session = Session(engine)
    
  # Min/Avg/Max temp
    start_date=dt.date(2017,7,20)
    end_date= dt.date(2017,7,30)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date.between(start_date, end_date)).all()
    
    session.close()
    
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

if __name__ == '__main__':
   app.run(debug=True)