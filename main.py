import os
import requests
import serpapi

client = serpapi.Client(api_key=os.getenv("d1dd78ada0cdcb4fe90e1b06efdea2928bf3f768b93e321653169bc7f452a301"))
params_for_id = {
  "engine": "google_maps",
  "q": "Киров",
  "hl": "ru",
  "type": "search",
  "api_key": "d1dd78ada0cdcb4fe90e1b06efdea2928bf3f768b93e321653169bc7f452a301"
}

results = client.search(params_for_id)["place_results"]["data_id"]

params_for_photo = {
  "engine": "google_maps_photos",
  "data_id": results,
  "api_key": "d1dd78ada0cdcb4fe90e1b06efdea2928bf3f768b93e321653169bc7f452a301"
}

all_photos = client.search(params_for_photo)["photos"]

links = [all_photos[0]["image"], all_photos[1]["image"], all_photos[2]["image"]]

print(links)
