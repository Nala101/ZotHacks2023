from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json

UTC_RADIUS = 360
CAMPUS_PLAZA_RADIUS = 220
OUTSIDE_UCI_RADIUS = 1000


app = Flask(__name__)
CORS(app)

UTC = {}
Plaza = {}
OutSideUCI = {}
InUCI = {}



@app.route('/UTC')
def getResultsUTC():
        
    url = "https://api.yelp.com/v3/businesses/search?latitude=33.650551206116795&longitude=-117.83889468961557&term=food&radius=360&sort_by=best_match&limit=50"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bB0ZapOxzLjsHScdSZc2iOD_8PjTuGXiLvEeB2UseuIZKBV4KRPGKZ6TgLchYZfzXxX219srxe_GLnq8eaOPpx5H1M9TmCODk7Cb6JuTZyWASGYrSIPz24oXBp1GZXYx"
    }

    UTC = requests.get(url, headers=headers).json()

    return jsonify(UTC)


@app.route('/CampusPlaza')
def getResultsPlaza():
        
    url = "https://api.yelp.com/v3/businesses/search?latitude=33.64960859868817&longitude=-117.83154993786337&term=food&radius=220&sort_by=best_match&limit=20"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bB0ZapOxzLjsHScdSZc2iOD_8PjTuGXiLvEeB2UseuIZKBV4KRPGKZ6TgLchYZfzXxX219srxe_GLnq8eaOPpx5H1M9TmCODk7Cb6JuTZyWASGYrSIPz24oXBp1GZXYx"
    }

    Plaza = requests.get(url, headers=headers).json()

    return jsonify(Plaza)


@app.route('/OutsideUCI')
def getResultsOutUCI():

    url = "https://api.yelp.com/v3/businesses/search?latitude=33.64602211664342&longitude=-117.84272864126669&term=food&radius=10000&sort_by=best_match&limit=20"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bB0ZapOxzLjsHScdSZc2iOD_8PjTuGXiLvEeB2UseuIZKBV4KRPGKZ6TgLchYZfzXxX219srxe_GLnq8eaOPpx5H1M9TmCODk7Cb6JuTZyWASGYrSIPz24oXBp1GZXYx"
    }
    
    OutSideUCI = requests.get(url, headers=headers).json()
        
    for resturant in UTC['businesses']: 
        deleteResturant(OutSideUCI['businesses'], resturant['name'])
    
    for resturant in Plaza['businesses']:
        del OutSideUCI['businesses'][resturant['name']]


    return jsonify(OutSideUCI.json())


def deleteResturant(del_list, string):
    for resturant in del_list:
        


@app.route('/InsideUCI')
def getResultsInUCI():
        
    with open('./on_campus_locations.json', 'r') as file:
        InUCI = json.load(file)

    return jsonify(InUCI.json())






