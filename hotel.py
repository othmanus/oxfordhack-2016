import requests
import json

API_KEY="ha348334469154725681039185711735"
entityid="27544008" #input("Enter Location: ")
checkindate= input("Check-in: ")
checkoutdate=input("Check-out: ")
guests=input("No. of guests: ")
rooms=input("No. of rooms: ")

URL= "http://partners.api.skyscanner.net/apiservices/hotels/liveprices/v2/UK/GBP/en-GB/{}/{}/{}/{}/{}?apiKey={}&pageSize=20"
res = requests.get(URL.format(entityid,checkindate,checkoutdate,guests,rooms,API_KEY))

session = "http://partners.api.skyscanner.net" + res.headers['location']

filt = requests.get(session + "&price={}".format("0-200")).json()
agents = filt["agents"]
match = []

available = filt["total_available_hotels"]
hotel_hash = {} # hash table

for agent in agents:
    hotel_hash[agent["id"]] = agent["name"]

hotel_prices = filt["hotels_prices"]

new_prices = {}

for price in hotel_prices:
    id = price["agent_prices"][0]["id"]
    if hotel_hash[id] in new_prices:
        new_prices[hotel_hash[id]].append(price["agent_prices"][0]["price_total"])
    else:
        new_prices[hotel_hash[id]] = [price["agent_prices"][0]["price_total"]]

print(new_prices)
