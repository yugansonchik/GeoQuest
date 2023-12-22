import os
import serpapi
import json
import random

from GeoQuest.Bot_program.Game_formation.countries import available_counties

client = serpapi.Client(api_key=os.getenv("d1dd78ada0cdcb4fe90e1b06efdea2928bf3f768b93e321653169bc7f452a301"))


def run_cities():
    # Open JSON with the list of big Russian cities
    with open('Game_formation/big_russian_cities.json') as json_file:
        cities = json.load(json_file)["cities"]

    # Choose one random city
    city = random.choice(cities)

    # Setting parameters for the id-search
    params_for_id = {
        "engine": "google_maps",
        "q": city["name"],
        "hl": "ru",
        "type": "search",
        "api_key": "c0300a70404e97563d66c62c41e272e8e9ee995f6e1abbffef49b719b181c9ce"
    }

    # Getting results of the id-search
    results = client.search(params_for_id)["place_results"]["data_id"]

    # Setting parameters for the photo-search
    params_for_photo = {
        "engine": "google_maps_photos",
        "data_id": results,
        "api_key": "c0300a70404e97563d66c62c41e272e8e9ee995f6e1abbffef49b719b181c9ce"
    }

    # Getting 30 first results of the photo-search
    all_photos = client.search(params_for_photo)["photos"][:30]

    # Making the list of five photos
    random_five = random.sample(all_photos, 5)
    links = [random_five[0]["image"], random_five[1]["image"], random_five[2]["image"], random_five[3]["image"],
             random_five[4]["image"]]

    return links, city["name"]


def run_countries():
    # Choose one random country
    country = random.choice(available_counties)

    # Setting parameters for the id-search
    params_for_id = {
        "engine": "google_maps",
        "q": country,
        "hl": "ru",
        "type": "search",
        "api_key": "d1dd78ada0cdcb4fe90e1b06efdea2928bf3f768b93e321653169bc7f452a301"
    }

    # Getting results of the id-search
    results = client.search(params_for_id)["place_results"]["data_id"]

    # Setting parameters for the photo-search
    params_for_photo = {
        "engine": "google_maps_photos",
        "data_id": results,
        "api_key": "d1dd78ada0cdcb4fe90e1b06efdea2928bf3f768b93e321653169bc7f452a301"
    }

    # Getting 30 first results of the photo-search
    all_photos = client.search(params_for_photo)["photos"][:30]

    # Making the list of five photos
    random_five = random.sample(all_photos, 5)
    links = [random_five[0]["image"], random_five[1]["image"], random_five[2]["image"], random_five[3]["image"],
             random_five[4]["image"]]

    return links, country


if __name__ == '__main__':
    run_cities()
