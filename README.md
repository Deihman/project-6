# UOCIS322 - Project 5 #
Brevet time calculator with MongoDB!

Author:     Calvin Stewart

Contact:    clownvant@icloud.com
        or
            cstewar2@uoregon.edu

## Overview

### Display is not working!

This is a python AJAX-based calculator that takes the distance of a 200km, 300km, 400km, 600km, or 1000km brevet, the brevet's start time, and the distance of a checkpoint and calculates the open and close times of the checkpoint.

The JQuery watches for the user to exit the form, then takes their input and displays the open and close times in the form `YYYY-MM-DDTH:mm`.

This version of the calculator adds `Submit` and `Display` buttons that are supposed to store and fetch the input data from a Mongo database. This version also adds a REST API to communitcate between the python backend and the mongo database. `Submit` is supposed to clear out the input fields, and `Display` is supposed to refill the input fields with the previously stored data.

## How to run

In the home directory of the project, run the following command to set up the docker images and run the calculator. The `--build` tag forces the container to rebuild, which will be helpful if you have an older version of this project on your system. You may add the `-d` flag if you want to disconnect docker's prompting from your terminal. 

```
docker-compose up --build
```

To connect to the calculator, open up your browser and go to `localhost:5001`. If you would like to  Play around with it as much as you want, and let me know if you find any issues.

If you haven't disconnected your terminal from the internal containers, hitting `Crtl+C` will stop the containers. It will leave the outside container still running, but the program will not run anymore.

To stop and disable every container in the project, type in the following command. 

```
docker-compose down
```

This will also stop the external container, killing the program entirely. 