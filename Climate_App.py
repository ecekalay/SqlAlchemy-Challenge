import numpy as np
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

os.chdir(os.path.dirname(os.path.abspath(__file__)))
#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
sta = Base.classes.station

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
def prep():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    all_measurement = []
    for date, prcp in results:
        m_dict = {}
        m_dict["date"] = date
        m_dict["prcp"] = prcp
        all_measurement.append(m_dict)

    return jsonify(all_measurement) 

   
@app.route("/api/v1.0/stations")
def statit():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results2 = session.query(sta.name).all()
    
    session.close()

    all_stations = []
    for name in results2:
        s_dict = {}
        s_dict["station"] = name
        all_stations.append(s_dict)

    return jsonify(all_stations)    

@app.route("/api/v1.0/tobs")
def active():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results3 = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).first()
    
    session.close()

#    most_active = list(np.ravel(results3))
#    return results3

    return jsonify(results3)   

if __name__ == '__main__':
    app.run(debug=True)