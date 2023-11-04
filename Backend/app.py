from flask import Flask, jsonify
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)

@app.route('/results')
def getResults():
    
        
    url = "https://api.yelp.com/v3/businesses/search?latitude=33.650551206116795&longitude=-117.83889468961557&term=food&radius=10000&sort_by=best_match&limit=20"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bB0ZapOxzLjsHScdSZc2iOD_8PjTuGXiLvEeB2UseuIZKBV4KRPGKZ6TgLchYZfzXxX219srxe_GLnq8eaOPpx5H1M9TmCODk7Cb6JuTZyWASGYrSIPz24oXBp1GZXYx"
    }

    response = requests.get(url, headers=headers)

    return jsonify(response)




