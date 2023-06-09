# Measuring Starlink Latency from RIPE Atlas

## Authors: Ben Kogan, Margia Rounok, Robert Zhao

This repository contains the code we used to:
- Request the probes connected to the Starlink network
- Create ping measurment every 15 minutes for one day
- Retrieve the results with average RTTs over time for each probe
- Plot the results for analysis

To run the code, first activate your virtual environment and install the dependencies with `pip install -r requirements.txt`. You can then run the code with `python main.py`.

The code currently retrieves the results from our measurement and saves the plot images to the "graphs/combined" directory. By default, the plots combine all of the results from each probe into one plot for each region, but you can specify the "separate" command-line argument to plot each probe separately. These will be saved to the "graphs/separate" directory.

The functions for retrieving the probe IDs and creating the measurement are not called in the main function, since they require credits and an API key. You can specify your API key in a .env file with the key "API_KEY".
