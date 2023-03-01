from flask import Flask, render_template, request, redirect, url_for
import base64
import requests
from requests import post, get
import json
import pycountry
from geopy.geocoders import Nominatim
import folium
import csv

CLIENT_ID = '0eb4a8d852b8488fbad67a83956d0a0e'
CLIENT_SECRET = '071812ad19cd47df8fe78085995820a1'

app = Flask(__name__)

@app.route('/')

def home():
    """
    do home
    """
    return render_template('home.html')

@app.route('/map', methods=['POST'])

def but():
    """
    gets text from input
    """
    # with open('countries.csv', mode='r') as file:

    #     # Create a CSV reader object
    #     csv_reader = csv.reader(file)
    #     countries = list(csv_reader)
    token = get_token()
    iput = request.form['iput']
    artist_info = search_aut(token, iput)
    markets_track = []
    for market in get_markets(token)["markets"]:
        tracks = get_tracks(get_token(), artist_info["artists"]["items"][0]["id"], market)
        country = pycountry.countries.get(alpha_2=market)
        geolocator = Nominatim(user_agent="get_location")
        if not country:
            continue
        else:
            location = geolocator.geocode(country.name, timeout=100)
        # with open("tracks.json", "a", encoding="utf-8") as fff:
            # fff.write(str(country))
        #     # json.dump(tracks, fff, indent = 4, ensure_ascii=False)
        #     try:
        #         fff.write(location)
        #     except:
        #         pass
        try:
            markets_track.append((tracks["tracks"][0]["name"], (location.latitude, location.longitude)))
        except:
            continue
    map = folium.Map(tiles="Stamen Toner",
                    location=[49.817545, 24.023932],
                    zoom_start=5)
    for track in markets_track:
        try:
            map.add_child(folium.Marker(track[1],
                                        popup=track[0],
                                        icon=folium.Icon(color="purple")))
        except:
            continue
    return map._repr_html_()



def get_token():
    """
    gets token
    """
    auth_code = f'{CLIENT_ID}:{CLIENT_SECRET}'
    code_credential = str(base64.b64encode(auth_code.encode("utf-8")), "utf-8")
    url = 'https://accounts.spotify.com/api/token'

    headers = {
        "Authorization": "Basic " + code_credential,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_res = json.loads(result.content)
    return json_res["access_token"]


def get_aut_head(token):
    """
    gets autorization header
    """
    return {'Authorization': f'Bearer {token}'}


def search_aut(token, artist):
    """
    searches for artist
    """
    url = 'https://api.spotify.com/v1/search'
    request_params = {
        'query': artist,
        'type': 'artist'
    }
    response = requests.get(url, headers = get_aut_head(token), params=request_params)
    response_data = response.json()
    return response_data


def get_tracks(token, id_art, country_code):
    """
    get tracks
    """
    url = f'https://api.spotify.com/v1/artists/{id_art}/top-tracks?country={country_code}'
    response = requests.get(url, headers = get_aut_head(token))
    responce_data = response.json()
    return responce_data


def get_markets(token):
    """
    gets markets
    """
    url = 'https://api.spotify.com/v1/markets'
    response = requests.get(url, headers = get_aut_head(token))
    response_data = response.json()
    # with open("markets.json", "w", encoding="utf-8") as fff:
            # json.dump(response_data, fff, indent = 4, ensure_ascii=False)
    return response_data

import requests

def get_country(lat, lon):
    url = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&accept-language=en&zoom=3'
    try:
        result = requests.get(url=url)
        result_json = result.json()
        return result_json['display_name']
    except:
        return None

# print(get_country(32.782023,35.478867)) # results in Israel