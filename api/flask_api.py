"""
Brevets RESTful API
"""
import os
from flask import Flask
from flask_restful import Api
import logging
from mongoengine import connect
# You need to implement two resources: Brevet and Brevets.
# Uncomment when done:
from resources.brevet import BrevetResource
from resources.brevets import BrevetsResource

# Connect MongoEngine to mongodb
connect(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017/brevetsdb")

# Start Flask app and Api here:
app = Flask(__name__)
api = Api(app)

# Bind resources to paths here:
# api.add_resource(...)
api.add_resource(BrevetResource, "/api/brevet/<_id>")
api.add_resource(BrevetsResource, "/api/brevets")

app.debug = os.environ["DEBUG"]
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(os.environ["PORT"]))
    app.run(port=os.environ["PORT"], host="0.0.0.0")