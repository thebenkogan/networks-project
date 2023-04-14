import requests

RIPE_API = "https://atlas.ripe.net/api/v2/probes?status_name=Connected&tags=starlink"


def get_starlink_probe_ids():
    response = requests.get(RIPE_API)
    json = response.json()

    return list(map(lambda p: p["id"], json["results"]))


if __name__ == "__main__":
    probe_ids = get_starlink_probe_ids()
    print(probe_ids)
