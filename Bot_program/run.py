import os
import serpapi
import json
import random

import GeoQuest.Bot_program.countries as countries

SERPAPI_KEY = '49f5e2bbce2ef9327cf096793312adadd18668aff11ffaa8b10037e7ac29e7e7'

client = serpapi.Client(api_key=os.getenv(SERPAPI_KEY))


def run_cities():
    # Open JSON with the list of big Russian cities
    with open('big_russian_cities.json') as json_file:
        cities = json.load(json_file)["cities"]

    # Choose one random city
    city = random.choice(cities)

    # Setting parameters for the id-search
    params_for_id = {
        "engine": "google_maps",
        "q": city["name"],
        "hl": "ru",
        "type": "search",
        "api_key": SERPAPI_KEY
    }

    # Getting results of the id-search
    results = client.search(params_for_id)["place_results"]

    # Setting parameters for the photo-search
    params_for_photo = {
        "engine": "google_maps_photos",
        "data_id": results["data_id"],
        "api_key": SERPAPI_KEY
    }

    # Getting 30 first results of the photo-search
    all_photos = client.search(params_for_photo)["photos"][:30]

    # Making the list of five photos
    random_five = random.sample(all_photos, 5)
    links = [random_five[0]["image"], random_five[1]["image"],
             random_five[2]["image"], random_five[3]["image"],
             random_five[4]["image"]]

    coords = (results["gps_coordinates"]["latitude"],
              results["gps_coordinates"]["longitude"])

    return links, city["name"], coords


def run_countries():
    # Choose one random country
    country = random.choice(list(countries.available_countries.keys()))

    # Setting parameters for the id-search
    params_for_id = {
        "engine": "google_maps",
        "q": country,
        "hl": "ru",
        "type": "search",
        "api_key": SERPAPI_KEY
    }

    # Getting results of the id-search
    results = client.search(params_for_id)["place_results"]["data_id"]

    # Setting parameters for the photo-search
    params_for_photo = {
        "engine": "google_maps_photos",
        "data_id": results,
        "api_key": SERPAPI_KEY
    }

    # Getting 30 first results of the photo-search
    all_photos = client.search(params_for_photo)["photos"][:30]

    # Making the list of five photos
    random_five = random.sample(all_photos, 5)
    links = [random_five[0]["image"], random_five[1]["image"], random_five[2]["image"], random_five[3]["image"],
             random_five[4]["image"]]

    return links, country
