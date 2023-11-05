from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json

UTC_RADIUS = 360
CAMPUS_PLAZA_RADIUS = 220
OUTSIDE_UCI_RADIUS = 1000


app = Flask(__name__)
CORS(app)

UTC = []
Plaza = []
OutSideUCI = []
InUCI = []

@app.route('/')
def getResults():
    
    getResultsUTC()
    getResultsInUCI()
    getResultsPlaza()
    getResultsOutUCI()



def getResultsUTC():
        
    url = "https://api.yelp.com/v3/businesses/search?latitude=33.650551206116795&longitude=-117.83889468961557&term=food&radius=360&sort_by=best_match&limit=50"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bB0ZapOxzLjsHScdSZc2iOD_8PjTuGXiLvEeB2UseuIZKBV4KRPGKZ6TgLchYZfzXxX219srxe_GLnq8eaOPpx5H1M9TmCODk7Cb6JuTZyWASGYrSIPz24oXBp1GZXYx"
    }

    UTC = _parse(requests.get(url, headers=headers).json())



def getResultsPlaza():
        
    url = "https://api.yelp.com/v3/businesses/search?latitude=33.64960859868817&longitude=-117.83154993786337&term=food&radius=220&sort_by=best_match&limit=20"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bB0ZapOxzLjsHScdSZc2iOD_8PjTuGXiLvEeB2UseuIZKBV4KRPGKZ6TgLchYZfzXxX219srxe_GLnq8eaOPpx5H1M9TmCODk7Cb6JuTZyWASGYrSIPz24oXBp1GZXYx"
    }

    Plaza = _parse(requests.get(url, headers=headers).json())



def getResultsOutUCI() -> 'json':

    url = "https://api.yelp.com/v3/businesses/search?latitude=33.64602211664342&longitude=-117.84272864126669&term=food&radius=10000&sort_by=best_match&limit=20"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bB0ZapOxzLjsHScdSZc2iOD_8PjTuGXiLvEeB2UseuIZKBV4KRPGKZ6TgLchYZfzXxX219srxe_GLnq8eaOPpx5H1M9TmCODk7Cb6JuTZyWASGYrSIPz24oXBp1GZXYx"
    }
    
    OutSideUCI = _parse(requests.get(url, headers=headers).json())
        
    for resturant in UTC: 
        deleteResturant(OutSideUCI, resturant)
    
    for resturant in Plaza:
        deleteResturant(OutSideUCI, resturant)




def deleteResturant(del_list : list, resturant_rm : dict) -> None:
    index = 0
    for resturant in del_list:
        if resturant_rm == resturant:
            del del_list[index]
            break
        index += 1
            
        

def getResultsInUCI():
        
    with open('./on_campus_locations.json', 'r') as file:
        InUCI = json.load(file)

    return jsonify(InUCI.json())


def _parse(res: dict) -> list:
    '''Returns a list that only has the needed attributes of the locations'''
    copy_of_res = res.copy()

    needed_attributes = ['name', 'image_url', 'rating', 'price', 'location', 'display_phone', 'distance']
    for location in copy_of_res['businesses']:
        attributes_to_delete = []
        for attribute in location:
            if attribute not in needed_attributes:
                attributes_to_delete.append(attribute)
        for attribute in attributes_to_delete:
            del location[attribute]
        
    return copy_of_res['businesses']