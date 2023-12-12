# Import the dependencies.
import os
import numpy as np
import pandas as pd
import datetime as datetime
import sqlalchemy
import sqlite3
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
#create an app
app = Flask(__name__)

@app.route("/")
def home():
    print("Climate App")
    return (
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>"
    f"/api/v1.0/<start>/<end><br/>"
    )

#################################################
# Flask Routes
#################################################
# Create Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

#Retrive precipitation data for last 12 months
    yearprcp = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= "2016-08-24").filter(Measurement.date <= "2017-08-23").all()

#Convert list of tuples to a dictionary
    prcp_dict = {} 
    for date, prcp in yearprcp:
        prcp_dict[date] = prcp
    
#Convert the dictionary to JSON
    return jsonify(prcp_dict)

#Create Stations Route
@app.route("/api/v1.0/stations")
def stations(): 
    session = Session(engine)
    
    stations_query = session.query(Station.id, Station.name).all()

#Convert list to a dictionary
    station_list = []
    for station in stations_query:
        station_dict = {}
        station_dict["id"] = station[0]
        station_dict["name"] = station[1]
        station_list.append(station_dict)

    session.close()

    return jsonify(station_list)

#Create tobs Route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
     
#Query for most active station
    try:
        most_active_station = session.query(Measurement.station, func.count(Measurement.station).label\
                    ('station_count')).group_by(Measurement.station).order_by(desc('station_count')).\
                    first()[0]
    
        if most_active_station:
            most_active_station = most_active_station[0]

#Query for temperature statistics for the most active station
            temperature_stats = session.query(func.min(Measurement.tobs).label('lowest_temperature'),
                                      func.max(Measurement.tobs).label('highest_temperature'),
                                      func.avg(Measurement.tobs).label('average_temperature'))\
                    .filter(Measurement.station == most_active_station).first()

#Query for Previous 12 months

            recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
            last_date = session.query(func.max(Measurement.date)).scalar()
            most_recent_date = datetime.datetime.strptime(last_date, '%Y-%m-%d') - datetime.timedelta(days=365)

            results = session.query(Measurement.tobs).filter(Measurement.date.between\
                    (most_recent_date,last_date),Measurement.station == 'USC00519281').all()

            session.close()

#Prepare the result as a dictionary
            result = {
        'temperature_statistics': {
            'lowest_temperature': temperature_stats.lowest_temperature,
            'highest_temperature': temperature_stats.highest_temperature,
            'average_temperature': temperature_stats.average_temperature
        },
        'temperature_results': results
    }
            return jsonify(result)
        else:
            return jsonify({'error': 'No data available to calculate most active station'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Create start date and end date

@app.route('/api/temp_stats/<start>', defaults={'end': None}, methods=['GET'])
@app.route('/api/temp_stats/<start>/<end>', methods=['GET'])
def temperature_stats(start, end=None):
    try:
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d') if end else None 
        
        if end_date:
            temp_stats = session.query(func.min(Measurement.tobs).label('TMIN'),
                                       func.avg(Measurement.tobs).label('TAVG'),
                                       func.max(Measurement.tobs).label('TMAX')) \
                .filter(Measurement.date.between(start_date, end_date)).all()
        else:
            temp_stats = session.query(func.min(Measurement.tobs).label('TMIN'),
                                       func.avg(Measurement.tobs).label('TAVG'),
                                       func.max(Measurement.tobs).label('TMAX')) \
                .filter(Measurement.date >= start_date).all()
            
            temp_stats_dict = {'TMIN': temp_stats[0][0], 'TAVG': temp_stats[0][1], 'TMAX': temp_stats[0][2]}

# Return as Json
            return jsonify(temp_stats_dict)

    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

if __name__ == '__main__':
    app.run(debug=True)