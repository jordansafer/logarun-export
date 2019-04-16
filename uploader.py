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

def get_duration(ts):
  t = datetime.strptime(ts, "%H:%M:%S")
  td = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
  return int(td.total_seconds())

def get_meters(dist, units):
  if (units.startswith("Kilo")):
    return dist * 1000
  elif (units.startswith("Meter")):
    return dist
  else: # miles
    return dist * 1609.344

def main():

    # Creating a log file and a logging function
    log = open("log.txt","a+")
    now = str(datetime.now())
    def logger (message):
        log.write(now + " | " + message + "\n")
        print(message)

    # Opening the connection to Strava
    logger("Connecting to Strava")
    client = Client()

    # You need to run the strava_local_client.py script - with your application's ID and secret - to generate the access token.
    access_token = "ebdaaf4293b002c782fd56c0b90720d3c605ae86" # replace this with your token
    client.access_token = access_token
    athlete = client.get_athlete()
    logger("Now authenticated for " + athlete.firstname + " " + athlete.lastname)
           
    # We open the cardioactivities CSV file and start reading through it
    with open('logarun_export_20140601_20190415.json') as f:
        days = json.load(f)
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
                if (not act['type'].startswith('Run')):
                    continue
                logger("Manually uploading " + date)
                duration = get_duration(act['Time']) # time in seconds
                dist = get_meters(float(act['Distance']), act['Units'])

                # extra
                shoes = act['Shoes']
           
                try:
                    upload = client.create_activity(
                        name = title,
                        start_date_local = date + "T00:00:00Z",
                        elapsed_time = duration,
                        distance = dist,
                        description = note + "\n Shoes: " + shoes,
                        activity_type = "Run"
                    )
                    
                    logger("Manually created " + date)
                    activity_counter += 1

                except ConnectionError as err:
                    logger("No Internet connection: {}".format(err))
                    exit(1)
                note = "" # hack so note isn't repeated for doubles

        logger("Complete! Logged " + str(activity_counter) + " activities.")

if __name__ == '__main__':
    main()

