import googlemaps
import requests
import datetime
import json

API_KEY = 'AIzaSyAzKgY27NTR5LDPyR98AiCh39UcEWvFs7c'

gmaps = googlemaps.Client(key=API_KEY)

'''
the following inputs are required from the user as the format and type stated
    string mode = string "walking" or "driving"
    string intervalType = string "time" or "distance"
    
    string origin is input from user. It is the name of a city
    string destination is input from user. It is the name of a city
'''

origin = "New York"
destination = "Toronto"
departureTime = datetime.datetime.now()
    
modeType = input ("Would you like to walk <1>, or go by car <2>?")

''' remove this if when using input from user '''
if modeType == 1:
    mode = "walking"
elif modeType == 2:
    mode = "driving"

res = requests.get("https://maps.googleapis.com/maps/api/directions/json?origin="+origin+"&destination="+destination+"&mode="+mode+"&key="+API_KEY)
jsonOfRes = res.json()

intervalNum = input ("Would you like to stop every few kilometres <1>, or every few hours <2>?")

intervalType = ""

''' remove this if when using input from the user '''
if intervalNum == 1:
    intervalType = "distance"
elif intervalNum == 2:
    intervalType = "time"
    
print "interval type " + intervalType

waypoints = []
waypointCoords = []

# if they want to split by distance
if intervalType == "distance":
    distanceFromWaypoint = 0  

    # distance is measured in metres
    distanceInterval = input("How far do you want to travel before you stop?")
   
    # add waypoints after every interval of distance
    for step in range(len(jsonOfRes[u'routes'][0][u'legs'][0][u'steps'])):
        distanceFromWaypoint += jsonOfRes[u'routes'][0][u'legs'][0][u'steps'][step][u'distance'][u'value']
        
        if distanceFromWaypoint >= distanceInterval:
            waypoints.append(jsonOfRes[u'routes'][0][u'legs'][0][u'steps'][step])
            distanceFromWaypoint = 0

# if they want to split by time
elif intervalType == "time":
    timeFromWaypoint = 0  

    # time is measured in seconds
    timeInterval = input("How long do you want to travel before you stop?") 
     
    # add waypoints after every interval of distance
    for step in range(len(jsonOfRes[u'routes'][0][u'legs'][0][u'steps'])):
        timeFromWaypoint += jsonOfRes[u'routes'][0][u'legs'][0][u'steps'][step][u'duration'][u'value']
        
        if timeFromWaypoint >= timeInterval:
            waypoints.append(jsonOfRes[u'routes'][0][u'legs'][0][u'steps'][step])
            timeFromWaypoint = 0
    

# store coordinates of each waypoint
for point in range(len(waypoints)):
    coordinates = {} #to hold latitude and longitude
    coordinates['lat'] = waypoints[point][u'start_location'][u'lat']
    coordinates['long'] = waypoints[point][u'start_location'][u'lng']
    coordinates['time'] = waypoints[point][u'duration'][u'value']
    waypointCoords.append(coordinates)

# convert coordinates to json    
jsonCoords = json.dumps({"waypoints":waypointCoords})

# get coordinates back from json file
jsonOfCoords = json.loads(jsonCoords)

parsedWaypoints = []

for waypoint in range(len(jsonOfCoords['waypoints'])):
    parsedWaypoints.append(jsonOfCoords['waypoints'][waypoint])
    
# print lat and long of each waypoint
for point in range(len(parsedWaypoints)):
    print "lat " + str(parsedWaypoints[point][u'lat']) + " long " + str(parsedWaypoints[point][u'long']) + " time " + str(parsedWaypoints[point][u'time'])