from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import googlemaps
import requests
import datetime
import json

def index(request):
    context = {'name': 'index'}
    return render(request, "index.html", context)

def search(request):
    # Get the data
    origin = request.GET['origin']
    destination = request.GET['destination']
    mode = request.GET['mode']
    intervalType = request.GET['criteria']
    interval = int(request.GET['interval'])
    date_string = request.GET['date']
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    currency = "EUR"

    # ==========================================================================
    # Google Map API
    # Search for the directions and divide it by steps
    # ==========================================================================
    GOOGLE_API_KEY = 'AIzaSyAzKgY27NTR5LDPyR98AiCh39UcEWvFs7c'

    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

    '''
    the following inputs are required from the user as the format and type stated
        string mode = string "walking" or "driving"
        string intervalType = string "time" or "distance"

        string origin is input from user. It is the name of a city
        string destination is input from user. It is the name of a city
    '''

    departureTime = datetime.datetime.now()

    res = requests.get("https://maps.googleapis.com/maps/api/directions/json?origin="+origin+"&destination="+destination+"&mode="+mode+"&key="+GOOGLE_API_KEY)
    jsonOfRes = res.json()


    waypoints = []
    waypointCoords = []

    # if they want to split by distance
    if intervalType == "distance":
        distanceFromWaypoint = 0

        # distance is measured in metres
        distanceInterval = interval * 1000

        # add waypoints after every interval of distance
        for step in range(len(jsonOfRes[u'routes'][0][u'legs'][0][u'steps'])):
            distanceFromWaypoint += jsonOfRes[u'routes'][0][u'legs'][0][u'steps'][step][u'distance'][u'value']

            if distanceFromWaypoint >= distanceInterval:
                waypoints.append(jsonOfRes[u'routes'][0][u'legs'][0][u'steps'][step])
                distanceFromWaypoint = 0

    # if they want to split by time
    if intervalType == "time":
        timeFromWaypoint = 0

        # time is measured in seconds
        timeInterval = interval * 3600

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

    # return HttpResponse(str(jsonOfCoords['waypoints']))

    # ==========================================================================
    # Skyscanner API
    # Search for flight
    # ==========================================================================
    API = "ha348334469154725681039185711735"
    url = "http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/GB/{}/EN/?query={}&apikey={}"

    start = origin
    dest = destination
    depature_date = date_string
    end_date = date + datetime.timedelta(days=1)
    arrival_date = end_date.strftime("%Y-%m-%d")
    cur = currency

    # location_start = json.loads(requests.get(url.format(cur,start, API)).text)
    # location_id_start = location_start["Places"][0]['CityId']
    #
    # location_dest = json.loads(requests.get(url.format(cur,dest, API)).text)
    # location_id_dest = location_dest["Places"][0]['CityId']
    # #print ("LOCATIONS")
    # #print (json.dumps(locations,indent = 4))
    #
    # url_2 = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/GB/{}/en-GP/{}/{}/{}/{}?apiKey={}"
    # prices = json.loads(requests.get(url_2.format(cur,location_id_start, location_id_dest, depature_date, arrival_date, API)).text)
    #
    # msg = ""
    # mincost = []
    # for x in range(0,len(prices["Quotes"])):
    #     mincost.append([x,prices["Quotes"][x]['MinPrice']])
    # if not mincost:
    #     msg = "No flights found"
    #
    # car = []
    # for x in range(0,len(prices["Carriers"])):
    #     car.append(prices["Carriers"][x]['CarrierId'])
    #     car.append(prices["Carriers"][x]['Name'])
    #
    # info = input('For more info on the flight enter the reference number of the price: ')
    # if 'OutboundLeg' in prices["Quotes"][int(info)]:
    #     p = prices["Quotes"][int(info)]['OutboundLeg']['CarrierIds']
    # else:
    #     p = prices["Quotes"][int(info)]['InboundLeg']['CarrierIds']
    #
    # carrier_find = car.index(p[0])
    # carrier = car[carrier_find+1]

    #print(json.dumps(prices["Quotes"][int(info)],indent = 4))
    # print ("\nMore information for flight from %s to %s:" % (start, dest))
    # print("Depature Date: %s"%(depature_date))
    # print("Return Date: %s"%(arrival_date))
    # print("Direct: %s"%(prices["Quotes"][int(info)]['Direct']))
    # print("Price: %s %s "%(cur, mincost[int(info)][1]))
    # print("Airlines: %s"%carrier)

    # flight_direct = prices["Quotes"][int(info)]['Direct']
    # flight_price = mincost[int(info)][1] + cur
    # flight_airlines = carrier

    # ==========================================================================
    # Skyscanner API
    # Search for hotels in each step of the trip
    # ==========================================================================
    # hotels = {}

    hotels = []

    for point in range(len(parsedWaypoints)):
        lat = ("%.2f" % parsedWaypoints[point][u'lat'])
        lng = ("%.2f" % parsedWaypoints[point][u'long'])
        entityid=lat+","+lng+"-latlong" #input("Enter Location: ")
        checkindate= depature_date
        checkoutdate= arrival_date
        guests = 1
        rooms = 1

        URL= "http://partners.api.skyscanner.net/apiservices/hotels/liveprices/v2/UK/GBP/en-GB/{}/{}/{}/{}/{}?apiKey={}&pageSize=20"
        res = requests.get(URL.format(entityid,checkindate,checkoutdate,guests,rooms,API))

        session = "http://partners.api.skyscanner.net" + res.headers['location']

        filt = requests.get(session + "&price={}".format("0-200")).json()
        hs = filt["hotels"]

        hotels_hash = []
        for hotel in hs:
            hotel_id = hotel['hotel_id']
            hotel_name = hotel['name']
            hotel_lat = hotel['latitude']
            hotel_lng = hotel['longitude']

            hotels_hash.append([hotel_id, hotel_name, hotel_lat, hotel_lng])

        hotels.append(hotels_hash)
        # URL= "http://partners.api.skyscanner.net/apiservices/hotels/liveprices/v2/UK/GBP/en-GB/{}/{}/{}/{}/{}?apiKey={}&pageSize=20"
        # res = requests.get(URL.format(entityid,checkindate,checkoutdate,guests,rooms,API))
        #
        # session = "http://partners.api.skyscanner.net" + res.headers['location']
        #
        # filt = requests.get(session + "&price={}".format("0-200")).json()
        # agents = filt["agents"]
        # match = []
        #
        # available = filt["total_available_hotels"]
        # hotel_hash = {} # hash table
        #
        # for agent in agents:
        #     hotel_hash[agent["id"]] = agent["name"]
        #
        # hotel_prices = filt["hotels_prices"]
        #
        # new_prices = {}
        #
        # for price in hotel_prices:
        #     id = price["agent_prices"][0]["id"]
        #     if hotel_hash[id] in new_prices:
        #         new_prices[hotel_hash[id]].append(price["agent_prices"][0]["price_total"])
        #     else:
        #         new_prices[hotel_hash[id]] = [price["agent_prices"][0]["price_total"]]

        # hotels.append(new_prices)

    # ==========================================================================
    # Return the response
    # ==========================================================================
    context = {
        'name': 'search',
        'points': parsedWaypoints,
        'origin': origin,
        'destination': destination,
        'mode': mode,
        'criteria': intervalType,
        'interval': interval,
        'flight_direct': flight_direct,
        'flight_price': flight_price,
        'flight_airlines': flight_airlines,
    }
    # return render(request, "search.html", context)
    return HttpResponse(str(parsedWaypoints))
