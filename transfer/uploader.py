import os
from stravalib import Client, exc, model
from requests.exceptions import ConnectionError, HTTPError
import requests
import csv
import shutil
import time
import datetime as dt
from datetime import datetime, timedelta
import json
from strava_local_client import getToken

def get_duration(ts):
  t = datetime.strptime(ts, "%H:%M:%S")
  td = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
  return int(td.total_seconds())

def get_meters(dist, units):
  if (units.startswith("Kilo")):
    return dist * 1000
  elif (units.startswith("Meter")):
    return dist
  elif (units.startswith("Yard")):
    return dist * 0.9144
  else: # miles
    return dist * 1609.344

def get_activity(act):
  if (act.startswith("Bike")):
    return "Ride"
  elif (act.startswith("Exercise Bike")):
    return "EBikeRide"
  elif (act.startswith("Nordic" )):
    return "AlpineSki"
  else:
    return act

def is_uploadable(act):
  supported_activities = ["EBikeRide", "Ride", "AlpineSki", "Swim", \
    "Elliptical", "Run"]
  return act in supported_activities

def updateClient(client, c_id, secret):
    getToken(c_id, secret)
    new_token = access_token

    while new_token == access_token:
        # You need to run the strava_local_client.py script - with your application's ID and secret - to generate the access token.
        token_file = open("strava_access.txt", r+)
        new_token = token_file.read()
        time.sleep(1)
    
    #access_token = "3e4cc57201d5fcd71202003e1fbc1fed0da65b93" # replace this with your token
    
    client.access_token = access_token
    athlete = client.get_athlete()
    logger("Now authenticated for " + athlete.firstname + " " + athlete.lastname)
           

def uploadActivities(data, c_id, secret):

    # Creating a log file and a logging function
    log = open("log.txt","a+")
    now = str(datetime.now())
    def logger (message):
        log.write(now + " | " + message + "\n")
        print(message)

    # Opening the connection to Strava
    logger("Connecting to Strava")
    client = Client()
    updateClient(client, c_id, secret)
    
    # We open the cardioactivities CSV file and start reading through it
    days = data
    activity_counter = 0
    for day in days:
        if activity_counter >= 500:
            logger("Upload count at 500 - pausing uploads for 15 minutes to avoid rate-limit")
            time.sleep(900)
            activity_counter = 0
        note = day['note']
        date = day['date']
        title = day['title']
        for act in day['activities']:
            act_type = get_activity(act['type'])
            if (not is_uploadable(act_type)):
                continue
            logger("Manually uploading " + date)
            duration = get_duration(act['Time']) # time in seconds
            dist = get_meters(float(act['Distance']), act['Units'])

            # extra
            if (act_type.startswith("Run")):
                shoes = act['Shoes']
                extra = "\nShoes: " + shoes
            else:
                extra = ""
       
            try:
                upload = client.create_activity(
                    name = title,
                    start_date_local = date + "T00:00:00Z",
                    elapsed_time = duration,
                    distance = dist,
                    description = note + extra,
                    activity_type = act_type
                )
                
                logger("Manually created " + date)
                activity_counter += 1

            except ConnectionError as err:
                logger("No Internet connection: {}".format(err))
                exit(1)
            except:
                print("Lost authorization")
                updateClient(client, c_id, secret)
            note = "" # hack so note isn't repeated for doubles

    logger("Complete! Logged " + str(activity_counter) + " activities.")

if __name__ == '__main__':
    main()

