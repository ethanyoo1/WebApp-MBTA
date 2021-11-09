
import requests
import urllib.parse
import json
import pprint


# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "e30nPNzznK8P3TqbAnGpG6NyjzJqSNvC"
MBTA_API_KEY = "7ec191c992ec48a382b280851422636e"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    # data = urllib.request.urlopen(url)
    # data = json.loads(data)
    # pprint.pprint(data)
    # params = {"key": MAPQUEST_API_KEY, "location": "Washington,DC"}
    r = requests.get(url)
    data = r.json()
    # pprint.pprint(data)
    return data

# get_json("http://www.mapquestapi.com/geocoding/v1/address")

def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    # parsed_location = urllib.parse.urlencode(place_name)
    url = f"http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={place_name}"
    data = get_json(url)

    
    latLng = data["results"][0]["locations"][0]["latLng"]
    return (latLng.get("lat"), latLng.get("lng"))
    

    

# latLng = get_lat_long("Needham,MA")


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    url = f"{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&page[limit]=1&filter[latitude]={latitude}&filter[longitude]={longitude}&sort=-distance"
    data = get_json(url)
    # pprint.pprint(data)
    
    station_name = data["data"][0]["attributes"]["name"]
    wheelchair_accessible = data["data"][0]["attributes"]["wheelchair_boarding"]


    if wheelchair_accessible == 0:
        wheelchair_accessible = "Accessible"
    else:
        wheelchair_accessible = "No access"
    return(station_name, wheelchair_accessible)

# print(get_nearest_station(latLng[0], latLng[1]))



def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    latLng = get_lat_long(place_name)
    if latLng is False:
        return ("There was an error", "There was an error")
    return get_nearest_station(latLng[0], latLng[1])


def main():
    """
    You can test all the functions here
    """
    print(find_stop_near("Needham,MA"))


if __name__ == '__main__':
    main()
