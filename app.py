from flask import Flask, jsonify

# Precipitation dictionary
precipitation = [
    {"superhero": "Aquaman", "real_name": "Arthur Curry"},
    {"superhero": "Batman", "real_name": "Bruce Wayne"},
]

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
        f"Welcome to David's Super Duper Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation dictionary as json"""

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """Return the stations list as json"""

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return list of temperature observations as json"""

    return jsonify(tobs)

# @app.route("/api/v1.0/<start>")
# def start_end():
#     """Return list tmin, tavg, tmax for given start or start-end range as json"""

#     return jsonify(start_end)

if __name__ == "__main__":
    app.run(debug=True)
