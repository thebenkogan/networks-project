import requests
import os
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter

from datetime import datetime, timedelta
from dotenv import load_dotenv
from ripe.atlas.cousteau import (
    Ping,
    AtlasSource,
    AtlasCreateRequest,
    AtlasResultsRequest,
)
from ripe.atlas.sagan import PingResult
from collections import defaultdict

load_dotenv()

API_KEY = os.environ["API_KEY"]
RIPE_API = "https://atlas.ripe.net/api/v2/probes"
STARLINK_PARAMS = {"status_name": "Connected", "tags": "starlink", "asn": 14593}


def get_starlink_probe_ids():
    response = requests.get(RIPE_API, params=STARLINK_PARAMS)
    json = response.json()
    return [p["id"] for p in json["results"]]


def spawn_pings(probe_ids, target):
    ping = Ping(
        af=4,
        target=target,
        description=f"{target} pings",
        interval=15 * 60,
    )

    source = AtlasSource(
        type="probes",
        requested=min(25, len(probe_ids)),
        value=",".join([str(i) for i in probe_ids[:25]]),
    )

    atlas_request = AtlasCreateRequest(
        start_time=datetime.utcnow(),
        stop_time=datetime.utcnow() + timedelta(days=1),
        key=API_KEY,
        measurements=[ping],
        sources=[source],
        is_oneoff=False,
    )

    return atlas_request.create()


# Returns a dictionary of probe id -> list of (timestamp, RTT) tuples
def fetch_ping_results(msm_id):
    fetch_args = {
        "msm_id": msm_id,
    }

    _, results = AtlasResultsRequest(**fetch_args).create()
    results = [PingResult(res) for res in results]

    probe_rtts_over_time = defaultdict(list)

    for res in results:
        probe_rtts_over_time[res.probe_id].append((res.created, res.rtt_average))

    return probe_rtts_over_time

def create_plots(probe_data):
    # plot the graph for each key in the dictionary
    for key in probe_data.keys():
        # get datetime objects and rtt values from the list of tuples
        x = [t[0] for t in probe_data[key]]
        y = [t[1] for t in probe_data[key]]
        
        # plot the graph
        plt.plot(x, y, marker='o', label=key)

    # set labels and legend
    plt.xlabel('UTC Time')
    plt.ylabel('RTT')
    plt.title('Probe ID RTT Over Time')

    plt.legend()

    # set the xticks to only show every other label
    ax = plt.gca()
    xticks = ax.get_xticks()
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    ax.set_xticks(xticks[::3])

    # show the plot
    plt.show()

if __name__ == "__main__":
    # probe_ids = get_starlink_probe_ids()
    # print(probe_ids)
    # print(spawn_pings(probe_ids, "www.google.com"))
    res = fetch_ping_results(26445013)
    create_plots(res)
