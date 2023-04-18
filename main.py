import requests
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["API_KEY"]
RIPE_API = "https://atlas.ripe.net/api/v2/probes"
MEASUREMENT_API = "https://atlas.ripe.net/api/v2/measurements/"
STARLINK_PARAMS = {"status_name": "Connected", "tags": "starlink", "asn": 14593}


def get_starlink_probe_ids():
    response = requests.get(RIPE_API, params=STARLINK_PARAMS)
    json = response.json()
    return [p["id"] for p in json["results"]]


def spawn_pings(probe_ids, target):
    spawn_data = {
        "definitions": [
            {
                "target": target,
                "description": f"{target} pings",
                "type": "ping",
                "af": 4,
                "stop_time": str(datetime.now(timezone.utc) + timedelta(days=1)),
                "interval": 15 * 60,
            }
        ],
        "probes": [
            {
                "requested": min(25, len(probe_ids)),
                "type": "probes",
                "value": ",".join([str(i) for i in probe_ids[:25]]),
            }
        ],
    }
    headers = {
        "Authorization": f"Key {API_KEY}",
    }
    response = requests.post(MEASUREMENT_API, json=spawn_data, headers=headers)
    return response.json()


if __name__ == "__main__":
    probe_ids = get_starlink_probe_ids()
    print(spawn_pings(probe_ids, "google.com"))
    print(probe_ids)
