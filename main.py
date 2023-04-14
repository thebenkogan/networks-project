import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["API_KEY"]
RIPE_API = "https://atlas.ripe.net/api/v2/probes"
STARLINK_PARAMS = {"status_name": "Connected", "tags": "starlink"}


def get_starlink_probe_ids():
    response = requests.get(RIPE_API, params=STARLINK_PARAMS)
    json = response.json()

    return [p["id"] for p in json["results"]]


if __name__ == "__main__":
    print(API_KEY)
    probe_ids = get_starlink_probe_ids()
    print(probe_ids)
