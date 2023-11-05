from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import requests
import json
import random

UTC_RADIUS = 360
CAMPUS_PLAZA_RADIUS = 220
OUTSIDE_UCI_RADIUS = 10000
LIMIT = 50


app = Flask(__name__)
CORS(app)


def _parse(res: dict) -> list:
    '''Returns a list that only has the needed attributes of the locations'''
    copy_of_res = res.copy()

    needed_attributes = ['name', 'image_url', 'rating',
                         'price', 'location', 'display_phone', 'distance']
    for location in copy_of_res['businesses']:
        attributes_to_delete = []
        for attribute in location:
            if attribute not in needed_attributes:
                attributes_to_delete.append(attribute)
        for attribute in attributes_to_delete:
            del location[attribute]

    return copy_of_res['businesses']


def deleterestaurant(del_list: list[dict], restaurant_rm: dict) -> None:
    '''this is a helper function that will search through a given list for a single item and delete it'''

    index = 0
    for restaurant in del_list:
        if restaurant_rm == restaurant:
            # this will exit after deleting the item because there should only be one item to delete
            # makes it slightly more efficient and avoids iteration issues
            del del_list[index]
            break
        index += 1


def filterByPrice(restaurantList: list[dict], price: str) -> list[dict]:
    '''takes a price and the list of restaurants and then filters out the restaurants that are over the price,
    price should be a string of dolarsigns $$ and it will compare the lengths to each of the restaurants '''

    filteredList = []

    for location in restaurantList:
        # checks if a price exists for the restaurant and adds it to a list if it is equal to or under
        if 'price' in location:
            # it checks the length since the input will be $$, and the more $ there is the longer the string
            if len(location['price']) <= len(price):
                filteredList.append(location)
        else:
            # if the price is not listed, then add it anyways because it wont be considered
            filteredList.append(location)

    return filteredList


def filterByRating(restaurantList: list[dict], rating: int) -> list[dict]:
    '''takes a rating and the list of restaurants and then filters out the restaurants that are not above that threshold'''

    filteredList = []
    for location in restaurantList:
        # checks if a rating exists for the restaurant and adds it to a list if it is equal or above
        if 'rating' in location:
            if (restaurantList['rating'] >= rating):
                filteredList.append(location)
        else:
            # if the rating is not listed, then add it anyways because it wont be considered
            filteredList.append(location)

    return filteredList


def getResultsUTC() -> list[dict]:
    '''gets the results from the Yelp API at UTC'''

    # sends a get request to yelp about food places around UTC
    url = f"https://api.yelp.com/v3/businesses/search?latitude=33.650551206116795&longitude=-117.83889468961557&term=food&radius={UTC_RADIUS}&sort_by=best_match&limit={LIMIT}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bB0ZapOxzLjsHScdSZc2iOD_8PjTuGXiLvEeB2UseuIZKBV4KRPGKZ6TgLchYZfzXxX219srxe_GLnq8eaOPpx5H1M9TmCODk7Cb6JuTZyWASGYrSIPz24oXBp1GZXYx"
    }

    return _parse(requests.get(url, headers=headers).json())


def getResultsPlaza() -> list[dict]:
    '''gets the results from the Yelp API at campus plaza'''

    # sends a get request to yelp about food places around Campus Plaza
    url = f"https://api.yelp.com/v3/businesses/search?latitude=33.64960859868817&longitude=-117.83154993786337&term=food&radius={CAMPUS_PLAZA_RADIUS}&sort_by=best_match&limit={LIMIT}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bB0ZapOxzLjsHScdSZc2iOD_8PjTuGXiLvEeB2UseuIZKBV4KRPGKZ6TgLchYZfzXxX219srxe_GLnq8eaOPpx5H1M9TmCODk7Cb6JuTZyWASGYrSIPz24oXBp1GZXYx"
    }

    return _parse(requests.get(url, headers=headers).json())


def getResultsOutUCI(UTC: list[dict], Plaza: list[dict]) -> list[dict]:
    '''gets the results from the Yelp API and filters out all the locations found at UTC and the Plaza'''

    # sends a get request to yelp about food places around UCI within 10,000 meters
    url = f"https://api.yelp.com/v3/businesses/search?latitude=33.64602211664342&longitude=-117.84272864126669&term=food&radius={OUTSIDE_UCI_RADIUS}&sort_by=best_match&limit={LIMIT}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bB0ZapOxzLjsHScdSZc2iOD_8PjTuGXiLvEeB2UseuIZKBV4KRPGKZ6TgLchYZfzXxX219srxe_GLnq8eaOPpx5H1M9TmCODk7Cb6JuTZyWASGYrSIPz24oXBp1GZXYx"
    }

    OutSideUCI = _parse(requests.get(url, headers=headers).json())

    # loops through the UTC and Plaza lists to remove any items that are within UCI
    # since locations inside UCI are not on the yelp API, then removing them is not needed
    for restaurant in UTC:
        deleterestaurant(OutSideUCI, restaurant)

    for restaurant in Plaza:
        deleterestaurant(OutSideUCI, restaurant)

    return OutSideUCI


def getAllResults() -> list[dict]:
    '''gets all the results from the Yelp API and returns it as a python dictionary'''

    # sends a get request to yelp about food places around UCI within 10,000 meters
    url = f"https://api.yelp.com/v3/businesses/search?latitude=33.64602211664342&longitude=-117.84272864126669&term=food&radius=10000&sort_by=best_match&limit={LIMIT}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bB0ZapOxzLjsHScdSZc2iOD_8PjTuGXiLvEeB2UseuIZKBV4KRPGKZ6TgLchYZfzXxX219srxe_GLnq8eaOPpx5H1M9TmCODk7Cb6JuTZyWASGYrSIPz24oXBp1GZXYx"
    }

    return _parse(requests.get(url, headers=headers).json())


def getResultsInUCI() -> list[dict]:
    '''this will open the local restaurants in the json and return a dictionary'''

    # loads the json file
    with open('./on_campus_locations.json', 'r') as file:
        InUCI = json.load(file)

    return InUCI


def getResultsOfClubs() -> list[dict]:
    '''this will open the clubs in the json and return a dictionary'''

    # loads the json file
    with open('./clubs.json', 'r') as file:
        clubs = json.load(file)

    return clubs


@app.route('/')
def getResults() -> 'json':
    '''Recives a get request and queries the the yelp api to get information on '''
    try:
        # this will get the query paramters
        locationFilter = request.args.get('location')
        pricingFilter = request.args.get('pricing')
        ratingFilter = request.args.get('rating')
        randomFilter = request.args.get('random')
        
        if locationFilter != None:
            locationFilter.strip()
        if pricingFilter != None:
            pricingFilter.strip()
        if ratingFilter != None:
            ratingFilter.strip()
        if randomFilter != None:
            randomFilter.strip() 

        # depending on the location sent, it will query the yelp API accordingly
        if locationFilter == 'UTC':
            locations = getResultsUTC()
        elif locationFilter == 'Campus Plaza':
            locations = getResultsPlaza()
        elif locationFilter == 'On campus':
            locations = getResultsOfClubs()
            locations = locations + getResultsInUCI()
        elif locationFilter == 'Nearby campus':
            UTC = getResultsUTC()
            Plaza = getResultsPlaza()
            locations = getResultsOutUCI(UTC, Plaza)
        else:
            # this will account for no location, in which it will all the resturants nearby
            locations = getResultsOfClubs()
            locations = locations + getResultsInUCI()
            locations = locations + getAllResults()

        # checks if there is a filter in place and applies them
        if pricingFilter != None:
            locations = filterByPrice(locations, pricingFilter)
        if ratingFilter != None and ratingFilter != '':
            locations = filterByRating(locations, int(ratingFilter[0]))

        # checks if the query is asking for a random one, if so it will get a random location
        if randomFilter != None:
            randomIndex = random.randint(0, len(locations))
            return jsonify(locations[randomIndex])

    except Exception as e: 
        print(e)
        return {'ERROR': str(e)}

    return jsonify(locations)

if __name__ == '__main__':
   print(getResults()) 
   