import matplotlib.pyplot as plt
import math
from matplotlib.dates import DateFormatter, HourLocator
import os

LOCATIONS = {
    "USA1 (East Coast)": [60510, 63017, 61780, 62417, 62553, 61081],
    "USA2 (Midwest and West Coast)": [
        54330,
        62613,
        53798,
        60929,
        62498,
        62868,
        62083,
        61113,
    ],
    "EUROPE": [61878, 62843, 60323, 1002289, 35681, 20544, 50008],
    "OCEANIA": [19983, 52955],
}
COMBINED_DIR = "graphs/combined"
SEPARATE_DIR = "graphs/separate"


def create_separate_plots(probe_data, show=False, save=True):
    if save and not os.path.isdir(SEPARATE_DIR):
        os.makedirs(SEPARATE_DIR)

    # plot the graph for each key in the dictionary
    for location, probe_ids in LOCATIONS.items():
        r, c = (math.ceil(len(probe_ids) / 2), 2)
        fig, axs = plt.subplots(r, c, figsize=(10, 10), constrained_layout=True)
        axs = axs.flatten()
        fig.suptitle(location)
        for j, p in enumerate(probe_ids):
            # get datetime objects and rtt values from the list of tuples
            x = [t[0] for t in probe_data[p]]
            y = [t[1] for t in probe_data[p]]

            # plot the graph
            axs[j].plot(x, y, marker="o", label=p)

            # set labels and legend
            axs[j].set_xlabel("UTC Time")
            axs[j].set_ylabel("RTT")
            axs[j].set_title("{}".format(p))
            axs[j].xaxis.set_major_formatter(DateFormatter("%H:%M:%S"))
            axs[j].xaxis.set_major_locator(HourLocator(interval=4))
            for tick in axs[j].xaxis.get_major_ticks():
                tick.label1.set_fontsize(8)
        if save:
            plt.savefig(f"{SEPARATE_DIR}/{location}.png", dpi=500)
    if show:
        plt.show()


def create_combined_plots(probe_data, show=False, save=True):
    if save and not os.path.isdir(COMBINED_DIR):
        os.makedirs(COMBINED_DIR)

    # plot the graph for each key in the dictionary
    for i, (location, probe_ids) in enumerate(LOCATIONS.items()):
        plt.figure(i + 1, figsize=(10, 10))
        plt.title(location)
        for p in probe_ids:
            # get datetime objects and rtt values from the list of tuples
            x = [t[0] for t in probe_data[p]]
            y = [t[1] for t in probe_data[p]]

            # plot the graph
            plt.plot(x, y, marker="o", label=p)

            # set labels and legend
            plt.xlabel("UTC Time")
            plt.ylabel("RTT")

            ax = plt.gca()
            ax.xaxis.set_major_formatter(DateFormatter("%H:%M:%S"))
            ax.xaxis.set_major_locator(HourLocator(interval=4))
            plt.legend()
        if save:
            plt.savefig(f"{COMBINED_DIR}/{location}.png", dpi=500)
    if show:
        plt.show()
