from pymongo import MongoClient

def store(brevet_dist_km, start_time, checkpoints, database):
    '''
    stores a dictionary in the specified database
    '''
    output = database.insert_one({
        "brevet_dist_km": brevet_dist_km,
        "start_time": start_time,
        "checkpoints": checkpoints
    })

    _id = output.inserted_id

    return str(_id)

def fetch(database):
    '''
    returns an object from the specified database in dictionary form
    '''
    brevets = database.find().sort("_id", -1).limit(1)

    for brevet in brevets:
        return brevet["brevet_dist_km"], brevet["start_time"], brevet["checkpoints"]
