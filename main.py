import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["API_KEY"]
RIPE_API = "https://atlas.ripe.net/api/v2/probes"
MEASUREMENT_API = url = 'https://atlas.ripe.net/api/v2/measurements/'
STARLINK_PARAMS = {"status_name": "Connected", "tags": "starlink", "asn": 14593}


def get_starlink_probe_ids():
    response = requests.get(RIPE_API, params=STARLINK_PARAMS)
    json = response.json()
    return [p["id"] for p in json["results"]]

def spawn_pings(probe_ids, target):
    spawn_params = {
        "definitions": [{
            "description": "test",
            "type": "ping",
            "packets": 1,
            "target": target
        }],
        "probes": [{"value": str(probe_id)} for probe_id in probe_ids],
        "is_oneoff": True
    }
    response = requests.get(MEASUREMENT_API, params=STARLINK_PARAMS)
    return response["measurements"]

if __name__ == "__main__":
    print(API_KEY)
    probe_ids = get_starlink_probe_ids()
    # spawn_pings(probe_ids, "")
    print(probe_ids)
