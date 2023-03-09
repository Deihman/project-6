"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
from pymongo import MongoClient
import pymongo_interface
import os

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
client = MongoClient("mongodb://" + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.brevet

mongo_brevets = db.brevets

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects three URL-encoded arguments: 
        control km: a checkpoint's distance
        brevet distance: the total distance of the brevet
        start time: the start time of the brevet
    """
    app.logger.debug("Got a JSON request: /_calc_times")
    km = request.args.get('km', 999, type=float)
    brevet_dist_km = request.args.get('brevet_dist_km', 200, type=float)
    start_time = request.args.get('start_time', '2021-01-01T00:00', type=str)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!

    start_time_arrow = arrow.get(start_time, 'YYYY-MM-DDTHH:mm')

    open_time = acp_times.open_time(km, brevet_dist_km, start_time_arrow).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist_km, start_time_arrow).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


@app.route("/_submit", methods=["POST"])
def _submit():
    """
    adds the current inputs to a mongo database "brevet"
    Expects three URL-encoded arguments:
        brevet_dist_km: the brevet's distance
        start_time:     the brevet's start time
        checkpoints:    a list of dictionaries containing 
                        the km and location name of each 
                        filled-in checkpoint
    returns a jsonified true value if it reaches the end
    """

    app.logger.debug("Got a POST request: /_submit")

    try:
        input_json = request.json
        app.logger.debug("request received properly")
        
        brevet_dist_km = input_json["brevet_dist_km"]
        start_time = input_json["start_time"]
        checkpoints = input_json["checkpoints"]
        app.logger.debug("Data assigned properly")

        checkpoint_id = pymongo_interface.store(brevet_dist_km, start_time, checkpoints, mongo_brevets)
        app.logger.debug("checkpoint id grabbed successfully")

        return flask.jsonify(
            result={}, 
            message="Inserted",
            status=1,
            mongo_id=checkpoint_id)

    except:
        return flask.jsonify(
            result={},
            message="Server error, not inserted",
            status=0,
            mongo_id='None')


@app.route("/_display")
def _display():
    """
    pulls the newest brevet data from mongo database 'brevet'
    and returns it to the HTML side of the project.
    """

    try:
        brevet_dist_km, start_time, checkpoints = pymongo_interface.fetch(mongo_brevets)
        return flask.jsonify(
            result={
                "brevet_dist_km": brevet_dist_km,
                "start_time": start_time,
                "checkpoints": checkpoints
            },
            status=1,
            message="Successfully fetched a brevet"
        )

    except:
        return flask.jsonify(
            result={},
            status=0,
            message="Something went wrong, couldn't fetch any brevets"
        )


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
