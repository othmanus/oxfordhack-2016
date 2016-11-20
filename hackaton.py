import requests
import json


API = "ha348334469154725681039185711735"
url = "http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/GB/{}/EN/?query={}&apikey={}"
start = input('Enter start location: ')
dest = input('Enter destination: ')
depature_date = input('Enter depature date in the format yyyy-mm-dd: ')
arrival_date = input('Enter arrival date in the format yyyy-mm-dd: ')
cur = input('Enter currency: ')

location_start = json.loads(requests.get(url.format(cur,start, API)).text)
location_id_start = location_start["Places"][0]['CityId']

location_dest = json.loads(requests.get(url.format(cur,dest, API)).text)
location_id_dest = location_dest["Places"][0]['CityId']
#print ("LOCATIONS")
#print (json.dumps(locations,indent = 4))

url_2 = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/GB/{}/en-GP/{}/{}/{}/{}?apiKey={}"
prices = json.loads(requests.get(url_2.format(cur,location_id_start, location_id_dest, depature_date, arrival_date, API)).text)

mincost = []
for x in range(0,len(prices["Quotes"])):
    mincost.append([x,prices["Quotes"][x]['MinPrice']])
if not mincost:
    print("No flights found")
    exit(0)
else:
    print ("The costs of the tickets are: %s" % sorted(mincost))

car = []
for x in range(0,len(prices["Carriers"])):
    car.append(prices["Carriers"][x]['CarrierId'])
    car.append(prices["Carriers"][x]['Name'])

info = input('For more info on the flight enter the reference number of the price: ')
if 'OutboundLeg' in prices["Quotes"][int(info)]:
    p = prices["Quotes"][int(info)]['OutboundLeg']['CarrierIds']
else:
    p = prices["Quotes"][int(info)]['InboundLeg']['CarrierIds']

carrier_find = car.index(p[0])
carrier = car[carrier_find+1]

#print(json.dumps(prices["Quotes"][int(info)],indent = 4))
print ("\nMore information for flight from %s to %s:" % (start, dest))
print("Depature Date: %s"%(depature_date))
print("Return Date: %s"%(arrival_date))
print("Direct: %s"%(prices["Quotes"][int(info)]['Direct']))
print("Price: %s %s "%(cur, mincost[int(info)][1]))
print("Airlines: %s"%carrier)
