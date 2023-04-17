import requests
import os
import json
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

def spawn_pings(probe_ids, target, key=API_KEY):
    spawn_data = {
        "definitions": [
            {
                "target": target, 
                "description": "fuck you gpt", 
                "type": "ping",
                "af": 4,
                "resolve_on_probe": False,
                "is_public": False,
            }
        ],
        "probes": [
            {
                "requested": 25,
                "type": "probes",
                "value": ','.join([str(i) for i in probe_ids[0:25]])
            }
        ]
    }
    headers = {"Content-Type": "application/json", "Authorization": "Key {}".format(API_KEY)}
    response = requests.post(MEASUREMENT_API, data=json.dumps(spawn_data), headers=headers)
    return response.json()

if __name__ == "__main__":
    print(API_KEY)
    probe_ids = get_starlink_probe_ids()
    print(spawn_pings(probe_ids, "www.reddit.com", API_KEY))
    print(probe_ids)
